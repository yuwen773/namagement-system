from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # 调用 DRF 默认的异常处理程序，获取标准错误响应
    response = exception_handler(exc, context)

    if response is not None:
        # 自定义响应结构
        custom_data = {
            'code': response.status_code,
            'message': '请求失败',
            'data': response.data
        }

        # 如果是验证错误（400 Bad Request），优化错误提示
        if response.status_code == 400:
            messages = []
            for field, errors in response.data.items():
                if isinstance(errors, list):
                    error_msg = errors[0]
                else:
                    error_msg = errors
                
                # 尝试将字段名转换为更友好的中文名称
                field_map = {
                    'username': '用户名',
                    'password': '密码',
                    'password2': '确认密码',
                    'real_name': '真实姓名',
                    'phone': '手机号',
                    'email': '邮箱',
                    'new_password': '新密码',
                    'new_password2': '确认新密码',
                    'old_password': '旧密码',
                    'id_card': '身份证号',
                    'address': '通讯地址',
                    'emergency_contact': '紧急联系人',
                    'non_field_errors': '错误'
                }
                
                field_name = field_map.get(field, field)
                if field == 'non_field_errors':
                    messages.append(f"{error_msg}")
                else:
                    messages.append(f"{field_name}: {error_msg}")
            
            custom_data['message'] = '、'.join(messages)

        response.data = custom_data

    return response
