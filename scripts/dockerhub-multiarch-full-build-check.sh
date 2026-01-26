#!/bin/bash
set -e

GIT_DIFF_BASE="$1"
GIT_DIFF_HEAD="$2"
THRESHOLD_HOURS=${THRESHOLD_HOURS:-24}
THRESHOLD_SECONDS=$((THRESHOLD_HOURS * 3600))
EXIT_CODE=0

command -v crane >/dev/null 2>&1 || { echo >&2 "crane is required but not installed. Aborting."; exit 1; }

if [ -z "$GIT_DIFF_BASE" -o -z "$GIT_DIFF_HEAD" ]; then
  echo "Usage: $0 <base_sha> <head_sha>"
  exit 1
fi

# Function to get manifest info using crane
get_manifest_info() {
    local image="$1"
    local json
    json=$(crane manifest "$image" 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$json" ]; then
        return 1
    fi
    
    # Check if it's a manifest list/index
    local media_type
    media_type=$(echo "$json" | jq -r '.mediaType')
    
    if [[ "$media_type" == *"index"* ]] || [[ "$media_type" == *"manifest.list"* ]]; then
        # Multi-arch
        echo "$json" | jq -c '
            .manifests | map(
                select(.platform.os != "unknown" and .platform.os != null) | 
                {
                    key: (
                        .platform.os + "/" + .platform.architecture + 
                        (if .platform.variant then "/" + .platform.variant else "" end)
                    ),
                    value: {
                        digest: .digest,
                        created: .annotations["org.opencontainers.image.created"]
                    }
                }
            ) | from_entries
        '
    else
        # Single arch
        local config
        config=$(crane config "$image")
        local platform
        platform=$(echo "$config" | jq -r '.os + "/" + .architecture + (if .variant then "/" + .variant else "" end)')
        local created
        created=$(echo "$config" | jq -r '.created')
        local digest
        digest=$(crane digest "$image")
        
        echo "{}" | jq -c --arg p "$platform" --arg d "$digest" --arg c "$created" '. + {($p): {digest: $d, created: $c}}'
    fi
}

print_info() {
    local label="$1"
    local info="$2"
    echo "  $label info:"
    if [ "$info" == "{}" ]; then
        echo "    (none)"
        return
    fi
    echo "$info" | jq -r 'to_entries | .[] | "    - \(.key): \(.value.digest) (\(.value.created // "N/A"))"'
}

# Find all Dockerfiles in containers/ directory
DOCKERFILES=$(git diff --name-only "$GIT_DIFF_BASE..$GIT_DIFF_HEAD" | grep "containers/.*/Dockerfile" || true)

if [ -z "$DOCKERFILES" ]; then
    echo "No Dockerfiles changed in containers/."
    exit 0
fi

for df in $DOCKERFILES; do
    if [ ! -f "$df" ]; then continue; fi
    
    echo "Checking $df..."
    
    # Extract base images
    NEW_FROM=$(grep "^FROM" "$df" | head -n1 | awk '{print $2}')
    OLD_FROM=$(git show "$GIT_DIFF_BASE:$df" 2>/dev/null | grep "^FROM" | head -n1 | awk '{print $2}')
    
    if [ -z "$NEW_FROM" ]; then
        echo "  [SKIP] No FROM instruction found in $df"
        continue
    fi
    
    if [ "$NEW_FROM" == "$OLD_FROM" ]; then
        echo "  [SKIP] Base image didn't change"
        continue
    fi
    
    echo "  Old base: $OLD_FROM"
    echo "  New base: $NEW_FROM"
    
    echo "  Fetching manifest info for new base..."
    NEW_INFO=$(get_manifest_info "$NEW_FROM")
    if [ $? -ne 0 ]; then
        echo "  [ERROR] Failed to fetch manifest info for $NEW_FROM"
        EXIT_CODE=1
        continue
    fi
    
    OLD_INFO="{}"
    if [ -n "$OLD_FROM" ]; then
        echo "  Fetching manifest info for old base..."
        OLD_INFO=$(get_manifest_info "$OLD_FROM" || echo "{}")
    fi

    print_info "Old base" "$OLD_INFO"
    print_info "New base" "$NEW_INFO"
    
    # 1. Architecture Retention Check
    MISSING_ARCHS=$(echo "$NEW_INFO $OLD_INFO" | jq -rs '
        .[1] as $old | .[0] as $new |
        $old | keys | .[] | select(. as $k | $new[$k] | not)
    ' | xargs echo)
    
    if [ -n "$MISSING_ARCHS" ]; then
        echo "  [FAIL] Missing architectures that were present in old base: $MISSING_ARCHS"
        echo "::error file=$df::Missing architectures that were present in old base image: $MISSING_ARCHS"
        EXIT_CODE=1
    fi
    
    # 2. Sync Check (Timestamp Spread)
    TIMESTAMPS=$(echo "$NEW_INFO" | jq -r 'to_entries | map(select(.value.created != null) | .value.created) | .[]')
    if [ -n "$TIMESTAMPS" ]; then
        MAX_TS=$(echo "$TIMESTAMPS" | xargs -I{} date -d {} +%s | sort -rn | head -n1)
        MIN_TS=$(echo "$TIMESTAMPS" | xargs -I{} date -d {} +%s | sort -n | head -n1)
        DIFF=$((MAX_TS - MIN_TS))
        
        if [ $DIFF -gt $THRESHOLD_SECONDS ]; then
            HOURS=$((DIFF / 3600))
            echo "  [FAIL] Large timestamp spread: ${HOURS}h (Threshold: ${THRESHOLD_HOURS}h)"
            
            # Identify which archs are old
            STALE_ARCHS=$(echo "$NEW_INFO" | jq -r --argjson max "$MAX_TS" --argjson threshold "$THRESHOLD_SECONDS" '
                to_entries | map(select(.value.created != null and ($max - (.value.created | fromdateiso8601)) > $threshold)) | .[].key
            ' | xargs echo)
            
            echo "  Stale architectures: $STALE_ARCHS"
            echo "::error file=$df::Large timestamp spread (${HOURS}h) in base image. Stale architectures: $STALE_ARCHS"
            EXIT_CODE=1
        fi
    fi
    
    # 3. Hash Stability Check (Mixed old/new digests)
    # If some digests are new and some are old, it is probably still building
    HAS_NEW_DIGESTS=$(echo "$NEW_INFO $OLD_INFO" | jq -rs '
        .[1] as $old | .[0] as $new |
        $new | to_entries | map(select(.key as $k | $old[$k] and .value.digest != $old[$k].digest)) | length > 0
    ')
    
    if [ "$HAS_NEW_DIGESTS" == "true" ]; then
        STUCK_DIGESTS=$(echo "$NEW_INFO $OLD_INFO" | jq -rs '
            .[1] as $old | .[0] as $new |
            $new | to_entries | map(select(.key as $k | $old[$k] and .value.digest == $old[$k].digest)) | .[].key
        ' | xargs echo)
        
        if [ -n "$STUCK_DIGESTS" ]; then
            echo "  [FAIL] Some architectures have new digests, but these are still the same as old base: $STUCK_DIGESTS"
            echo "::error file=$df::Partial rebuild detected. Some architectures have been updated, but these still have the old digest: $STUCK_DIGESTS"
            EXIT_CODE=1
        fi
    fi
    
    if [ "$EXIT_CODE" == "0" ]; then
        echo "  [OK] $df base image is fully built and synchronized."
    fi
done

exit $EXIT_CODE
