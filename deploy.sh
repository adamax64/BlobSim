#!/bin/bash

echo -ne "\033]0;Blob Championship System - Deploy\007"

scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$scriptDir"

branch="main"
pollInterval="${DEPLOY_POLL_INTERVAL:-60}"

echo "Starting application..."
"$scriptDir/start.sh"

echo "Watching origin/$branch for new commits every ${pollInterval}s (Ctrl+C to stop watching; the backend keeps running)..."

while true; do
    sleep "$pollInterval"

    remoteCommit=$(git ls-remote origin "refs/heads/$branch" | cut -f1)
    localCommit=$(git rev-parse HEAD)

    if [ -n "$remoteCommit" ] && [ "$remoteCommit" != "$localCommit" ]; then
        echo "New commits detected on origin/$branch, fetching and updating..."
        git fetch origin "$branch"
        if git pull --ff-only origin "$branch"; then
            echo "Update complete, restarting application..."
            "$scriptDir/start.sh"
        else
            echo "Failed to fast-forward to origin/$branch. Resolve manually before the next check."
        fi
    fi
done
