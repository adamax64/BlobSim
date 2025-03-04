#!/bin/bash

# filepath: /d:/SoftwareDevelopement/BlobSim/start.sh

echo -ne "\033]0;Blob Championship System\007"

if [ ! -d "./venv" ]; then
    echo "Python virtual environment not found. Run setup.sh to create it."
    read -p "Press any key to exit..."
    exit 1
fi

if command -v python3 &> /dev/null; then
    python_exec="python3"
else
    python_exec="python"
fi

$python_exec -m venv venv
source venv/bin/activate
echo "Python virtual environment activated"
export MODE=prd
$python_exec -m fastapi run main.py &

cd web-ui
if [ ! -d "./node_modules" ]; then
    echo "Node modules not found. Run setup.sh to create them."
    read -p "Press any key to exit..."
    exit 1
fi
npm run start &
xdg-open http://localhost:5173

read -p "Press any key to stop the development server..."
echo "Stopping the development application"

cd ..

pkill -f "$python_exec -m fastapi run main.py"
pkill -f "node"
deactivate
