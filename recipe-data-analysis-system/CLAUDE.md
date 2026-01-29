# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**菜谱数据分析系统** - A recipe data analysis platform with 10,000-20,000 recipe records, featuring data visualization dashboards, user behavior analytics, and administrative management capabilities.

## IMPORTANT:
### Always read memory-bank/@architecture.md before writing any code. Include entire database schema.
### Always read memory-bank/@PRD.md before writing any code.
### After adding a major feature or completing a milestone, update memory-bank/@architecture.md.


## Tech Stack

- **Backend**: Django 5.2 + Django REST Framework (DRF)
- **Frontend**: Vue 3 (Composition API) + Element Plus + Tailwind CSS
- **Database**: MySQL 8.0+
- **Visualization**: ECharts
- **State Management**: Pinia
- **Data Processing**: Pandas + NumPy
- **Authentication**: JWT

## Key Architecture

### Database Structure

The database (`recipe_analysis_db`) has these core tables:

- **users** / **user_profiles** - User accounts with role-based access (admin/user)
- **recipes** - Recipe main table with difficulty, taste, cooking_time, view_count, collect_count
- **categories** - Recipe categories with hierarchical structure (parent_id, level)
- **ingredients** - Ingredient library with categories
- **recipe_ingredients** - Many-to-many relationship between recipes and ingredients
- **recipe_steps** - Recipe cooking steps
- **user_favorites** - User favorites with unique constraint on (user_id, recipe_id)
- **user_behavior_logs** - Behavior tracking (login, view, search, collect, share) for analytics

Initialize database with: `mysql -u root -p < init.sql`

### Backend Structure (Django)

```
backend/
├── config/          # Django settings, main URLs, WSGI
├── utils/           # Common utilities (response, exceptions, pagination, constants)
├── accounts/        # User authentication module
├── [feature modules] # Feature-based apps (recipes, analytics, etc.)
└── manage.py
```

**Module naming**: Use lowercase, plural nouns (recipes, categories, analytics)

### Frontend Structure (Vue 3)

```
frontend/
├── src/
│   ├── components/  # Reusable components
│   ├── views/       # Page components
│   ├── api/         # API service layer
│   ├── stores/      # Pinia stores
│   └── router/      # Vue Router configuration
```

## Backend Development Standards

**All backend API development must follow** `backend-api-standards.md`. Key points:

### Response Format

All APIs return unified JSON structure:
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {}
}
```

Use `utils.response.ApiResponse`:
- `ApiResponse.success(data, message, code)` - Success response
- `ApiResponse.error(message, code, errors, data)` - Error response
- `ApiResponse.paginate(data, message)` - Paginated response

### Exception Handling

Use custom exceptions from `utils.exceptions`:
- `BusinessError` - Base business exception
- `ValidationError` - Parameter validation
- `NotFoundError` - Resource not found
- `PermissionDeniedError` - Permission denied
- `StateNotAllowedError` - State transition not allowed

### Pagination

Use `utils.pagination.StandardPagination`:
- Default page_size: 20
- Query params: `page`, `page_size` (max 100)

### ViewSet Pattern

Extend `BaseModelViewSet` when possible, override `get_serializer_class()` for different serializers:
```python
def get_serializer_class(self):
    if self.action == 'list':
        return self.serializer_list_class
    if self.action == 'create':
        return self.serializer_create_class
    return self.serializer_class
```

### Route Naming

All API routes prefixed with `/api/`:
```
/api/{module}/{resource}/{action}
```

Examples:
- `/api/recipes/` - Recipe list
- `/api/recipes/{id}/` - Recipe detail
- `/api/recipes/{id}/favorite/` - Custom action (kebab-case)

### Serializer Naming

| Type | Naming | Example |
|------|--------|---------|
| Base | Model + Serializer | `RecipeSerializer` |
| List | Model + ListSerializer | `RecipeListSerializer` |
| Create | Model + CreateSerializer | `RecipeCreateSerializer` |
| Update | Model + UpdateSerializer | `RecipeUpdateSerializer` |
| Action | Action + Serializer | `ApproveSerializer` |

## Common Development Commands

### Backend (Django)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Django shell
python manage.py shell
```

### Frontend (Vue 3)

```bash
# Install dependencies
npm install  # or pnpm install

# Development server
npm run dev

# Build for production
npm run build

# Type check (if using TypeScript)
npm run type-check
```

## Data Requirements

The project requires **10,000-20,000 recipe records** with images. Data can be:
1. Web scraped from recipe sites (下厨房, 美食杰)
2. Sourced from public recipe datasets

Each recipe must have:
- Basic info (name, difficulty, cooking_time, taste)
- Ingredients with quantities
- Cooking steps
- At least one cover image

### User Behavior Simulation

Admin dashboards require simulated user behavior data. Scripts in `data-scripts/` should:
- Generate 100+ mock users
- Simulate behaviors: login, search, view, collect, share
- Distribute activities over past 30 days with realistic patterns
- Update recipe view_count and collect_count accordingly

## Role-Based Access Control

### Regular Users
- Browse/search recipes
- View recipe details
- Favorite/unfavorite recipes
- View read-only data statistics (cuisine distribution, difficulty, etc.)

### Admins
- User management (view, ban/unban)
- Recipe CRUD operations
- Category and ingredient management
- Batch import recipes (CSV/JSON)
- Deep data analytics (cuisine trends, ingredient correlations, conversion rates)
- Dashboard with key metrics and user behavior analysis

## Data Visualization Focus

This project prioritizes **high-quality data visualization**:

**User-facing**:
- Cuisine distribution (pie chart)
- Difficulty statistics (bar chart)
- Taste preference analysis (radar chart)
- Ingredient frequency (word cloud or Top list)

**Admin dashboard**:
- Overview metrics cards (total recipes, users, today's new, active users)
- Trend charts (recipe growth, user growth, favorites)
- User behavior analytics:
  - Clickstream analysis (conversion paths)
  - Active users (DAU/WAU/MAU)
  - Login frequency distribution
  - Page duration heatmap

## Performance Requirements

- Search response: < 500ms
- Recipe detail load: < 1s
- Dashboard load: < 2s
- Support 100+ concurrent users

## Important Files

| File | Purpose |
|------|---------|
| `prd.md` | Product requirements document |
| `implementation-plan.md` | Step-by-step implementation guide (100+ steps) |
| `backend-api-standards.md` | Django backend development standards (strictly required) |
| `tech-stack.md` | Technology stack details |
| `init.sql` | Database initialization script |



## Development Workflow

1. Refer to `implementation-plan.md` for step-by-step guidance
2. Follow `backend-api-standards.md` for all backend API development
3. Use the database schema in `init.sql` as the single source of truth
4. Implement features following the 22-phase plan: initialization → database → data → auth → user module → admin module → simulation → optimization → testing
