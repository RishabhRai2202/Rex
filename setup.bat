@echo off
echo Checking Python installation...
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed! Please install Python 3 and try again.
    exit /b 1
)

echo Creating virtual environment...
python -m venv myenv

echo Activating virtual environment...
call myenv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete! Run "start.bat" to execute the project.
pause