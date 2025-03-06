@echo off
python -m venv venv
call venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head

cd web-ui
call npm install
call npm run generate-api
call npm run build
cd ..
pause
