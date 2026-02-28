# 开发问题记录

本文档记录在开发过程中遇到的所有问题及其解决方案。

---

## 问题 #1: Celery 启动错误 - Module has no attribute 'celery'

**日期**: 2026-02-07

**问题描述**:
```bash
$ celery -A crawler worker -l info
Error: Unable to load celery application.
Module 'crawler' has no attribute 'celery'
```

**原因**: Celery 应用定义在 `tmall_project/celery.py` 中，而不是 `crawler` 模块中。

**解决方案**:
```bash
# 错误命令
celery -A crawler worker -l info

# 正确命令
celery -A tmall_project worker -l info
```

**预防**: 确保启动 Celery Worker 时指向正确的 Django 项目配置模块。

---

## 问题 #2: Windows 控制台编码问题导致测试脚本崩溃

**日期**: 2026-02-07

**问题描述**:
```python
UnicodeEncodeError: 'gbk' codec can't encode character '\u2713' in position 0
```

**原因**: Windows 默认控制台使用 GBK 编码，测试脚本中的 Unicode 字符（✓、✗）无法正确显示。

**解决方案**:
在 `test_crawler.py` 开头添加 UTF-8 编码设置：
```python
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

**替代方案**: 使用 ASCII 字符替换 Unicode 符号（如 `[OK]`、`[FAIL]`）。

---

## 问题 #3: CrawlLog 模型重复注册到 Django Admin

**日期**: 2026-02-07

**问题描述**:
```python
django.contrib.admin.exceptions.AlreadyRegistered:
The model CrawlLog is already registered with 'products.CrawlLogAdmin'.
```

**原因**: `CrawlLog` 模型已在 `products/admin.py` 中注册，`crawler/admin.py` 尝试重复注册。

**解决方案**:
清空 `crawler/admin.py`，只保留注释说明：
```python
"""
Admin configuration for crawler module.
注意：CrawlLog 模型已在 products/admin.py 中注册，此处无需重复注册。
"""
from django.contrib import admin

# CrawlLog 的 Admin 配置在 products/admin.py 中
```

**最佳实践**: 一个模型应该只在一个地方注册到 Admin。

---

## 问题 #4: Celery 任务 ValueError - not enough values to unpack

**日期**: 2026-02-07

**问题描述**:
```python
ValueError: not enough values to unpack (expected 3, got 0)
```

错误发生在 `celery/app/trace.py`:
```python
tasks, accept, hostname = _loc
```

**原因**: Celery 5.6.2 在 Windows 上使用默认的 `prefork` 池时存在兼容性问题。

**解决方案**:
使用 `solo` 池（单线程模式）启动 Celery Worker：
```bash
celery -A tmall_project worker -l info --pool=solo
```

或使用 `threads` 池：
```bash
set FORKED_BY_MULTIPROCESSING=0
celery -A tmall_project worker -l info --pool=threads
```

**影响**:
- `solo` 池是单线程模式，适合开发和测试
- 生产环境建议在 Linux 上使用默认配置

---

## 问题 #5: 非交互模式下 input() 导致 EOFError

**日期**: 2026-02-07

**问题描述**:
```python
EOFError: EOF when reading a line
```

当在非交互式环境（如 Git Bash、CI/CD）运行测试脚本时，`input()` 调用失败。

**解决方案**:
使用 try-except 捕获 EOFError：
```python
try:
    choice = input("\n是否继续测试爬虫任务? (y/n): ").lower()
except (EOFError, OSError):
    print("\n[SKIP] 非交互模式，跳过爬虫任务测试")
    return None  # 返回 None 表示跳过
```

**最佳实践**: 为测试脚本提供非交互模式支持，便于自动化测试。

---

## 问题 #6: tasks.py 中嵌套函数缩进错误

**日期**: 2026-02-07

**问题描述**:
`_update_progress` 函数被错误地缩进为类方法而不是嵌套函数。

**原因**: 代码结构错误，`update_progress` 应该是 `start_crawl_task` 函数内的嵌套函数，以便访问 `self`（Celery task 实例）。

**解决方案**:
```python
@shared_task(bind=True, name='crawler.tasks.start_crawl_task')
def start_crawl_task(self, mode='demo', keywords=None):
    task_id = self.request.id

    # 正确：嵌套函数定义
    def update_progress(progress, stage, items, logs):
        """内部函数：更新任务进度"""
        self.update_state(
            state='PROGRESS',
            meta={'progress': progress, 'current_stage': stage, ...}
        )

    # 使用嵌套函数
    update_progress('0%', '初始化', 0, [])
```

---

## 开发建议

### 环境配置

1. **Windows 开发环境**
   - 使用 `--pool=solo` 运行 Celery Worker
   - 设置控制台为 UTF-8 编码

2. **生产环境（Linux）**
   - 使用默认 Celery 配置
   - 考虑使用 Supervisor 管理 Celery 进程

### 代码规范

1. **Django Admin 注册**
   - 每个模型只在一个地方注册
   - 如果模型属于特定应用，在该应用的 admin.py 中注册

2. **测试脚本**
   - 支持非交互模式
   - 使用 ASCII 字符确保兼容性
   - 提供清晰的错误信息

3. **Celery 任务**
   - 使用嵌套函数访问 `self`（bind=True）
   - 正确处理异常和任务状态更新

### 相关文档

- [Celery on Windows](https://docs.celeryproject.org/en/stable/userguide/windows.html)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
