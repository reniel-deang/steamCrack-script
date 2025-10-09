@echo off
setlocal

REM Root folder where this .bat lives (ends with a backslash)
set "ROOT=%~dp0"

REM Virtualenv folder (relative to ROOT)
set "VENV=%ROOT%.steamCrack"

REM Path to activation script
set "ACTIVATE=%VENV%\Scripts\activate.bat"

REM Create venv if it does not exist
if not exist "%ACTIVATE%" (
    echo Creating virtual environment in "%VENV%" ...
    py -m venv "%VENV%" || (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate venv
echo Activating virtual environment...
call "%ACTIVATE%" || (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Upgrade pip in venv
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements if file exists
if exist "%ROOT%requirements.txt" (
    echo Installing requirements from "%ROOT%requirements.txt" ...
    python -m pip install -r "%ROOT%requirements.txt" || (
        echo pip install failed.
        pause
        exit /b 1
    )
) else (
    echo requirements.txt not found — skipping pip install.
)

REM Run the Python script (forward any args passed to the .bat)
echo Running script...
python "%ROOT%steamcrack.py" %* 
echo Script finished with exit code %errorlevel%.

pause
endlocal