#!/bin/bash
set -e

DOCKERFILE="$1"
if [ -z "$DOCKERFILE" ]; then
    echo "Usage: $0 <path_to_dockerfile>"
    exit 1
fi

if [ ! -f "$DOCKERFILE" ]; then
    echo "Error: File $DOCKERFILE not found"
    exit 1
fi

declare -A STAGE_IMAGES
declare -A IMAGE_OS_CACHE

CURRENT_IMAGE=""
EXIT_CODE=0

# Function to get OS version from image
get_image_os() {
    local img="$1"
    if [ -n "${IMAGE_OS_CACHE[$img]}" ]; then
        echo "${IMAGE_OS_CACHE[$img]}"
        return
    fi

    local os_info
    os_info=$(docker run --rm --entrypoint "" "$img" sh -c '
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            if [ "$ID" = "alpine" ]; then
                if [ -f /etc/alpine-release ]; then
                    echo "alpine $(cat /etc/alpine-release)"
                else
                    echo "alpine $VERSION_ID"
                fi
            else
                echo "$ID $VERSION_ID"
            fi
        elif [ -f /etc/alpine-release ]; then
            echo "alpine $(cat /etc/alpine-release)"
        fi
    ' 2>/dev/null || echo "unknown")

    local os_id=$(echo "$os_info" | awk '{print $1}')
    local os_ver=$(echo "$os_info" | awk '{print $2}')
    local mapped_os="unknown"

    case "$os_id" in
        alpine)
            local major_minor=$(echo "$os_ver" | cut -d. -f1,2 | tr '.' '_')
            mapped_os="alpine_${major_minor}"
            ;;
        debian)
            local major=$(echo "$os_ver" | cut -d. -f1)
            mapped_os="debian_${major}"
            ;;
        ubuntu)
            local major_minor=$(echo "$os_ver" | cut -d. -f1,2 | tr '.' '_')
            mapped_os="ubuntu_${major_minor}"
            ;;
    esac

    IMAGE_OS_CACHE["$img"]="$mapped_os"
    echo "$mapped_os"
}

echo "Checking $DOCKERFILE for OS drift..."

while IFS= read -r line || [ -n "$line" ]; do
    # Match FROM instructions
    if [[ "$line" =~ ^[[:space:]]*FROM ]]; then
        image=$(echo "$line" | sed -E 's/^[[:space:]]*FROM[[:space:]]+(--platform=[^[:space:]]+[[:space:]]+)?([^[:space:]]+).*/\2/')
        stage=$(echo "$line" | sed -E 's/.*[Aa][Ss][[:space:]]+([^[:space:]]+).*/\1/')
        
        if [ -n "${STAGE_IMAGES[$image]}" ]; then
            CURRENT_IMAGE="${STAGE_IMAGES[$image]}"
        else
            CURRENT_IMAGE="$image"
        fi

        if [ -n "$stage" ] && [ "$stage" != "$line" ]; then
            STAGE_IMAGES["$stage"]="$CURRENT_IMAGE"
        fi
        continue
    fi

    # Check for renovate repology annotation
    if [[ "$line" =~ renovate:.*datasource=repology ]]; then
        if [ -z "$CURRENT_IMAGE" ]; then
            continue
        fi

        if [[ "$line" =~ depName=([^[:space:]/]+) ]]; then
            expected_prefix="${BASH_REMATCH[1]}"
            actual_os=$(get_image_os "$CURRENT_IMAGE")
            
            if [ "$actual_os" = "unknown" ]; then
                echo "  [WARN] Could not determine OS for image $CURRENT_IMAGE"
            elif [[ "$expected_prefix" != "$actual_os"* ]]; then
                echo "  [ERROR] Drift detected!"
                echo "    Annotation: $expected_prefix"
                echo "    Base image ($CURRENT_IMAGE): $actual_os"
                EXIT_CODE=1
            else
                echo "  [OK] $expected_prefix matches $actual_os"
            fi
        fi
    fi
done < "$DOCKERFILE"

exit $EXIT_CODE
