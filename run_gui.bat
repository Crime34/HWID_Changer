@echo off
title HWID Manager - Interface Graphique
color 0B

echo.
echo ========================================
echo    HWID Manager - Lancement GUI
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

REM Lancer l'interface graphique
echo Lancement de l'interface graphique...
echo.
python hwid_gui.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Une erreur s'est produite lors du lancement
    echo.
    pause
)
