python -m venv venv
call venv\Scripts\activate
echo Python virtual environment activated
start fastapi run main.py

cd web-ui
if not exist .\node_modules (
    echo Node modules not found. Run setup.bat to create them.
    exit
)
start "npm" cmd /c "npm run start"
start http://localhost:5173

echo Startup complete
