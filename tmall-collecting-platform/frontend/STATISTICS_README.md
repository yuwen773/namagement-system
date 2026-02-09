# 📊 数据统计展示页面 - 快速开始

## ✨ 新功能

全新打造的数据分析仪表板现已上线！访问 `/admin/statistics` 查看丰富的数据可视化分析。

## 🚀 快速启动

### Windows用户

双击运行：
```
start-statistics.bat
```

### Mac/Linux用户

```bash
chmod +x start-statistics.sh
./start-statistics.sh
```

### 手动启动

```bash
npm install  # 首次运行需要
npm run dev
```

然后访问：
- 登录页: http://localhost:5173/login
- 统计页: http://localhost:5173/admin/statistics

## 📊 功能特性

### 数据展示
- ✅ 6个关键指标卡片
- ✅ 价格分布饼图
- ✅ 销量分布柱状图
- ✅ 品牌分析雷达图
- ✅ 地区分布图
- ✅ 价格-销量关联分析
- ✅ Top商品排行榜
- ✅ 市场洞察分析

### 交互功能
- 🔍 按品牌/地区筛选数据
- 🔄 手动或自动刷新
- 📊 销量/价格排序切换
- ✨ 流畅的动画效果

### 设计特色
- 🌙 深色科技风格
- 🎨 丰富的渐变和光效
- 📱 完美的响应式布局

## 📖 文档

详细文档请查看：
- [使用指南](../docs/frontend-statistics-guide.md)
- [API文档](../docs/statistics-api-reference.md)
- [快速指南](../docs/statistics-quick-guide.md)

## 🐛 常见问题

### 图表不显示？
```bash
npm install echarts element-plus
```

### 后端连接失败？
确保后端服务已启动：
```bash
cd backend
python manage.py runserver
```

### 样式不正确？
清除浏览器缓存或使用隐私模式访问

## 💡 提示

- 页面每5分钟自动刷新数据
- 点击"刷新数据"按钮手动刷新
- 使用筛选功能查看特定数据
- 切换排序方式查看不同排行

---

**需要帮助？** 查看 `docs/` 目录下的详细文档。
