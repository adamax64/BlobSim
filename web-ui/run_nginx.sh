#!/bin/bash

# Get the directory of this script
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment variables from .env file
envFile="$scriptDir/.env"
if [ -f "$envFile" ]; then
    set -a
    source "$envFile"
    set +a
fi

# Set defaults if not set
export SERVER_NAME="${SERVER_NAME:-localhost}"
export ROOT_PATH="${ROOT_PATH:-$scriptDir/dist}"

# Preprocess nginx config
configTemplate="$scriptDir/nginx.conf"
configOutput="$scriptDir/nginx_processed.conf"

if [ -f "$configTemplate" ]; then
    sed -e "s|\${SERVER_NAME}|$SERVER_NAME|g" \
        -e "s|\${ROOT_PATH}|$ROOT_PATH|g" \
        "$configTemplate" > "$configOutput"
fi

# Run nginx with processed config
# Note: Update the nginx path if it's not in your PATH
if [ -n "$NGINX_PATH" ]; then
    "$NGINX_PATH/nginx" -c "$configOutput"
else
    nginx -c "$configOutput"
fi