# 前端对接接口文档（可直接联调）

## 1. 快速开始

- Base URL：`http://127.0.0.1:8000/api/v1`
- 认证方式：`Authorization: Bearer <access_token>`
- 默认要求登录（除 `auth/login`、`auth/refresh`）
- 建议请求路径统一使用带尾斜杠版本（例如 `/heritage/`）

标准响应结构：

```ts
export interface ApiResponse<T> {
  code: number;        // 0 成功，非 0 失败
  message: string;     // 提示信息
  data: T;             // 业务数据
  total?: number;      // 列表接口返回
}
```

## 2. 前端请求封装建议（Axios）

```ts
import axios from "axios";

const request = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  timeout: 10000,
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

request.interceptors.response.use(
  (resp) => {
    const payload = resp.data as ApiResponse<unknown>;
    if (payload.code === 0) return payload;
    return Promise.reject(payload);
  },
  (error) => {
    if (error?.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
    return Promise.reject(error);
  }
);

export default request;
```

## 3. 全局类型

```ts
export type Id = number;

export type Level = "national" | "provincial" | "city_county";
export type Gender = "male" | "female" | "other";
export type UserRole = "admin" | "user";

export interface PageQuery {
  page?: number;
}
```

## 4. 认证模块（`/auth`）

## 4.1 登录

- `POST /auth/login/`
- 请求：

```ts
export interface LoginBody {
  username: string;
  password: string;
}

export interface LoginData {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    role: UserRole;
  };
}
```

## 4.2 刷新 token

- `POST /auth/refresh/`

```ts
export interface RefreshBody {
  refresh: string;
}

export interface RefreshData {
  access: string;
}
```

## 4.3 登出

- `POST /auth/logout/`

```ts
export interface LogoutBody {
  refresh: string;
}
```

## 4.4 当前用户信息

- `GET /auth/me/`

```ts
export interface MeData {
  id: number;
  username: string;
  role: UserRole;
}
```

## 5. 非遗项目模块（`/heritage`）

## 5.1 类型

```ts
export interface CategoryBrief {
  id: number;
  name: string;
  code: string;
  level: Level;
}

export interface RegionBrief {
  id: number;
  country_code: string;
  country_name: string;
  continent: string;
}

export interface HeritageItem {
  id: number;
  name: string;
  category: CategoryBrief;
  level: Level;
  region: RegionBrief;
  area: string;
  protection_unit: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface HeritageUpsertBody {
  name: string;
  category: Id;
  level: Level;
  region: Id;
  area?: string;
  protection_unit?: string;
  description?: string;
}
```

## 5.2 接口

- `GET /heritage/`（登录可读）
  - query：`page`、`category`、`level`、`region`、`name`
- `GET /heritage/{id}/`（登录可读）
- `POST /heritage/`（仅 admin）
- `PUT /heritage/{id}/`（仅 admin）
- `PATCH /heritage/{id}/`（仅 admin）
- `DELETE /heritage/{id}/`（仅 admin，返回 `data: null`）

## 6. 传承人模块（`/inheritors`）

## 6.1 类型

```ts
export interface InheritorHeritageBrief {
  id: number;
  name: string;
  level: Level;
}

export interface Inheritor {
  id: number;
  name: string;
  heritage_item: InheritorHeritageBrief;
  region: RegionBrief;
  gender: "" | Gender;
  level: "" | Level;
  area: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface InheritorUpsertBody {
  name: string;
  heritage_item: Id;
  region: Id;
  gender?: Gender | "";
  level?: Level | "";
  area?: string;
  description?: string;
}
```

## 6.2 接口

- `GET /inheritors/`（登录可读）
  - query：`page`、`heritage_item`、`level`、`region`、`name`
- `GET /inheritors/{id}/`（登录可读）
- `POST /inheritors/`（仅 admin）
- `PUT /inheritors/{id}/`（仅 admin）
- `PATCH /inheritors/{id}/`（仅 admin）
- `DELETE /inheritors/{id}/`（仅 admin）

约束：同一 `heritage_item` 下 `name` 唯一。

