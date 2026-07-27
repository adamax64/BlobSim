@echo off
setlocal enabledelayedexpansion

title Blob Championship System - Deploy

set "scriptDir=%~dp0"
if "%scriptDir:~-1%"=="\" set "scriptDir=%scriptDir:~0,-1%"
cd /d "%scriptDir%"

set "branch=main"
if not defined DEPLOY_POLL_INTERVAL set "DEPLOY_POLL_INTERVAL=60"

echo Starting application...
call "%scriptDir%\start.bat"

echo Watching origin/%branch% for new commits every %DEPLOY_POLL_INTERVAL%s (Ctrl+C to stop watching; the backend keeps running)...

:watchLoop
timeout /t %DEPLOY_POLL_INTERVAL% /nobreak > nul

set "remoteCommit="
for /f "tokens=1" %%h in ('git ls-remote origin "refs/heads/%branch%"') do set "remoteCommit=%%h"

set "localCommit="
for /f "usebackq delims=" %%i in (`git rev-parse HEAD`) do set "localCommit=%%i"

if defined remoteCommit if not "!remoteCommit!"=="!localCommit!" (
    echo New commits detected on origin/%branch%, fetching and updating...
    git fetch origin %branch%
    git pull --ff-only origin %branch%
    if !errorlevel! equ 0 (
        echo Update complete, restarting application...
        call "%scriptDir%\start.bat"
    ) else (
        echo Failed to fast-forward to origin/%branch%. Resolve manually before the next check.
    )
)

goto watchLoop
