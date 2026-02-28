@echo off
chcp 65001 > nul
echo ==========================================
echo   天猫潮玩数据采集 - 前端统计页面快速启动
echo ==========================================
echo.

REM 检查当前目录
if not exist "package.json" (
    echo ❌ 错误：请在frontend目录下运行此脚本
    pause
    exit /b 1
)

REM 检查依赖
echo 📦 检查依赖...
if not exist "node_modules" (
    echo ⚠️  node_modules目录不存在，正在安装依赖...
    call npm install
)

REM 检查关键依赖
echo 🔍 检查关键依赖...
call npm list echarts > nul 2>&1
if errorlevel 1 (
    echo ❌ echarts未安装
    set NEED_INSTALL=1
)

call npm list element-plus > nul 2>&1
if errorlevel 1 (
    echo ❌ element-plus未安装
    set NEED_INSTALL=1
)

if defined NEED_INSTALL (
    echo.
    echo 正在安装缺失的依赖...
    call npm install echarts element-plus
)

echo ✅ 依赖检查完成
echo.

REM 检查后端服务
echo 🔍 检查后端服务...
curl -s http://localhost:8000/api/products/statistics/dashboard/ > nul 2>&1
if errorlevel 1 (
    echo ⚠️  后端服务未响应
    echo.
    echo 请先启动后端服务：
    echo   cd backend
    echo   python manage.py runserver
    echo.
    set /p CONTINUE="是否继续启动前端？(y/n): "
    if /i not "%CONTINUE%"=="y" (
        exit /b 1
    )
) else (
    echo ✅ 后端服务正常运行
)

echo.
echo 🚀 启动前端开发服务器...
echo.
echo 访问地址：
echo   登录页: http://localhost:5173/login
echo   统计页: http://localhost:5173/admin/statistics
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 启动开发服务器
call npm run dev

pause
