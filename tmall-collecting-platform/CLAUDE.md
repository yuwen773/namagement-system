# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**天猫潮玩电商数据采集系统** - A data collection and visualization system for Tmall toy/collectible products.

| Aspect | Details |
|--------|---------|
| **Status** | Planning phase - implement per IMPLEMENTATION_PLAN.md |
| **Backend** | Django 5.2 + DRF + Celery + Redis |
| **Frontend** | Vue 3 + Element Plus + ECharts + Tailwind CSS |
| **Database** | MySQL 8.0 (`tmall_collecting` database) |
| **Key Feature** | Scrapy + Playwright crawler with async task queue |

## Critical Rules

1. **Read memory-bank documents first** - `architecture.md`, `PRD.md`, `IMPLEMENTATION_PLAN.md` , `progress.md`
2. **API response format**: `{ code: 0, data: {...}, total: n }` for lists
3. **Use Chinese field names** - Follow patterns in PRD (e.g., `title`, `price`, `sales`, `shop`)
4. **Frontend must use frontend-design skill** - For all UI implementation

## Common Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver        # Port 8000
python manage.py createsuperuser  # Create admin account
celery -A crawler worker -l info  # Start Celery worker for crawler tasks
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # Development server (port 5173)
npm run build                     # Production build
```

### Database
```bash
mysql -u root -p < sql/init_db.sql    # Initialize schema + test data
```
> 本地的 MySQL 数据库的相关配置：
> 1.Port:3307  
> 2.password : "yuwen123"
> Redis 相关配置：
> 1.Port:6379
> 2.没有密码

## API Conventions

### Response Format
```javascript
// Success
{ "code": 0, "data": {...}, "total": n }

// Error
{ "code": -1, "message": "错误描述" }

// Auth
{ "code": 0, "data": { "access_token": "...", "refresh_token": "...", "user": {...} } }
```

## Important Files

| File | Purpose |
|------|---------|
| `memory-bank/IMPLEMENTATION_PLAN.md` | Full implementation roadmap |
| `memory-bank/PRD.md` | Product requirements |
| `memory-bank/tech-stack.md` | Technology decisions |
| `memory-bank/progress.md` | Only track completed tasks |
| `memory-bank/architecture.md` |Only system architecture |
