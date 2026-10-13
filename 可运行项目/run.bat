@echo off
title 大学生生活管家 Python 系统
cd /d "%~dp0"

echo [INFO] 正在启动大学生生活管家系统...
python student_life_manager.py
if errorlevel 1 (
    echo [ERROR] 程序运行失败，请确认已安装 Python 3 并加入 PATH。
    pause
    exit /b 1
)

pause
