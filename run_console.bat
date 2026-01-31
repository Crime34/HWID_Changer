@echo off
title HWID Manager - Mode Console
color 0A

echo.
echo ========================================
echo    HWID Manager - Mode Console
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Telechargez Python depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Lancer le mode console
python hwid_manager.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Une erreur s'est produite lors du lancement
    echo.
)

pause
