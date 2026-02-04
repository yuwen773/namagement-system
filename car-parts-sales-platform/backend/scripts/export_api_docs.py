"""
API 文档导出脚本

功能：
1. 检查并启动 Django 开发服务器（如果未运行）
2. 下载 Swagger JSON 和 YAML 格式的 API 文档
3. 保存到 docs/ 目录

使用方法:
    cd backend
    python scripts/export_api_docs.py

依赖:
    - requests (pip install requests)
"""

import os
import sys
import time
import subprocess
import signal
import requests
from pathlib import Path

# 设置输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# 配置
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
DOCS_DIR = BASE_DIR / 'docs'
SERVER_URL = f'http://{SERVER_HOST}:{SERVER_PORT}'

# 文档 URL
DOCS_URLS = {
    'swagger.json': f'{SERVER_URL}/swagger.json',
    'swagger.yaml': f'{SERVER_URL}/swagger.yaml',
}


class ServerManager:
    """Django 服务器管理"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.process = None

    def is_running(self):
        """检查服务器是否正在运行"""
        try:
            response = requests.get(f'http://{self.host}:{self.port}/api/', timeout=2)
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    def start(self):
        """启动 Django 开发服务器"""
        if self.is_running():
            print(f'[INFO] Django 服务器已在 {self.host}:{self.port} 运行')
            return True

        print(f'[INFO] 正在启动 Django 服务器...')
        # 设置环境变量
        env = os.environ.copy()
        env['PYTHONPATH'] = str(BASE_DIR)
        env['DJANGO_SETTINGS_MODULE'] = 'config.settings'

        self.process = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver', f'{self.host}:{self.port}'],
            cwd=str(BASE_DIR),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 等待服务器启动
        for i in range(30):  # 最多等待 30 秒
            time.sleep(1)
            if self.is_running():
                print(f'[SUCCESS] Django 服务器启动成功: {self.host}:{self.port}')
                return True
            if i % 5 == 0:
                print(f'[WAIT] 等待服务器启动... ({i+1}s)')

        print('[ERROR] Django 服务器启动失败')
        return False

    def stop(self):
        """停止 Django 服务器（仅当脚本启动的服务器）"""
        if self.process:
            print('[INFO] 正在停止 Django 服务器...')
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print('[SUCCESS] Django 服务器已停止')


def download_document(url, output_path):
    """下载文档到指定路径"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(response.text, encoding='utf-8')

        print(f'[SUCCESS] 已下载: {output_path.name} ({len(response.text)} 字节)')
        return True
    except requests.RequestException as e:
        print(f'[ERROR] 下载失败 {url}: {e}')
        return False


def export_all_docs():
    """导出所有 API 文档"""
    print('=' * 60)
    print('API 文档导出工具')
    print('=' * 60)

    # 创建文档目录
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # 服务器管理
    server = ServerManager(SERVER_HOST, SERVER_PORT)
    server_started = server.start()

    if not server_started:
        print('[ERROR] 无法启动或连接到 Django 服务器')
        return False

    try:
        # 下载文档
        print('\n[INFO] 开始下载 API 文档...\n')

        results = []
        for filename, url in DOCS_URLS.items():
            output_path = DOCS_DIR / filename
            success = download_document(url, output_path)
            results.append((filename, success))

        # 打印结果摘要
        print('\n' + '=' * 60)
        print('导出结果摘要:')
        print('=' * 60)
        for filename, success in results:
            status = '[OK] 成功' if success else '[X] 失败'
            print(f'  {filename:20} {status}')

        total = len(results)
        success_count = sum(1 for _, s in results if s)
        print(f'\n总计: {success_count}/{total} 个文件导出成功')

        if success_count == total:
            print(f'\n[SUCCESS] 所有文档已保存到: {DOCS_DIR}')
            print('\n生成的文件:')
            for filename, _ in results:
                file_path = DOCS_DIR / filename
                print(f'  - {file_path}')
            print('\n提示:')
            print('  1. JSON 文件可导入 Postman、Insomnia 等 API 工具')
            print('  2. 访问 http://swagger.io/tools/ 可将 JSON 转换为其他格式')
            print('  3. 使用在线工具 json2yaml.com 可进行格式转换')
            return True
        else:
            print(f'\n[WARNING] 部分文档导出失败，请检查网络连接和服务器状态')
            return False

    finally:
        # 仅停止脚本启动的服务器
        if server_started and server.process:
            server.stop()


def main():
    """主函数"""
    try:
        export_all_docs()
    except KeyboardInterrupt:
        print('\n\n[INFO] 用户中断操作')
        sys.exit(0)
    except Exception as e:
        print(f'\n[ERROR] 发生错误: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
