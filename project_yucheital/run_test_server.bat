@echo off
chcp 65001 >nul
rem ==============================================================
rem  Yucheital - test (mock) AI server + frontend
rem  Double-click this file. Browser opens http://127.0.0.1:8000
rem  Option: run_test_server.bat --require-login   (login required)
rem ==============================================================
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo [ERROR] Python not found. Install Python 3.10+ from https://www.python.org
        pause
        exit /b 1
    )
    set PY=py -3
) else (
    set PY=python
)

%PY% -c "import PIL, numpy" >nul 2>nul
if errorlevel 1 (
    echo Installing pillow, numpy ...
    %PY% -m pip install pillow numpy
)

%PY% "dev_server\mock_server.py" %*
pause
