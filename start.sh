#!/bin/bash

scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$scriptDir"

pidFile="$scriptDir/.backend.pid"

if [ -f "$pidFile" ]; then
    oldPid=$(cat "$pidFile")
    if [ -n "$oldPid" ] && kill -0 "$oldPid" 2>/dev/null; then
        echo "Stopping previous backend process (PID $oldPid)..."
        kill "$oldPid"
    fi
    rm -f "$pidFile"
fi

if command -v python3 &> /dev/null; then
    python_exec="python3"
else
    python_exec="python"
fi

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $python_exec -m venv venv
fi

source venv/bin/activate
echo "Python virtual environment activated"

$python_exec -m pip install --upgrade pip
pip install -r requirements.txt

pushd web-ui > /dev/null
pnpm install

echo "Building frontend..."
pnpm add -g @openapitools/openapi-generator-cli
pnpm run generate-api
pnpm run build

popd > /dev/null

echo "Setup complete"
echo "Starting application..."
nohup $python_exec -m fastapi run main.py > backend.log 2>&1 &
echo $! > "$pidFile"
echo "Backend started with PID $(cat "$pidFile")"
