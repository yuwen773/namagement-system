# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**问答信息采集系统** - A web-based Q&A data collection and management system targeting 360问答 (wenda.so.com). The system crawls Q&A data, stores it in MySQL, and provides a Vue-based admin interface for data management and visualization.

**Current Status**: Planning phase - project documentation complete, implementation not yet started.


## Critical Rules

1. **Read memory-bank documents first** - `architecture.md`, `PRD.md`, `IMPLEMENTATION_PLAN.md` , `progress.md`
2. **API response format**: `{ code: 0, data: {...}, total: n }` for lists
3. **Use Chinese field names** - Follow patterns in PRD (e.g., `title`, `price`, `sales`, `shop`)
4. **Frontend must use frontend-design skill** - For all UI implementation

## Tech Stack
reference [](memory-bank/tech-stack.md)

## Development Commands

### Backend (after implementation)
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Create admin account
python manage.py runserver          # Port 8000
```

### Frontend (after implementation)
```bash
cd frontend
npm install
npm run dev                        # Development server (port 5173)
npm run build                      # Production build
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