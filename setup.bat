@echo off
python -m venv venv
call venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

cd web-ui
call npm install
call npm install @openapitools/openapi-generator-cli -g
call npm run generate-api
call npm run build
cd ..
pause
