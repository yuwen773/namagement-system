from rest_framework import serializers
from django.utils import timezone
from .models import Region, Cinema


class RegionSerializer(serializers.ModelSerializer):
    """
    地域序列化器

    用于序列化地域（省份/城市）的基本信息，包含父级地域名称和子地域数量统计。

    字段说明：
    - id: 地域唯一标识
    - name: 地域名称
    - parent: 父级地域ID（省份为null，城市为所属省份ID）
    - parent_name: 父级地域名称（只读）
    - level: 地域层级（PROVINCE-省份/CITY-城市）
    - created_at: 创建时间
    - children_count: 子地域数量（只读）

    使用场景：
    - 地域列表展示
    - 地域详情查看
    - 地域信息更新响应
    """
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            'id', 'name', 'parent', 'parent_name', 'level',
            'created_at', 'children_count'
        ]
        read_only_fields = ['id', 'created_at']

    def get_children_count(self, obj):
        """
        获取子地域数量

        Args:
            obj: Region实例

        Returns:
            int: 子地域数量
        """
        return obj.children.count()


class RegionCreateSerializer(serializers.ModelSerializer):
    """
    地域创建序列化器

    用于创建新地域时的数据验证和序列化。

    字段说明：
    - name: 地域名称（必填）
    - parent: 父级地域ID（省份为null，城市必填）
    - level: 地域层级（PROVINCE-省份/CITY-城市，必填）

    验证规则：
    - 省份（level=PROVINCE）不能有父级
    - 城市（level=CITY）必须指定父级省份
    - 父级地域必须是省份级别

    使用场景：
    - 创建新地域
    - 更新地域信息
    """
    class Meta:
        model = Region
        fields = ['name', 'parent', 'level']

    def validate(self, attrs):
        """
        验证地域数据

        验证规则：
        1. 省份不能有父级地域
        2. 城市必须选择父级省份
        3. 父级地域必须是省份级别

        Args:
            attrs: 待验证的数据字典

        Returns:
            dict: 验证通过的数据

        Raises:
            ValidationError: 验证失败时抛出
        """
        parent = attrs.get('parent')
        level = attrs.get('level')

        # 如果选择省份，则不能有父级
        if level == 'PROVINCE' and parent:
            raise serializers.ValidationError({
                'parent': '省份不能有父级地域'
            })

        # 如果选择城市，必须选择父级省份
        if level == 'CITY' and not parent:
            raise serializers.ValidationError({
                'parent': '城市必须选择父级省份'
            })

        # 验证父级必须是省份
        if parent and parent.level != 'PROVINCE':
            raise serializers.ValidationError({
                'parent': '父级地域必须是省份'
            })

        return attrs


