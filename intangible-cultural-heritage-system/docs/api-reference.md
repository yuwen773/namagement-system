# Intangible Cultural Heritage System API Reference

## 1. Overview

- Base URL: `/api/v1`
- Auth scheme: `Bearer <access_token>` in `Authorization` header
- API style: Django REST Framework + unified response envelope
- Content type: `application/json` unless noted

## 2. Global Conventions

### 2.1 Unified Response Envelope

All successful and failed responses use:

```json
{
  "code": 0,
  "message": "text",
  "data": {},
  "total": 0
}
```

- `code`: `0` means success, non-zero means failure (current implementation uses `1`)
- `message`: localized message text (may vary by endpoint)
- `data`: payload object/array/null
- `total`: only returned by list-like endpoints that provide totals

### 2.2 Error Format

Standard error envelope:

```json
{
  "code": 1,
  "message": "error reason",
  "data": null
}
```

Common HTTP status codes:

- `400`: validation or business failure
- `401`: unauthenticated or invalid credentials/token
- `403`: authenticated but not allowed
- `404`: resource not found
- `500`: unhandled internal error

### 2.3 Authentication and Authorization

- Default permission is authenticated access.
- `POST /auth/login` and `POST /auth/refresh` are public.
- Most CRUD endpoints use `IsAdminOrReadOnly`:
  - `GET`: any authenticated user
  - `POST/PUT/PATCH/DELETE`: admin only
- Admin check is: `is_superuser` OR profile role `admin`.

### 2.4 Pagination

List endpoints use page-number pagination with:

- default page size: `20`
- query param: `page` (integer, optional)
- `page_size` override: not supported

## 3. Auth APIs

Prefix: `/api/v1/auth`

> Note: these routes accept both with and without trailing slash (`/`).

### 3.1 Login

- Method/Path: `POST /api/v1/auth/login/`
- Auth: none

Request body:

```json
{
  "username": "admin",
  "password": "password123"
}
```

Success `200`:

```json
{
  "code": 0,
  "message": "Login success",
  "data": {
    "access": "jwt-access-token",
    "refresh": "jwt-refresh-token",
    "user": {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
}
```

Failure `401`: invalid username/password or inactive account.

### 3.2 Refresh Access Token

- Method/Path: `POST /api/v1/auth/refresh/`
- Auth: none

Request body:

```json
{
  "refresh": "jwt-refresh-token"
}
```

Success `200`:

```json
{
  "code": 0,
  "message": "Refresh success",
  "data": {
    "access": "new-jwt-access-token"
  }
}
```

Failure `401`: invalid/expired refresh token.

### 3.3 Logout

- Method/Path: `POST /api/v1/auth/logout/`
- Auth: Bearer access token required

Request body:

```json
{
  "refresh": "jwt-refresh-token"
}
```

Success `200`: refresh token is blacklisted.

Failure:

- `400`: invalid refresh token
- `403`: refresh token does not belong to current user

### 3.4 Current User Profile

- Method/Path: `GET /api/v1/auth/me/`
- Auth: Bearer access token required

Success `200`:

