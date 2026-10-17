@echo off
title AUTOCOR - Sistema de Gestion
cd /d "%~dp0"
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al ejecutar el programa.
    pause
)
