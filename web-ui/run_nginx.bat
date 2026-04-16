@echo off
setlocal enabledelayedexpansion

REM Get the directory of this script
set "scriptDir=%~dp0"
if "%scriptDir:~-1%"=="\" set "scriptDir=%scriptDir:~0,-1%"

REM Load environment variables from .env file
set "envFile=%scriptDir%\.env"
if exist "%envFile%" (
    for /f "tokens=1,* delims==" %%a in ('type "%envFile%"') do (
        set "%%a=%%b"
    )
)

REM Set defaults if not set
if not defined SERVER_NAME set "SERVER_NAME=localhost"
if not defined ROOT_PATH set "ROOT_PATH=%scriptDir%\dist"

REM Preprocess nginx config
set "configTemplate=%scriptDir%\nginx.conf"
set "configOutput=%scriptDir%\nginx_processed.conf"

if exist "%configTemplate%" (
    > "%configOutput%" (
        for /f "delims=" %%i in ('type "%configTemplate%"') do (
            set "line=%%i"
            REM Replace ${VAR} with environment variables
            set "line=!line:${SERVER_NAME}=%SERVER_NAME%!"
            set "line=!line:${ROOT_PATH}=%ROOT_PATH%!"
            REM Add more replacements as needed
            echo !line!
        )
    )
)

REM Run nginx with processed config
REM Note: Update the nginx path if it's not in your PATH
if defined NGINX_PATH (
    "%NGINX_PATH%\nginx.exe" -c "%configOutput%"
) else (
    nginx.exe -c "%configOutput%"
)