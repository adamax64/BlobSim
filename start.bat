@echo off
setlocal enabledelayedexpansion

set "scriptDir=%~dp0"
if "%scriptDir:~-1%"=="\" set "scriptDir=%scriptDir:~0,-1%"
cd /d "%scriptDir%"

set "pidFile=%scriptDir%\.backend.pid"

if exist "%pidFile%" (
    set "oldPid="
    set /p oldPid=<"%pidFile%"
    if defined oldPid (
        tasklist /fi "PID eq !oldPid!" 2>nul | find "!oldPid!" >nul
        if not errorlevel 1 (
            echo Stopping previous backend process ^(PID !oldPid!^)...
            taskkill /pid !oldPid! /t /f >nul 2>&1
        )
    )
    del "%pidFile%" >nul 2>&1
)

if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
echo Python virtual environment activated

python.exe -m pip install --upgrade pip
pip install -r requirements.txt

cd web-ui
call pnpm install

echo Building frontend...
call pnpm add -g @openapitools/openapi-generator-cli
call pnpm run generate-api
call pnpm run build

cd ..

echo Setup complete
echo Starting application...

powershell -NoProfile -Command "(Start-Process -FilePath python -ArgumentList '-m fastapi run main.py' -WindowStyle Normal -PassThru).Id" > "%pidFile%"
set /p backendPid=<"%pidFile%"

echo Startup complete, backend PID !backendPid!