```json
{
  "code": 0,
  "message": "Fetched successfully",
  "data": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

## 4. Heritage Item APIs

Prefix: `/api/v1/heritage`

### 4.1 List Heritage Items

- Method/Path: `GET /api/v1/heritage/`
- Auth: authenticated
- Query params:
  - `page`: integer, optional
  - `category`: category id, optional
  - `level`: `national|provincial|city_county`, optional
  - `region`: region id, optional
  - `name`: fuzzy match on name, optional

Response item fields:

- `id`, `name`, `level`, `area`, `protection_unit`, `description`, `created_at`, `updated_at`
- `category` (nested): `id`, `name`, `code`, `level`
- `region` (nested): `id`, `country_code`, `country_name`, `continent`

Includes `total`.

### 4.2 Create Heritage Item

- Method/Path: `POST /api/v1/heritage/`
- Auth: admin

Request body:

```json
{
  "name": "Example Heritage",
  "category": 1,
  "level": "national",
  "region": 1,
  "area": "Optional area",
  "protection_unit": "Optional unit",
  "description": "Optional description"
}
```

Success `201`: returns read-model payload (nested `category` and `region`).

### 4.3 Retrieve Heritage Item

- Method/Path: `GET /api/v1/heritage/{id}/`
- Auth: authenticated

### 4.4 Update Heritage Item

- Method/Path:
  - `PUT /api/v1/heritage/{id}/`
  - `PATCH /api/v1/heritage/{id}/`
- Auth: admin
- Body uses same fields as create.

### 4.5 Delete Heritage Item

- Method/Path: `DELETE /api/v1/heritage/{id}/`
- Auth: admin
- Success `200`: `data` is `null`.

## 5. Inheritor APIs

Prefix: `/api/v1/inheritors`

### 5.1 List Inheritors

- Method/Path: `GET /api/v1/inheritors/`
- Auth: authenticated
- Query params:
  - `page`: integer, optional
  - `heritage_item`: heritage item id, optional
  - `level`: `national|provincial|city_county`, optional
  - `region`: region id, optional
  - `name`: fuzzy match on name, optional

Response item fields:

- `id`, `name`, `gender`, `level`, `area`, `description`, `created_at`, `updated_at`
- `heritage_item` (nested): `id`, `name`, `level`
- `region` (nested): `id`, `country_code`, `country_name`, `continent`

Includes `total`.

### 5.2 Create Inheritor

- Method/Path: `POST /api/v1/inheritors/`
- Auth: admin

Request body:

```json
{
  "name": "Example Inheritor",
  "heritage_item": 1,
  "region": 1,
  "gender": "male",
  "level": "national",
  "area": "Optional area",
  "description": "Optional description"
}
```

Notes:

- `gender` optional: `male|female|other`
- `level` optional: `national|provincial|city_county`
- unique constraint on `(heritage_item, name)`

### 5.3 Retrieve / Update / Delete Inheritor

- `GET /api/v1/inheritors/{id}/` (authenticated)
- `PUT /api/v1/inheritors/{id}/` (admin)
- `PATCH /api/v1/inheritors/{id}/` (admin)
- `DELETE /api/v1/inheritors/{id}/` (admin)

## 6. Category APIs

Prefix: `/api/v1/categories`

### 6.1 List Categories

- Method/Path: `GET /api/v1/categories/`
- Auth: authenticated
- Query params:
  - `page`: integer, optional
  - `level`: `national|provincial|city_county`, optional
  - `parent_id`: category id, optional
    - if empty string / `null` / `none`, filters root categories (`parent is null`)
  - `name`: fuzzy match on category name, optional

Response item fields:

- `id`, `name`, `code`, `level`, `parent_id`, `created_at`, `updated_at`
- `parent` nested brief object or `null`

Includes `total`.

### 6.2 Category Tree

- Method/Path: `GET /api/v1/categories/tree/`
- Auth: authenticated

Response `data` is hierarchical nodes:

```json
[
  {
    "id": 1,
    "name": "Category",
    "code": "CAT001",
    "level": "national",
    "parent_id": null,
    "children": []
  }
]
```

Includes `total` (count of all category records).

### 6.3 Create / Retrieve / Update / Delete Category

- `POST /api/v1/categories/` (admin)
  - body: `name`, `code`, `level`, `parent` (optional)
- `GET /api/v1/categories/{id}/` (authenticated)
- `PUT /api/v1/categories/{id}/` (admin)
- `PATCH /api/v1/categories/{id}/` (admin)
- `DELETE /api/v1/categories/{id}/` (admin)

## 7. Region APIs

Prefix: `/api/v1/regions`

### 7.1 List Regions

- Method/Path: `GET /api/v1/regions/`
- Auth: authenticated
- Query params:
  - `page`: integer, optional
  - `search`: matches `country_name` (icontains) OR `country_code` (icontains)

Response item fields:

- `id`, `country_code`, `country_name`, `continent`, `latitude`, `longitude`

Includes `total`.

### 7.2 Create / Retrieve / Update / Delete Region

- `POST /api/v1/regions/` (admin)
  - body fields: `country_code`, `country_name`, `continent`, `latitude`, `longitude`
  - `continent` optional; others required
- `GET /api/v1/regions/{id}/` (authenticated)
- `PUT /api/v1/regions/{id}/` (admin)
- `PATCH /api/v1/regions/{id}/` (admin)
- `DELETE /api/v1/regions/{id}/` (admin)

## 8. Dashboard APIs

Prefix: `/api/v1/dashboard`

> Note: these routes accept both with and without trailing slash (`/`).

### 8.1 Overview

- Method/Path: `GET /api/v1/dashboard/overview/`
- Auth: authenticated

Response `data`:

- `heritage_count`
- `inheritor_count`
- `category_count`
- `country_count` (distinct region count referenced by heritage items)

### 8.2 Map Distribution

- Method/Path: `GET /api/v1/dashboard/map-distribution/`
- Auth: authenticated
- Query params:
  - `category` OR `category_id` (category id, optional)

Response item fields:

- `country_code`, `country_name`, `longitude`, `latitude`
- `heritage_count` (distinct heritage items in region)
- `inheritor_count` (distinct inheritors in region)

Only countries with at least one heritage or inheritor are returned.

### 8.3 Category Distribution

- Method/Path: `GET /api/v1/dashboard/category-distribution/`
- Auth: authenticated

Response item fields:

- `category_name`
- `heritage_count`
- `percentage` (float, rounded to 2 decimals, adjusted so non-zero totals sum to 100.00)

Sorted by `heritage_count` desc, then category name asc.

### 8.4 Country Ranking

- Method/Path: `GET /api/v1/dashboard/country-ranking/`
- Auth: authenticated
- Query params:
  - `limit` optional (default `20`, max `100`, invalid/non-positive resets to `20`)

Response item fields:

- `rank` (1-based)
- `country_name`
- `heritage_count`

Only countries with `heritage_count > 0` are returned.

## 9. Not Exposed as HTTP API (Current State)

- The `apps/importer` module currently provides data import services/tests/models but no registered HTTP endpoints in `heritage_system/urls.py`.
- If importer APIs are needed later, they must be added to URL routing and documented in a new version of this file.

## 10. Quick cURL Examples

### 10.1 Login

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

### 10.2 List Heritage Items

```bash
curl "http://127.0.0.1:8000/api/v1/heritage/?page=1&name=opera" \
  -H "Authorization: Bearer <access_token>"
```

### 10.3 Dashboard Overview

```bash
curl "http://127.0.0.1:8000/api/v1/dashboard/overview/" \
  -H "Authorization: Bearer <access_token>"
```
