from django.db import models


class Department(models.Model):
    """
    部门模型：树形结构，支持无限层级
    """
    name = models.CharField("部门名称", max_length=50)
    code = models.CharField("部门编码", max_length=20, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="上级部门"
    )
    sort_order = models.IntegerField("排序", default=0)
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name

    def get_full_path(self):
        """获取部门完整路径，如：总公司/技术部/后端组"""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name


class Post(models.Model):
    """
    岗位模型：关联到部门
    """
    name = models.CharField("岗位名称", max_length=50)
    code = models.CharField("岗位编码", max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="所属部门"
    )
    description = models.TextField("岗位描述", blank=True, default="")
    sort_order = models.IntegerField("排序", default=0)
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "岗位"
        verbose_name_plural = "岗位"
        ordering = ["department__sort_order", "department_id", "sort_order", "id"]

    def __str__(self):
        return self.name
