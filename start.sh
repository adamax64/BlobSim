#!/bin/bash

if command -v python3 &> /dev/null; then
    python_exec="python3"
else
    python_exec="python"
fi

$python_exec -m venv venv
source venv/bin/activate
echo "Python virtual environment activated"
$python_exec -m fastapi run main.py

cd web-ui
if [ ! -d "./dist" ]; then
    echo "Build not found. Run setup.sh to build the project."
    exit 1
fi

echo "Application startup complete"
