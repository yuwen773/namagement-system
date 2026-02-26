# Architecture

## 技术栈
```
Vue3 + Django + DRF + MySQL
```

## 约定
| 类型 | 规则 |
|------|------|
| 响应 | `{ code: 0, data: {...}, total?: n }` |
| 认证 | JWT Bearer |
| 权限 | admin 写 / user 读 |

## 模型
```
Category → HeritageItem → Inheritor
                ↑           ↑
                Region ──────┘
```

## 结构
```
backend/apps/ → frontend/src/
```
