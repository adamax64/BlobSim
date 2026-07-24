#!/bin/bash

# filepath: /d:/SoftwareDevelopement/BlobSim/setup.sh

if command -v python3 &> /dev/null; then
    python_exec="python3"
else
    python_exec="python"
fi

$python_exec -m venv venv
source venv/bin/activate
$python_exec -m pip install --upgrade pip
pip install -r requirements.txt

cd web-ui
pnpm install
pnpm add -g @openapitools/openapi-generator-cli
pnpm run generate-api
pnpm run build
cd ..

echo "Setup complete"
