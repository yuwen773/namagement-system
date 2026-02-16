from django.db import models


class AreaType(models.TextChoices):
    TEACHING = "TEACHING", "教学区"
    LIVING = "LIVING", "生活区"
    OFFICE = "OFFICE", "办公区"


class RoomType(models.TextChoices):
    DORMITORY = "DORMITORY", "宿舍"
    OFFICE = "OFFICE", "办公室"
    CLASSROOM = "CLASSROOM", "教室"


class Campus(models.Model):
    name = models.CharField(max_length=128, verbose_name="校区名称")
    code = models.CharField(max_length=64, unique=True, verbose_name="校区编码")
    capacity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="校区容量",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "em_campuses"
        verbose_name = "校区"
        verbose_name_plural = "校区"

    def __str__(self) -> str:
        return f"{self.name}({self.code})"


class Building(models.Model):
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name="buildings",
        verbose_name="所属校区",
    )
    name = models.CharField(max_length=128, verbose_name="建筑名称")
    code = models.CharField(max_length=64, unique=True, verbose_name="建筑编码")
    area_type = models.CharField(
        max_length=16,
        choices=AreaType.choices,
        default=AreaType.TEACHING,
        verbose_name="区域类型",
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    floors_count = models.PositiveIntegerField(default=0, verbose_name="楼层数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "em_buildings"
        verbose_name = "建筑"
        verbose_name_plural = "建筑"
        constraints = [
            models.UniqueConstraint(
                fields=["campus", "name"],
                name="uk_em_buildings_campus_name",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}({self.code})"


class Floor(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="floors",
        verbose_name="所属建筑",
    )
    floor_number = models.IntegerField(verbose_name="楼层号")
    name = models.CharField(max_length=64, verbose_name="楼层名称")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "em_floors"
        verbose_name = "楼层"
        verbose_name_plural = "楼层"
        constraints = [
            models.UniqueConstraint(
                fields=["building", "floor_number"],
                name="uk_em_floors_building_floor_number",
            )
        ]

    def __str__(self) -> str:
        return f"{self.building.name}-{self.name}"


class Room(models.Model):
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="所属楼层",
    )
    room_number = models.CharField(max_length=32, verbose_name="房间号")
    room_type = models.CharField(
        max_length=16,
        choices=RoomType.choices,
        default=RoomType.CLASSROOM,
        verbose_name="房间类型",
    )
    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="面积(㎡)",
    )
    department = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="所属部门",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "em_rooms"
        verbose_name = "房间"
        verbose_name_plural = "房间"
        constraints = [
            models.UniqueConstraint(
                fields=["floor", "room_number"],
                name="uk_em_rooms_floor_room_number",
            )
        ]

    def __str__(self) -> str:
        return f"{self.floor.name}-{self.room_number}"
