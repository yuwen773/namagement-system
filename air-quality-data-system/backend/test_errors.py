# Test error messages
from apps.accounts.serializers import LoginSerializer, RegisterSerializer

# 测试登录 - 缺少必填字段
print("=== 测试登录 - 缺少用户名 ===")
s = LoginSerializer(data={'password': 'test123'})
s.is_valid()
print(s.errors)

# 测试登录 - 缺少密码
print("\n=== 测试登录 - 缺少密码 ===")
s = LoginSerializer(data={'username': 'test'})
s.is_valid()
print(s.errors)

# 测试注册 - 缺少用户名
print("\n=== 测试注册 - 缺少用户名 ===")
s = RegisterSerializer(data={'password': 'test123456', 'email': 'test@example.com'})
s.is_valid()
print(s.errors)

# 测试注册 - 密码长度不足
print("\n=== 测试注册 - 密码长度不足 ===")
s = RegisterSerializer(data={'username': 'testuser', 'password': '12345', 'email': 'test@example.com'})
s.is_valid()
print(s.errors)

# 测试注册 - 邮箱格式错误
print("\n=== 测试注册 - 邮箱格式错误 ===")
s = RegisterSerializer(data={'username': 'testuser', 'password': '123456', 'email': 'invalid-email'})
s.is_valid()
print(s.errors)

# 测试注册 - 用户名太短
print("\n=== 测试注册 - 用户名太短 ===")
s = RegisterSerializer(data={'username': 'ab', 'password': '123456', 'email': 'test@example.com'})
s.is_valid()
print(s.errors)