## 7. 分类模块（`/categories`）

## 7.1 类型

```ts
export interface CategoryParent {
  id: number;
  name: string;
  code: string;
  level: Level;
}

export interface CategoryItem {
  id: number;
  name: string;
  code: string;
  level: Level;
  parent: CategoryParent | null;
  parent_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface CategoryUpsertBody {
  name: string;
  code: string;
  level: Level;
  parent?: number | null;
}

export interface CategoryTreeNode {
  id: number;
  name: string;
  code: string;
  level: Level;
  parent_id: number | null;
  children: CategoryTreeNode[];
}
```

## 7.2 接口

- `GET /categories/`（登录可读）
  - query：`page`、`level`、`parent_id`、`name`
  - `parent_id` 传 `null`/`none`/空字符串可筛根节点
- `GET /categories/tree/`（登录可读）
- `GET /categories/{id}/`（登录可读）
- `POST /categories/`（仅 admin）
- `PUT /categories/{id}/`（仅 admin）
- `PATCH /categories/{id}/`（仅 admin）
- `DELETE /categories/{id}/`（仅 admin）

## 8. 地区模块（`/regions`）

## 8.1 类型

```ts
export interface RegionItem {
  id: number;
  country_code: string;
  country_name: string;
  continent: string;
  latitude: string | number;
  longitude: string | number;
}

export interface RegionUpsertBody {
  country_code: string;
  country_name: string;
  continent?: string;
  latitude: string | number;
  longitude: string | number;
}
```

## 8.2 接口

- `GET /regions/`（登录可读）
  - query：`page`、`search`
- `GET /regions/{id}/`（登录可读）
- `POST /regions/`（仅 admin）
- `PUT /regions/{id}/`（仅 admin）
- `PATCH /regions/{id}/`（仅 admin）
- `DELETE /regions/{id}/`（仅 admin）

## 9. 大盘模块（`/dashboard`）

## 9.1 类型

```ts
export interface DashboardOverview {
  heritage_count: number;
  inheritor_count: number;
  category_count: number;
  country_count: number;
}

export interface DashboardMapItem {
  country_code: string;
  country_name: string;
  longitude: number;
  latitude: number;
  heritage_count: number;
  inheritor_count: number;
}

export interface DashboardCategoryItem {
  category_name: string;
  heritage_count: number;
  percentage: number;
}

export interface DashboardCountryRankItem {
  rank: number;
  country_name: string;
  heritage_count: number;
}
```

## 9.2 接口

- `GET /dashboard/overview/`
- `GET /dashboard/map-distribution/`
  - query：`category` 或 `category_id`
- `GET /dashboard/category-distribution/`
- `GET /dashboard/country-ranking/`
  - query：`limit`（默认 20，最大 100）

以上均要求登录。

## 10. 可直接复制的 API 文件示例

```ts
// src/api/heritage.ts
import request from "./request";

export const listHeritage = (params?: {
  page?: number;
  category?: number;
  level?: Level;
  region?: number;
  name?: string;
}) => request.get<ApiResponse<HeritageItem[]>>("/heritage/", { params });

export const getHeritage = (id: number) =>
  request.get<ApiResponse<HeritageItem>>(`/heritage/${id}/`);

export const createHeritage = (data: HeritageUpsertBody) =>
  request.post<ApiResponse<HeritageItem>>("/heritage/", data);

export const updateHeritage = (id: number, data: Partial<HeritageUpsertBody>) =>
  request.patch<ApiResponse<HeritageItem>>(`/heritage/${id}/`, data);

export const deleteHeritage = (id: number) =>
  request.delete<ApiResponse<null>>(`/heritage/${id}/`);
```

## 11. 联调检查清单

- 登录后 `access_token` 注入 Header 是否生效
- 列表页是否正确使用 `total` 驱动分页
- 普通用户写操作是否收到 `403`
- token 过期后是否进入刷新或重新登录流程
- `level`、`gender` 枚举值是否严格按文档发送

## 12. 当前未开放 HTTP 接口

- `apps/importer` 目前只有服务层与模型，没有注册 API 路由；前端无需对接。
