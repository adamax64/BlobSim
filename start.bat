python -m venv venv
call venv\Scripts\activate
echo Python virtual environment activated
start fastapi run main.py

cd web-ui
if not exist .\dist (
    echo dist folder not found. Run setup.bat to create them.
    exit
)

echo Startup complete
