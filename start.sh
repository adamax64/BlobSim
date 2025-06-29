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
if [ ! -d "./node_modules" ]; then
    echo "Node modules not found. Run setup.sh to create them."
    exit 1
fi
npm run start

echo "Application startup complete"
