@echo off
cd /d "%~dp0"
echo Starting OpenWrt Manager Backend...
python main.py
if %errorlevel% neq 0 (
    echo Backend crashed with code %errorlevel%
    pause
)
