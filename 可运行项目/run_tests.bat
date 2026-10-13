@echo off
title 大学生生活管家 - 测试脚本
cd /d "%~dp0"

echo [INFO] 正在执行语法检查...
python -m py_compile student_life_manager.py
if errorlevel 1 (
    echo [ERROR] 主程序语法检查失败。
    pause
    exit /b 1
)

echo [INFO] 语法检查通过。
echo [INFO] 正在执行测试样例...
python test_student_life_manager.py
if errorlevel 1 (
    echo [ERROR] 测试未全部通过。
    pause
    exit /b 1
)

echo [INFO] 测试执行完成。
pause
