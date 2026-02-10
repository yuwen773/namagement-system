# CLAUDE.md

## Project Overview
**电影票房预测与可视化系统**
A full-stack web application for movie box office prediction using Django 5.2 + Vue 3.

## Critical Rules

1. **Read memory-bank documents first** - `architecture.md`, `PRD.md`, `IMPLEMENTATION_PLAN.md` , `progress.md`
2. **API response format**: `{ code: 0, data: {...}, total: n }` for lists
3. **Use Chinese field names** - Follow patterns in PRD (e.g., `title`, `price`, `sales`, `shop`)
4. **Frontend must use frontend-design skill** - For all UI implementation

## Commands

### Backend (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

## Architecture
```
movie-prediction-visualization-system/
├── backend/                   # Django 5.2 + DRF
│   ├── movie_prediction/      # Settings
│   ├── accounts/              # Auth & Users
│   ├── movies/                # Movies & Types
│   ├── cinemas/               # Cinemas & Regions
│   ├── boxoffice/             # Box Office Data
│   ├── prediction/            # Analysis Algorithms
│   └── visualization/         # Chart Data APIs
└── frontend/                  # Vue 3 + Vite
    ├── src/
    │   ├── api/               # API Integration
    │   ├── views/             # Pages (Admin & User)
    │   └── components/        # Reusable Components
```

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