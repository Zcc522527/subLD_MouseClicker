@echo off
chcp 65001 >nul
title subLD - 鼠标连点器

echo ========================================
echo   subLD 鼠标连点器启动脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [信息] Python环境检测成功
echo.

:: 检查依赖
echo [信息] 正在检查依赖包...
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo [警告] 缺少依赖包，正在安装...
    pip install -r requirements.txt
)

echo [信息] 依赖检查完成
echo.

:: 启动程序
echo [信息] 启动 subLD 鼠标连点器...
echo.
python mouse_clicker_app.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出错
    pause
)
