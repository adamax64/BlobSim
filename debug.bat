@echo off

title Blob Championship System - Development

if not exist .\venv (
    echo Python virtual environment not found. Run setup.bat to create it.
    pause
    exit
) 

python -m venv venv
call venv\Scripts\activate
echo Python virtual environment activated
set MODE=dev
start fastapi dev main.py

cd web-ui
if not exist .\node_modules (
    echo Node modules not found. Run setup.bat to create them.
    pause
    exit
)
start "npm" cmd /c "npm run dev"
start http://localhost:3001

echo Press any key to stop the development server
pause > nul
echo Stopping the development application

cd ..

taskkill /IM "python.exe" /F
taskkill /IM "node.exe" /F
call venv\Scripts\deactivate.bat
exit
