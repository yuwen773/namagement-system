"""
PyMySQL 兼容层

解决 Django 6.0 与 PyMySQL 版本检查不兼容的问题
"""

# 必须在 django.db.backends.mysql 之前导入并设置
import pymysql

# 修改 pymysql 的 version_info 来绕过 Django 的版本检查
pymysql.version_info = (2, 2, 1, 'final', 0)

# 然后安装为 MySQLdb
pymysql.install_as_MySQLdb()

# 导入 Django 的 MySQL 后端
from django.db.backends.mysql.base import *  # noqa
from django.db.backends.mysql.base import DatabaseWrapper as _DatabaseWrapper

__all__ = ('DatabaseWrapper',)


class DatabaseWrapper(_DatabaseWrapper):
    """
    自定义 DatabaseWrapper，确保兼容性
    """
    pass