class RegionTreeSerializer(serializers.ModelSerializer):
    """
    地域树形结构序列化器

    用于序列化地域的层级树形结构，递归包含所有子地域。

    字段说明：
    - id: 地域唯一标识
    - name: 地域名称
    - level: 地域层级（PROVINCE-省份/CITY-城市）
    - children: 子地域列表（递归结构）

    使用场景：
    - 地域选择器（省-市级联）
    - 地域树形展示
    - 地域层级导航

    示例结构：
    ```json
    {
        "id": 1,
        "name": "北京市",
        "level": "PROVINCE",
        "children": [
            {
                "id": 3,
                "name": "朝阳区",
                "level": "CITY",
                "children": []
            }
        ]
    }
    ```
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ['id', 'name', 'level', 'children']

    def get_children(self, obj):
        """
        递归获取子地域

        Args:
            obj: Region实例

        Returns:
            list: 子地域序列化列表，如果无子地域返回空列表
        """
        children = obj.children.all()
        if children.exists():
            return RegionTreeSerializer(children, many=True).data
        return []


class CinemaSerializer(serializers.ModelSerializer):
    """
    影院序列化器

    用于序列化影院的完整信息，包含地域名称和累计票房统计。

    字段说明：
    - id: 影院唯一标识
    - name: 影院名称
    - address: 影院地址
    - phone: 联系电话
    - region: 所属地域ID（城市级别）
    - region_name: 所属地域名称（只读）
    - parent_region_name: 所属省份名称（只读）
    - screen_count: 屏幕数量
    - seats_count: 座位总数
    - is_active: 是否营业中
    - created_at: 创建时间（只读）
    - updated_at: 更新时间（只读）
    - box_office_total: 累计票房（万元，只读）

    使用场景：
    - 影院列表展示
    - 影院详情查看
    - 影院信息更新响应
    - 影院创建响应

    说明：
    - box_office_total 从关联的票房记录动态计算
    - 地域信息自动包含城市和省份名称
    """
    region_name = serializers.CharField(source='region.name', read_only=True)
    parent_region_name = serializers.CharField(source='region.parent.name', read_only=True)
    box_office_total = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = [
            'id', 'name', 'address', 'phone', 'region',
            'region_name', 'parent_region_name', 'screen_count',
            'seats_count', 'is_active', 'created_at',
            'updated_at', 'box_office_total'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_box_office_total(self, obj):
        """
        获取该影院累计票房（从关联的票房记录计算）

        从 BoxOfficeRecord 表汇总该影院的所有票房记录，
        并转换为万元单位。

        Args:
            obj: Cinema实例

        Returns:
            float: 累计票房（万元），保留两位小数
        """
        from boxoffice.models import BoxOfficeRecord
        from django.db.models import Sum
        total = BoxOfficeRecord.objects.filter(cinema=obj).aggregate(
            total=Sum('daily_box_office')
        )['total'] or 0
        return total / 10000  # 转换为万元


class CinemaCreateSerializer(serializers.ModelSerializer):
    """
    影院创建序列化器

    用于创建新影院时的数据验证和序列化。

    字段说明：
    - name: 影院名称（必填）
    - address: 影院地址（必填）
    - phone: 联系电话（可选）
    - region: 所属地域ID（必填，必须是城市级别）
    - screen_count: 屏幕数量（必填，必须大于0）
    - seats_count: 座位总数（必填，必须大于0）
    - is_active: 是否营业中（可选，默认true）

    验证规则：
    - 屏幕数量必须大于0
    - 座位数量必须大于0
    - 必须指定所属地域

    使用场景：
    - 创建新影院
    - 影院信息录入
    """
    class Meta:
        model = Cinema
        fields = [
            'name', 'address', 'phone', 'region',
            'screen_count', 'seats_count', 'is_active'
        ]

    def validate_screen_count(self, value):
        """
        验证屏幕数量

        Args:
            value: 屏幕数量

        Returns:
            int: 验证通过后的屏幕数量

        Raises:
            ValidationError: 如果屏幕数量小于0
        """
        if value < 0:
            raise serializers.ValidationError('屏幕数量必须大于0')
        return value

    def validate_seats_count(self, value):
        """
        验证座位数量

        Args:
            value: 座位数量

        Returns:
            int: 验证通过后的座位数量

        Raises:
            ValidationError: 如果座位数量小于0
        """
        if value < 0:
            raise serializers.ValidationError('座位数量必须大于0')
        return value


class CinemaUpdateSerializer(serializers.ModelSerializer):
    """
    影院更新序列化器

    用于更新影院信息时的数据验证和序列化。

    字段说明：
    - name: 影院名称
    - address: 影院地址
    - phone: 联系电话
    - region: 所属地域ID（必须是城市级别）
    - screen_count: 屏幕数量（必须大于0）
    - seats_count: 座位总数（必须大于0）
    - is_active: 是否营业中

    验证规则：
    - 屏幕数量必须大于0
    - 座位数量必须大于0

    使用场景：
    - 更新影院基本信息
    - 修改影院营业状态
    - 调整影院屏幕和座位数量

    说明：
    - 支持部分更新（PATCH请求）
    - 所有字段都是可选的
    """
    class Meta:
        model = Cinema
        fields = [
            'name', 'address', 'phone', 'region',
            'screen_count', 'seats_count', 'is_active'
        ]

    def validate_screen_count(self, value):
        """
        验证屏幕数量

        Args:
            value: 屏幕数量

        Returns:
            int: 验证通过后的屏幕数量

        Raises:
            ValidationError: 如果屏幕数量小于0
        """
        if value < 0:
            raise serializers.ValidationError('屏幕数量必须大于0')
        return value

    def validate_seats_count(self, value):
        """
        验证座位数量

        Args:
            value: 座位数量

        Returns:
            int: 验证通过后的座位数量

        Raises:
            ValidationError: 如果座位数量小于0
        """
        if value < 0:
            raise serializers.ValidationError('座位数量必须大于0')
        return value
