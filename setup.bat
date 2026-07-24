@echo off
python -m venv venv
call venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

cd web-ui
call pnpm install
call pnpm add -g @openapitools/openapi-generator-cli
call pnpm run generate-api
call pnpm run build
cd ..
pause
