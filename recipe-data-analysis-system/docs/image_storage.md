# 图片存储方案说明

> 更新日期: 2026-01-30
> 状态: ✅ 本地存储方案已配置完成

---

## 存储方案选择

**当前方案**: 本地文件系统存储

**选择理由**:
- 开发阶段简单快速
- 无需额外云服务配置
- 适合中小规模项目（20,000 张图片）

**未来扩展**: 可切换到云存储（阿里云 OSS、AWS S3 等）

---

## 目录结构

```
backend/
└── media/              # 媒体文件根目录
    ├── recipes/         # 菜谱成品图片
    ├── avatars/         # 用户头像
    └── temp/            # 临时上传目录
```

---

## Django 配置

### settings.py

```python
# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**说明**:
- `MEDIA_URL`: 访问媒体文件的 URL 前缀
- `MEDIA_ROOT`: 媒体文件在文件系统中的存储路径

### urls.py

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**说明**:
- 仅在开发环境（DEBUG=True）下提供静态文件服务
- 生产环境需要使用 Web 服务器（Nginx/Apache）处理媒体文件

---

## 文件命名规则

### 菜谱图片

**命名格式**: `{recipe_id}_{timestamp}.{ext}`

**示例**:
- `1_1706582400.jpg`
- `12345_1706582401.png`

**规则**:
- 使用菜谱 ID 作为前缀
- 使用时间戳防止冲突
- 支持的格式：`jpg`, `jpeg`, `png`, `webp`

### 用户头像

**命名格式**: `user_{user_id}_{timestamp}.{ext}`

**示例**:
- `user_1_1706582400.jpg`

---

## URL 访问规则

### 开发环境

```
URL: http://localhost:8000/media/recipes/1_1706582400.jpg
路径: backend/media/recipes/1_1706582400.jpg
```

### 生产环境（Nginx 配置示例）

```nginx
# 媒体文件服务
location /media/ {
    alias /path/to/backend/media/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## 图片上传流程

### 1. 前端上传

```javascript
const formData = new FormData();
formData.append('image', file);

axios.post('/api/recipes/upload-image/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

### 2. 后端处理

```python
from django.core.files.storage import default_storage
from django.utils import timezone
import os

def handle_upload(recipe_id, image_file):
    # 生成文件名
    timestamp = int(timezone.now().timestamp())
    ext = os.path.splitext(image_file.name)[1]
    filename = f"{recipe_id}_{timestamp}{ext}"

    # 保存文件
    path = default_storage.save(f"recipes/{filename}", image_file)

    # 返回 URL
    return f"{settings.MEDIA_URL}{path}"
```

### 3. 数据库存储

```python
# Recipe 模型
class Recipe(models.Model):
    image_url = models.CharField(max_length=500, verbose_name='图片URL')
    # 存储: /media/recipes/1_1706582400.jpg
```

---

## 当前数据状态

### 数据库中的图片 URL

当前导入的 20,000 条菜谱数据中，`image_url` 字段主要包含：

| 类型 | 示例 | 占比 |
|:-----|:-----|:----:|
| 外部 URL | `https://example.com/image1.jpg` | 大部分 |
| 空字符串 | `` | 少部分 |
| 本地路径 | `/media/recipes/xxx.jpg` | 0%（待上传）|

### 后续处理步骤

1. **图片下载**（可选）
   - 编写脚本从外部 URL 下载图片
   - 保存到 `media/recipes/` 目录
   - 更新数据库中的 `image_url` 字段

2. **图片上传**（管理后台）
   - 管理员可通过管理后台上传图片
   - 前端提供图片上传接口

3. **默认图片**
   - 为没有图片的菜谱设置默认图片
   - 建议位置: `media/recipes/default.jpg`

---

## 存储容量估算

### 单张图片大小

| 质量 | 分辨率 | 文件大小 |
|:-----|:------|:--------:|
| 低 | 640x480 | ~50 KB |
| 中 | 1280x720 | ~150 KB |
| 高 | 1920x1080 | ~300 KB |

### 总容量估算（20,000 张）

| 质量 | 单张大小 | 总容量 |
|:-----|:--------:|:------:|
| 低 | 50 KB | ~1 GB |
| 中 | 150 KB | ~3 GB |
| 高 | 300 KB | ~6 GB |

**建议**: 使用中等质量，总容量约 3 GB

---

## 性能优化建议

### 1. 图片压缩

```python
from PIL import Image

def compress_image(image_path, quality=85):
    """压缩图片"""
    img = Image.open(image_path)
    img.save(image_path, optimize=True, quality=quality)
```

### 2. 生成缩略图

```python
def create_thumbnail(image_path, size=(300, 200)):
    """创建缩略图"""
    img = Image.open(image_path)
    img.thumbnail(size)
    thumb_path = image_path.replace('.jpg', '_thumb.jpg')
    img.save(thumb_path)
```

### 3. 使用 CDN

生产环境建议使用 CDN 加速：
- 阿里云 CDN
- 腾讯云 CDN
- Cloudflare

---

## 验证测试

### 测试步骤

1. **启动开发服务器**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **访问媒体文件**
   ```
   http://localhost:8000/media/recipes/test.jpg
   ```

3. **验证结果**
   - ✅ 能正常访问图片文件
   - ✅ 加载速度可接受
   - ✅ 404 处理正确

### 快速验证脚本

```bash
# 在 backend/media/recipes/ 目录下放一个测试图片
# 然后访问: http://localhost:8000/media/recipes/test.jpg
```

---

## 生产环境部署

### Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 媒体文件服务
    location /media/ {
        alias /path/to/backend/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";

        # 图片压缩
        gzip on;
        gzip_types image/jpeg image/png image/webp;
        gzip_min_length 1000;
    }

    # Django 应用
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 文件权限

```bash
# 确保媒体目录可写
chmod 755 backend/media/
chmod 755 backend/media/recipes/
chmod 755 backend/media/avatars/
```

---

## 安全注意事项

1. **文件类型验证**
   - 只允许上传图片格式（jpg, png, webp）
   - 验证文件头部，而不仅是扩展名

2. **文件大小限制**
   - Django 默认限制: 2.5 MB
   - 可在 settings.py 中配置: `FILE_UPLOAD_MAX_MEMORY_SIZE`

3. **路径遍历防护**
   - 使用 Django 的 `default_storage.save()`
   - 避免直接拼接文件路径

4. **访问控制**
   - 媒体文件默认公开访问
   - 敏感图片需实现访问控制

---

## 相关文件

| 文件 | 说明 |
|:-----|:-----|
| `backend/config/settings.py` | 媒体文件配置 |
| `backend/config/urls.py` | URL 路由配置 |
| `backend/media/` | 媒体文件存储目录 |
| `.gitignore` | 排除 media/ 目录 |

---

## 下一步

- [ ] 添加图片上传 API 接口
- [ ] 实现图片下载脚本（从外部 URL 下载）
- [ ] 添加图片压缩功能
- [ ] 配置生产环境 Nginx

---

## 参考资源

- [Django 管理文件](https://docs.djangoproject.com/en/5.0/topics/files/)
- [Django 静态文件](https://docs.djangoproject.com/en/5.0/howto/static-files/)
