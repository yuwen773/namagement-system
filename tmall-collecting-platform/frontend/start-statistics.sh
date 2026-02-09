#!/bin/bash
# 前端统计页面快速启动脚本

echo "=========================================="
echo "  天猫潮玩数据采集 - 前端统计页面快速启动"
echo "=========================================="
echo ""

# 检查当前目录
if [ ! -f "package.json" ]; then
    echo "❌ 错误：请在frontend目录下运行此脚本"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules目录不存在，正在安装依赖..."
    npm install
fi

# 检查关键依赖
echo "🔍 检查关键依赖..."
missing_deps=0

if ! npm list echarts > /dev/null 2>&1; then
    echo "❌ echarts未安装"
    missing_deps=1
fi

if ! npm list element-plus > /dev/null 2>&1; then
    echo "❌ element-plus未安装"
    missing_deps=1
fi

if [ $missing_deps -eq 1 ]; then
    echo ""
    echo "正在安装缺失的依赖..."
    npm install echarts element-plus
fi

echo "✅ 依赖检查完成"
echo ""

# 检查后端服务
echo "🔍 检查后端服务..."
if curl -s http://localhost:8000/api/products/statistics/dashboard/ > /dev/null 2>&1; then
    echo "✅ 后端服务正常运行"
else
    echo "⚠️  后端服务未响应"
    echo ""
    echo "请先启动后端服务："
    echo "  cd backend"
    echo "  python manage.py runserver"
    echo ""
    read -p "是否继续启动前端？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 启动前端开发服务器..."
echo ""
echo "访问地址："
echo "  登录页: http://localhost:5173/login"
echo "  统计页: http://localhost:5173/admin/statistics"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动开发服务器
npm run dev
