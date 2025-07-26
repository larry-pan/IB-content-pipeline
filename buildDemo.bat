@echo off
setlocal enabledelayedexpansion

REM "Builds demo.exe"

set FRONTEND_DIR=frontend
set BACKEND_DIR=backend
set STATIC_DIR=%BACKEND_DIR%\static
set DIST_DIR=%FRONTEND_DIR%\dist
set MAIN_SCRIPT=main.py
set EXE_NAME=demo.exe

echo.
echo =========================================
echo 1. Building frontend...
echo =========================================
cd /d %FRONTEND_DIR%
call npm i
call npm run build
if errorlevel 1 (
    echo frontend build failed.
    exit /b 1
)
cd ..


rmdir /s /q "%STATIC_DIR%" 2>nul
mkdir "%STATIC_DIR%"
xcopy /E /I /Y "%DIST_DIR%\*" "%STATIC_DIR%\"

echo.
echo =========================================
echo 3. Building exe...
echo =========================================
call .\venv\Scripts\activate.bat
if errorlevel 1 (
    echo please make a venv in the project root and install the requirements.txt in the backend folder.
    exit /b 1
)
cd /d %BACKEND_DIR%
pyinstaller --noconfirm --onefile --add-data "static;static" --add-data ".env;." --name %EXE_NAME% %MAIN_SCRIPT%
if errorlevel 1 (
    echo backend bundle failed.
    exit /b 1
)
cd ..

echo.
echo =========================================
echo Build complete
echo Output exe: backend\dist\%EXE_NAME%
echo =========================================

endlocal
pause