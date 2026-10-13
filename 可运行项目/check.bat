@echo off
title 大学生生活管家 - 自检脚本
cd /d "%~dp0"

echo [INFO] 正在执行自检...
python main.py --check
if errorlevel 1 (
    echo [ERROR] 自检未通过。
    pause
    exit /b 1
)

echo [INFO] 自检完成。
pause
