@echo off
setlocal ENABLEDELAYEDEXPANSION

REM --- Paths and constants --------------------------------------------------
set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "REQUIREMENTS=requirements.txt"
set "FLASK_APP=app:create_app"
set "FLASK_RUN_PORT=5000"
set "FLASK_RUN_HOST=0.0.0.0"

REM --- Ensure Python launcher is available ----------------------------------
where py >NUL 2>&1
if errorlevel 1 (
    echo [ERROR] Python launcher 'py' not found on PATH.
    echo Install Python 3 (https://www.python.org/downloads/) and ensure ^"py.exe^" is available.
    exit /b 1
)

REM --- Ensure virtualenv module is installed --------------------------------
py -m virtualenv --version >NUL 2>&1
if errorlevel 1 (
    echo [INFO] Installing virtualenv helper...
    py -m pip install --upgrade pip
    if errorlevel 1 (
        echo [ERROR] Failed to upgrade pip.
        exit /b 1
    )
    py -m pip install virtualenv
    if errorlevel 1 (
        echo [ERROR] Failed to install virtualenv package.
        exit /b 1
    )
)

REM --- Create virtual environment if missing --------------------------------
if not exist "%VENV_PY%" (
    echo [INFO] Creating virtual environment in %VENV_DIR% ...
    py -m venv %VENV_DIR%
    if errorlevel 1 (
        echo [ERROR] Unable to create virtual environment.
        exit /b 1
    )
) else (
    echo [INFO] Reusing existing virtual environment.
)

REM --- Activate environment --------------------------------------------------
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

REM --- Install dependencies --------------------------------------------------
if exist "%REQUIREMENTS%" (
    echo [INFO] Installing Python dependencies from %REQUIREMENTS% ...
    pip install --upgrade pip >NUL
    pip install -r "%REQUIREMENTS%"
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        exit /b 1
    )
) else (
    echo [WARN] requirements.txt not found. Skipping dependency install.
)

REM --- Detect preferred IPv4 for LAN access ---------------------------------
set "LOCAL_IP="
for /f "tokens=2 delims=:" %%I in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (
    set "LOCAL_IP=%%I"
)
if defined LOCAL_IP (
    set "LOCAL_IP=!LOCAL_IP: =!"
)

REM --- Launch Flask dev server ----------------------------------------------
set "FLASK_APP=%FLASK_APP%"
set "FLASK_RUN_PORT=%FLASK_RUN_PORT%"
set "FLASK_RUN_HOST=%FLASK_RUN_HOST%"

echo.
echo [INFO] Preparing database (init + seed)...
python -m flask --app %FLASK_APP% init-db
if errorlevel 1 (
    echo [ERROR] Failed to initialize database.
    exit /b 1
)
python -m flask --app %FLASK_APP% seed-data
if errorlevel 1 (
    echo [ERROR] Failed to seed database.
    exit /b 1
)

echo.
echo [INFO] Starting Vashu Hotels dev server...
echo [INFO] Local  URL: http://localhost:%FLASK_RUN_PORT%
if defined LOCAL_IP (
    echo [INFO] LAN URL:   http://!LOCAL_IP!:%FLASK_RUN_PORT%
    echo [INFO] Ensure both devices are on the same network to use the LAN URL.
)
echo.
python -m flask run --host=%FLASK_RUN_HOST% --port=%FLASK_RUN_PORT% --debug

endlocal
