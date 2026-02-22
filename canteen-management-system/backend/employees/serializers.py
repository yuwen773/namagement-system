from rest_framework import serializers
from .models import EmployeeProfile


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """
    员工档案详情序列化器
    用于创建、更新、详情展示
    """
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # 字段级别中文错误消息
    name = serializers.CharField(
        error_messages={
            'required': '姓名不能为空',
            'blank': '姓名不能为空',
            'max_length': '姓名最多50个字符',
        }
    )
    phone = serializers.CharField(
        max_length=20,
        error_messages={
            'required': '手机号不能为空',
            'blank': '手机号不能为空',
            'max_length': '手机号最多20个字符',
        }
    )
    id_card = serializers.CharField(
        max_length=18,
        error_messages={
            'blank': '身份证号不能为空',
            'max_length': '身份证号最多18个字符',
        }
    )
    gender = serializers.ChoiceField(
        choices=EmployeeProfile.Gender.choices,
        error_messages={
            'invalid_choice': '请选择有效的性别',
            'required': '性别不能为空',
        }
    )
    position = serializers.ChoiceField(
        choices=EmployeeProfile.Position.choices,
        error_messages={
            'invalid_choice': '请选择有效的职位',
            'required': '职位不能为空',
        }
    )
    entry_date = serializers.DateField(
        error_messages={
            'required': '入职日期不能为空',
            'invalid': '入职日期格式不正确，请使用 YYYY-MM-DD 格式',
        }
    )
    status = serializers.ChoiceField(
        choices=EmployeeProfile.Status.choices,
        error_messages={
            'invalid_choice': '请选择有效的状态',
            'required': '状态不能为空',
        }
    )
    health_certificate_expiry = serializers.DateField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': '健康证到期日期格式不正确，请使用 YYYY-MM-DD 格式',
        }
    )
    health_certificate_no = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': '健康证号最多50个字符',
        }
    )
    chef_certificate_level = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': '厨师证等级最多20个字符',
        }
    )

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'name', 'gender', 'gender_display', 'phone', 'id_card', 'address',
            'position', 'position_display', 'entry_date', 'status', 'status_display',
            'health_certificate_no', 'health_certificate_expiry', 'health_certificate_url',
            'chef_certificate_level', 'created_at', 'updated_at'
        ]

    def validate_id_card(self, value):
        """
        验证身份证号唯一性（更新时排除当前记录）
        """
        if value:
            instance = self.instance
            queryset = EmployeeProfile.objects.filter(id_card=value)
            if instance:
                queryset = queryset.exclude(id=instance.id)
            if queryset.exists():
                raise serializers.ValidationError('该身份证号已存在')
        return value


class EmployeeProfileListSerializer(serializers.ModelSerializer):
    """
    员工档案列表序列化器（简化版）
    用于列表展示，不包含详细信息
    """
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'name', 'gender', 'gender_display', 'phone', 'id_card',
            'position', 'position_display', 'entry_date', 'status', 'status_display',
            'created_at'
        ]
