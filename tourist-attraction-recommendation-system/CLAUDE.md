# CLAUDE.md

## Project Overview
**Tourist Attraction Recommendation System** - Django + Vue 3 full-stack app.
- **Backend**: Django 5.2, DRF, MySQL, JWT.
- **Frontend**: Vue 3, Element Plus, ECharts, Tailwind CSS.
- **Docs**: See `prd.md`, `tech-stack.md`.

## Critical Rules

1. **Read memory-bank documents first** - `architecture.md`, `PRD.md`, `IMPLEMENTATION_PLAN.md` , `progress.md`
2. **API response format**: `{ code: 0, data: {...}, total: n }` for lists
3. **Use Chinese field names** - Follow patterns in PRD (e.g., `title`, `price`, `sales`, `shop`)
4. **Frontend must use frontend-design skill** - For all UI implementation

## Common Commands
### Backend
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
npm install
npm run dev
npm run build
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
