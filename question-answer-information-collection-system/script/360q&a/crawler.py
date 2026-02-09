"""360问答网站的爬虫 - 支持分页、断点续爬"""

import re
import csv
import os
import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin
from datetime import datetime


# ==================== 日志配置 ====================
def setup_logger(name: str = "qihu_crawler", level: int = logging.INFO) -> logging.Logger:
    """
    配置日志记录器（仅控制台输出）

    Args:
        name: 日志记录器名称
        level: 日志级别

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


class QihuWendaCrawler:
    """360问答爬虫"""

    BASE_URL = "https://wenda.so.com"

    # 默认请求头（从抓包分析获得）
    DEFAULT_HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://wenda.so.com/",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Microsoft Edge\";v=\"144\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    }

    def __init__(self, cookies: Optional[str] = None):
        """
        初始化爬虫

        Args:
            cookies: 可选的cookies字符串（如果为None，尝试从cookies.txt加载）
        """
        # 初始化日志记录器
        self.logger = setup_logger("qihu_list")
        self.logger.info("=" * 60)
        self.logger.info("360问答爬虫初始化")

        # 初始化会话
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

        # 加载cookies：优先使用传入的cookies，否则尝试从文件加载
        cookie_str = cookies or self._load_cookies_from_file()
        if cookie_str:
            self.session.cookies.update(self._parse_cookies(cookie_str))
            self.logger.info("已配置Cookies")
        else:
            self.logger.warning("未配置Cookies，可能影响爬取效果")

        self.logger.info(f"目标网站: {self.BASE_URL}")
        self.logger.info("=" * 60)

    def _load_cookies_from_file(self) -> Optional[str]:
        """
        从cookies.txt文件加载cookies

        Returns:
            cookies字符串，如果文件不存在或读取失败则返回None
        """
        cookie_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
        if not os.path.exists(cookie_file):
            return None

        try:
            with open(cookie_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    self.logger.info(f"从文件加载Cookies: {cookie_file}")
                    return content
        except Exception as e:
            self.logger.warning(f"读取cookies.txt失败: {e}")

        return None

    def _parse_cookies(self, cookie_str: str) -> dict:
        """解析cookies字符串"""
        cookies = {}
        for item in cookie_str.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookies[key] = value

        self.logger.debug(f"解析Cookies: {len(cookies)} 个键值对")
        return cookies

    def get_page(self, page_num: int = 1) -> str:
        """
        获取指定页码的HTML内容

        Args:
            page_num: 页码 (1=第1页, 2=第2页, ...)

        Returns:
            HTML内容
        """
        # pn参数从0开始: pn=0 -> 第1页, pn=1 -> 第2页
        pn = page_num - 1
        if pn == 0:
            url = f"{self.BASE_URL}/c/"
        else:
            url = f"{self.BASE_URL}/c/?pn={pn}"

        self.logger.debug(f"请求页面: {url}")

        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        self.logger.debug(f"页面获取成功: 第{page_num}页, HTML长度: {len(response.text)}字符")
        return response.text

    def _is_empty_page(self, html: str) -> bool:
        """检查是否为空白页（无问题数据）"""
        # 检查HTML是否异常短（可能是网站返回的空/错误页面）
        MIN_HTML_LENGTH = 10000  # 最小有效HTML长度
        if len(html) < MIN_HTML_LENGTH:
            self.logger.debug(f"HTML长度异常: {len(html)} < {MIN_HTML_LENGTH}")
            return True  # 异常短，判定为空页

        soup = BeautifulSoup(html, "html.parser")

        # 方法1: 检查是否有问题列表
        question_items = soup.select("ul.question-list li")
        if question_items:
            return False

        # 方法2: 检查是否有任何data-askid的li
        data_items = soup.select("li[data-askid]")
        if data_items:
            return False

        # 方法3: 检查是否有问题链接
        question_links = soup.select("a[href^='/q/']")
        if question_links:
            return False

        # 方法4: 检查pagination元素是否存在
        pagination = soup.select_one(".pagination, #list-page")
        if pagination:
            return False

        # 方法5: 检查是否有 "已解决" 或问题库相关的文本
        page_text = soup.get_text()
        if "已解决" in page_text or "问题库" in page_text:
            return False

        # 如果以上都没有，判定为空页
        return True

    def parse_question_list(self, html: str, page_num: int = 1) -> List[Dict]:
        """
        解析问题列表页面

        Args:
            html: HTML内容
            page_num: 页码（用于标记pn字段）

        Returns:
            问题列表，每项包含: id, title, category, answer_count, time, location, pn
        """
        self.logger.debug(f"开始解析第{page_num}页问题列表")
        soup = BeautifulSoup(html, "html.parser")
        questions = []

        # 查找问题列表 - 根据抓包分析的HTML结构
        # 结构: <ul class="question-list"> <li data-askid="xxx"> ... </li> </ul>
        question_items = soup.select("ul.question-list li")

        # 如果上面的选择器没找到，尝试备用选择器
        if not question_items:
            question_items = soup.select("li[data-askid]")

        if not question_items:
            self.logger.warning(f"第{page_num}页: 未找到问题列表项")

        for item in question_items:
            try:
                question = self._parse_question_item(item, page_num)
                if question:
                    questions.append(question)
            except Exception as e:
                self.logger.error(f"解析问题项失败: {e}", exc_info=True)
                continue

        self.logger.debug(f"第{page_num}页解析完成: {len(questions)}条问题")
        return questions

    def _parse_question_item(self, item, page_num: int = 1) -> Optional[Dict]:
        """解析单个问题项"""
        # 提取问题ID - 从data-askid属性获取
        qid = item.get("data-askid", "")

        # 备用: 从href中获取
        if not qid:
            title_link = item.select_one("a[href^='/q/']")
            if title_link:
                href = title_link.get("href", "")
                qid_match = re.search(r"/q/(\d+)", href)
                qid = qid_match.group(1) if qid_match else ""

        # 提取问题标题 - 查找有target="_blank"的链接
        title_link = item.select_one("a[target='_blank']")
        if not title_link:
            title_link = item.select_one("a[href^='/q/']")

        title = title_link.get_text(strip=True) if title_link else ""

        # 提取分类
        category_link = item.select_one("a.js-question-cate")
        category = category_link.get_text(strip=True) if category_link else ""

        # 从data-ans属性获取回答数（备用）
        answer_count = int(item.get("data-ans", 0))

        # 从div.fr中提取回答个数、时间、地点
        info_div = item.select_one("div.fr")
        if info_div:
            info_text = info_div.get_text(strip=True)

            # 解析回答个数（备用方法）
            ans_match = re.search(r"(\d+)个回答", info_text)
            if ans_match:
                answer_count = int(ans_match.group(1))

            # 解析时间
            time_str = ""
            time_match = re.search(r"(\d{4}\.\d{2}\.\d{2})", info_text)
            if time_match:
                time_str = time_match.group(1)

            # 解析地点
            location = ""
            loc_match = re.search(r"·\s*(\S+)", info_text)
            if loc_match:
                location = loc_match.group(1).strip()
        else:
            time_str = ""
            location = ""

        return {
            "id": qid,
            "title": title,
            "category": category,
            "answer_count": answer_count,
            "time": time_str,
            "location": location,
            "pn": page_num,  # 新增：页码列
        }

    def crawl_pages(self, max_pages: int = 10, delay: float = 1.0,
                    min_questions_per_page: int = 1, start_page: int = 1,
                    max_retries: int = 2) -> Tuple[List[Dict], int]:
        """
        爬取多页数据

        Args:
            max_pages: 最大爬取页数
            delay: 请求间隔（秒）
            min_questions_per_page: 每页最少问题数（低于此值则停止爬取）
            start_page: 起始页码（用于断点续爬）
            max_retries: 每次失败后的最大重试次数

        Returns:
            (爬取的问题列表, 最后一页页码)
        """
        import time as time_module

        self.logger.info("=" * 50)
        self.logger.info("开始爬取任务")
        self.logger.info(f"配置: 最大页数={max_pages}, 请求间隔={delay}秒, 起始页={start_page}, 最大重试={max_retries}")

        all_questions = []
        consecutive_empty = 0  # 连续空页计数
        max_consecutive_empty = 2  # 连续空页阈值
        last_page = start_page - 1

        for page_num in range(start_page, max_pages + 1):
            self.logger.info(f"正在爬取第 {page_num}/{max_pages} 页...")
            print(f"正在爬取第 {page_num} 页...")  # 保留终端输出

            retries = 0
            html = None
            questions = []
            is_empty = True

            while retries <= max_retries:
                try:
                    html = self.get_page(page_num)

                    # 检查HTML是否异常短（需要重试）
                    if len(html) < 10000:
                        retries += 1
                        if retries <= max_retries:
                            wait_time = retries * 3  # 更长的等待时间
                            msg = f"HTML异常短（{len(html)}字符），{wait_time}秒后重试 ({retries}/{max_retries})"
                            print(f"  {msg}")
                            self.logger.warning(f"第{page_num}页: {msg}")
                            time_module.sleep(wait_time)
                            continue
                        else:
                            # 重试次数用尽，仍然判定为空页
                            is_empty = True
                            questions = []
                            self.logger.error(f"第{page_num}页: HTML异常短且重试次数用尽")
                            break

                    is_empty = self._is_empty_page(html)
                    questions = self.parse_question_list(html, page_num) if not is_empty else []
                    break  # 请求成功，跳出重试循环

                except requests.RequestException as e:
                    retries += 1
                    if retries <= max_retries:
                        wait_time = retries * 3  # 递增等待时间
                        msg = f"请求失败，{wait_time}秒后重试 ({retries}/{max_retries}): {e}"
                        print(f"  {msg}")
                        self.logger.warning(f"第{page_num}页: {msg}")
                        time_module.sleep(wait_time)
                    else:
                        msg = f"请求第 {page_num} 页失败，已重试 {max_retries} 次: {e}"
                        print(f"  {msg}")
                        self.logger.error(f"第{page_num}页: {msg}")

            # 检查结果
            if not html:
                msg = f"无法获取第 {page_num} 页内容，跳过"
                print(f"  {msg}")
                self.logger.warning(f"第{page_num}页: {msg}")
                continue

            if is_empty:
                # 如果HTML正常但为空，才停止；如果是因为异常短，重试次数用尽也停止
                if len(html) >= 10000:
                    msg = f"[警告] 第 {page_num} 页被判定为空页"
                    print(f"  {msg}")
                    self.logger.warning(f"第{page_num}页: {msg}")
                    self.logger.debug(f"  - HTML长度: {len(html)} 字符")
                    # 诊断：检查HTML中的关键元素
                    from bs4 import BeautifulSoup as BS
                    diag_soup = BS(html, "lxml") if html else None
                    if diag_soup:
                        li_count = len(diag_soup.select('ul.question-list li'))
                        data_count = len(diag_soup.select('li[data-askid]'))
                        has_pagination = diag_soup.select_one('.pagination') is not None
                        self.logger.debug(f"  - ul.question-list li: {li_count}")
                        self.logger.debug(f"  - li[data-askid]: {data_count}")
                        self.logger.debug(f"  - pagination: {'存在' if has_pagination else '不存在'}")
                        page_text = diag_soup.get_text()[:500] if diag_soup else ""
                        has_content = "已解决" in page_text or "问题库" in page_text
                        self.logger.debug(f"  - 包含'已解决'文本: {'是' if has_content else '否'}")
                    print(f"  - HTML长度: {len(html)} 字符")
                    print(f"  停止爬取")
                    self.logger.info(f"第{page_num}页为空页，停止爬取")
                    break
                else:
                    # HTML异常短，重试次数用尽
                    msg = f"[错误] 第 {page_num} 页HTML异常短，已重试 {max_retries} 次"
                    print(f"  {msg}")
                    self.logger.error(f"第{page_num}页: {msg}")
                    self.logger.error(f"  - HTML长度: {len(html)} 字符")
                    print(f"    - HTML长度: {len(html)} 字符")
                    print(f"  可能原因：网站限制或cookies过期")
                    print(f"  建议：稍后重试或更新cookies")
                    self.logger.error(f"  可能原因：网站限制或cookies过期")
                    break

            if not questions:
                msg = f"第 {page_num} 页HTML正常但解析为0条问题，继续下一页"
                print(f"  {msg}")
                self.logger.warning(f"第{page_num}页: {msg}")
                consecutive_empty += 1
                if consecutive_empty >= max_consecutive_empty:
                    msg = f"连续 {max_consecutive_empty} 页无数据，停止爬取"
                    print(f"  {msg}")
                    self.logger.warning(f"第{page_num}页: {msg}")
                    break
                continue

            # 有数据
            consecutive_empty = 0
            last_page = page_num
            all_questions.extend(questions)
            msg = f"-> 获取 {len(questions)} 条问题 (累计: {len(all_questions)})"
            print(f"  {msg}")
            self.logger.info(f"第{page_num}页: {msg}")

            # 延时，避免请求过快
            if delay > 0 and page_num < max_pages:
                time_module.sleep(delay)

        self.logger.info("=" * 50)
        self.logger.info(f"爬取任务完成: 共 {len(all_questions)} 条问题, 最后一页: {last_page}")
        return all_questions, last_page

    def load_existing_csv(self, filepath: str = "360_qa.csv") -> Tuple[List[Dict], int]:
        """
        读取已存在的CSV文件，获取已有数据

        Args:
            filepath: CSV文件路径

        Returns:
            (已存在的数据列表, 最大页码)
        """
        if not os.path.exists(filepath):
            self.logger.info(f"CSV文件不存在: {filepath}")
            return [], 0

        existing_data = []
        max_pn = 0

        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_data.append(row)
                if "pn" in row:
                    try:
                        pn = int(row["pn"])
                        if pn > max_pn:
                            max_pn = pn
                    except ValueError:
                        pass

        self.logger.info(f"从CSV加载数据: {filepath}, {len(existing_data)}条记录, 最大页码: {max_pn}")
        return existing_data, max_pn

    def export_to_csv(self, questions: List[Dict], filepath: str = "360_qa.csv",
                      mode: str = "overwrite", existing_data: List[Dict] = None):
        """
        导出数据到CSV文件

        Args:
            questions: 问题列表
            filepath: 输出文件路径
            mode: 模式 - "overwrite"(覆盖) 或 "append"(追加)
            existing_data: 已存在的数据（用于合并）
        """
        self.logger.info(f"导出CSV: {filepath}, 模式: {mode}, 新数据: {len(questions)}条")

        if not questions and not existing_data:
            print("没有数据可导出")
            self.logger.warning("没有数据可导出")
            return

        # 字段名（包含pn列）
        fieldnames = ["pn", "id", "title", "category", "answer_count", "time", "location"]

        if mode == "append" and existing_data:
            # 追加模式：合并已有数据和新数据
            all_data = existing_data + questions
            # 去重：基于id去重
            seen_ids = set()
            unique_data = []
            for item in all_data:
                if item.get("id") not in seen_ids:
                    seen_ids.add(item.get("id"))
                    unique_data.append(item)

            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(unique_data)

            new_count = len(unique_data) - len(existing_data)
            print(f"已追加 {len(questions)} 条数据 (去重后新增 {new_count} 条)")
            print(f"文件总计 {len(unique_data)} 条数据")
            self.logger.info(f"追加模式完成: 原有{len(existing_data)}条, 新增{len(questions)}条, 去重后总计{len(unique_data)}条")
        else:
            # 覆盖模式
            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(questions)

            print(f"已导出 {len(questions)} 条数据到 {filepath}")
            self.logger.info(f"覆盖模式完成: 导出{len(questions)}条数据到 {filepath}")


def main():
    """主函数 - 爬取360问答数据"""
    import time

    crawler = QihuWendaCrawler()
    csv_file = "360_qa.csv"

    crawler.logger.info("=" * 60)
    crawler.logger.info("程序启动: 爬取360问答数据")
    crawler.logger.info(f"CSV文件: {csv_file}")

    # 检查是否已有CSV文件
    existing_data, max_pn = crawler.load_existing_csv(csv_file)

    if existing_data:
        print(f"检测到已存在的CSV文件: {csv_file}")
        print(f"  - 已有的数据: {len(existing_data)} 条")
        print(f"  - 最大页码: {max_pn}")
        crawler.logger.info(f"检测到已存在CSV: {len(existing_data)}条, 最大页码: {max_pn}")

        # 让用户选择模式
        print("\n请选择模式:")
        print("  1. 断点续爬 - 从上次停止的页码继续爬取")
        print("  2. 重新爬取 - 覆盖原有数据，从第1页开始")
        print("  3. 追加爬取 - 从指定页码开始，追加到现有数据")

        choice = input("\n请输入选项 (1/2/3): ").strip()
        crawler.logger.info(f"用户选择模式: {choice}")

        if choice == "1":
            # 断点续爬
            start_page = max_pn + 1
            print(f"\n>>> 断点续爬模式：从第 {start_page} 页开始")
            crawler.logger.info(f"断点续爬模式: 起始页={start_page}")
            mode = "append"
        elif choice == "2":
            # 重新爬取
            print("\n>>> 重新爬取模式：从第1页开始，覆盖原有数据")
            crawler.logger.info("重新爬取模式: 覆盖原有数据")
            existing_data = []  # 清空已有数据
            start_page = 1
            mode = "overwrite"
        elif choice == "3":
            # 追加爬取
            try:
                start_page = int(input("请输入起始页码: ").strip())
                print(f"\n>>> 追加爬取模式：从第 {start_page} 页开始")
                crawler.logger.info(f"追加爬取模式: 起始页={start_page}")
                mode = "append"
            except ValueError:
                print("无效的页码，将从第1页开始")
                crawler.logger.warning("无效的页码，使用默认设置")
                start_page = 1
                mode = "overwrite"
        else:
            print("无效选项，默认使用断点续爬")
            crawler.logger.warning(f"无效选项'{choice}'，使用断点续爬模式")
            start_page = max_pn + 1
            mode = "append"
    else:
        # 没有已有文件，正常爬取
        print("未检测到已有CSV文件，将从第1页开始爬取")
        crawler.logger.info("未检测到已有CSV，从第1页开始")
        start_page = 1
        mode = "overwrite"
        existing_data = []

    # 爬取参数
    max_pages = input("\n请输入最大爬取页数 (直接回车默认10页): ").strip()
    max_pages = int(max_pages) if max_pages else 10

    delay_input = input("请输入请求间隔秒数 (直接回车默认1秒): ").strip()
    delay = float(delay_input) if delay_input else 1.0

    print(f"\n开始爬取... (最大{max_pages}页, 间隔{delay}秒)")
    crawler.logger.info(f"爬取参数: 最大页数={max_pages}, 间隔={delay}秒, 起始页={start_page}")

    # 记录开始时间
    start_time = time.time()

    # 爬取数据
    questions, last_page = crawler.crawl_pages(
        max_pages=max_pages,
        delay=delay,
        start_page=start_page
    )

    # 导出数据
    crawler.export_to_csv(questions, csv_file, mode=mode, existing_data=existing_data)

    # 统计
    elapsed = time.time() - start_time
    print(f"\n===== 爬取完成 =====")
    print(f"本次爬取: {len(questions)} 条")
    print(f"最后一页: {last_page}")
    print(f"耗时: {elapsed:.1f} 秒")
    crawler.logger.info("=" * 60)
    crawler.logger.info("程序执行完成")
    crawler.logger.info(f"本次爬取: {len(questions)}条, 最后一页: {last_page}, 耗时: {elapsed:.1f}秒")
    crawler.logger.info("=" * 60)


class QihuWendaDetailCrawler:
    """360问答详情页爬虫 - 从CSV文件读取问题ID并获取详细答案"""

    BASE_URL = "https://wenda.so.com"

    DEFAULT_HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://wenda.so.com/",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Microsoft Edge\";v=\"144\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    }

    def __init__(self, cookies: Optional[str] = None, delay: float = 10.0):
        """
        初始化详情页爬虫

        Args:
            cookies: 可选的cookies字符串（如果为None，尝试从cookies.txt加载）
            delay: 请求间隔（秒），避免请求过快
        """
        # 初始化日志记录器
        self.logger = setup_logger("qihu_detail")
        self.logger.info("=" * 60)
        self.logger.info("360问答详情页爬虫初始化")

        # 初始化会话
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

        # 加载cookies：优先使用传入的cookies，否则尝试从文件加载
        cookie_str = cookies or self._load_cookies_from_file()
        if cookie_str:
            self.session.cookies.update(self._parse_cookies(cookie_str))
            self.logger.info("已配置Cookies")
        else:
            self.logger.warning("未配置Cookies，可能影响爬取效果")

        self.delay = delay
        self.logger.info(f"请求间隔: {delay}秒")
        self.logger.info(f"目标网站: {self.BASE_URL}")
        self.logger.info("=" * 60)

    def _load_cookies_from_file(self) -> Optional[str]:
        """
        从cookies.txt文件加载cookies

        Returns:
            cookies字符串，如果文件不存在或读取失败则返回None
        """
        cookie_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
        if not os.path.exists(cookie_file):
            return None

        try:
            with open(cookie_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    self.logger.info(f"从文件加载Cookies: {cookie_file}")
                    return content
        except Exception as e:
            self.logger.warning(f"读取cookies.txt失败: {e}")

        return None

    def _parse_cookies(self, cookie_str: str) -> dict:
        """解析cookies字符串"""
        cookies = {}
        for item in cookie_str.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookies[key] = value

        self.logger.debug(f"解析Cookies: {len(cookies)} 个键值对")
        return cookies

    def get_question_ids_from_csv(self, csv_path: str = "360_qa.csv",
                                   id_column: str = "id") -> List[str]:
        """
        从CSV文件中读取问题ID列表

        Args:
            csv_path: CSV文件路径
            id_column: ID列的列名

        Returns:
            问题ID列表
        """
        if not os.path.exists(csv_path):
            msg = f"文件不存在: {csv_path}"
            print(msg)
            self.logger.error(msg)
            return []

        ids = []
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                qid = row.get(id_column, "").strip()
                if qid:
                    ids.append(qid)

        msg = f"从 {csv_path} 读取到 {len(ids)} 个问题ID"
        print(msg)
        self.logger.info(msg)
        return ids

    def get_detail_page(self, question_id: str) -> str:
        """
        获取指定问题ID的详情页HTML

        Args:
            question_id: 问题ID

        Returns:
            HTML内容
        """
        url = f"{self.BASE_URL}/q/{question_id}"
        self.logger.debug(f"请求详情页: {url}")

        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        self.logger.debug(f"详情页获取成功: 问题ID={question_id}, HTML长度={len(response.text)}字符")
        return response.text

    def _remove_hidden_elements(self, element):
        """
        移除元素中所有CSS隐藏的子元素（反爬虫干扰）

        Args:
            element: BeautifulSoup元素对象

        Returns:
            None（直接修改原元素）
        """
        # 检测并移除隐藏元素（通过CSS class判断）
        # 检测模式：长随机class名（>8字符且含数字字母混合）
        for tag in element.find_all(True):
            if tag.get("class"):
                for cls in tag["class"]:
                    if len(cls) > 8 and any(c.isdigit() for c in cls):
                        tag.decompose()
                        break

    def _extract_text_from_js(self, html: str, var_name: str) -> str:
        """
        从JavaScript变量中提取文本（备用方案）

        Args:
            html: HTML内容
            var_name: JavaScript变量名（如 'askTitle'）

        Returns:
            提取的文本值
        """
        # 匹配 $INFO['askTitle'] = "xxx";
        pattern = rf"\$INFO\['{var_name}'\]\s*=\s*['\"]([^'\"]+)['\"]"
        match = re.search(pattern, html)
        if match:
            return match.group(1)
        return ""

    def parse_detail(self, html: str, question_id: str) -> Dict:
        """
        解析问题详情页HTML - 增强版，支持多种解析方案

        Args:
            html: HTML内容
            question_id: 问题ID

        Returns:
            包含问题详情和答案的字典
        """
        self.logger.debug(f"解析详情页: 问题ID={question_id}")
        soup = BeautifulSoup(html, "html.parser")

        result = {
            "id": question_id,
            "question_content": "",
            "answer_list": "",
            "source_url": f"{self.BASE_URL}/q/{question_id}",
        }

        # ============ 解析问题内容 ============
        # 方案1：从HTML中获取问题标题
        title_tag = soup.select_one("h1.question-title .question-title-txt, .question-title-txt, h1.question-title")
        if title_tag:
            # 创建新soup副本，避免修改原始soup
            from copy import deepcopy
            title_soup = BeautifulSoup(str(title_tag), "html.parser")

            # 移除隐藏元素（所有带随机class的标签）
            self._remove_hidden_elements(title_soup)

            # 移除问题金币图标等无用元素
            for tag in title_soup.find_all(["i", "em"]):
                if "question-coin" in " ".join(tag.get("class", [])):
                    tag.decompose()

            # 获取纯文本
            result["question_content"] = title_soup.get_text(separator=" ", strip=True)

        # 方案2：如果HTML解析失败，从JavaScript变量获取（备用方案）
        if not result["question_content"]:
            result["question_content"] = self._extract_text_from_js(html, "askTitle")

        # ============ 解析所有答案 ============
        answer_divs = soup.select(".answer-content")
        answers = []

        for div in answer_divs:
            # 创建新soup副本
            from copy import deepcopy
            div_soup = BeautifulSoup(str(div), "html.parser")

            # 移除隐藏元素
            self._remove_hidden_elements(div_soup)

            # 获取答案文本
            answer_text = div_soup.get_text(separator=" ", strip=True)
            if answer_text:
                # 清理多余空白
                answer_text = re.sub(r'\s+', ' ', answer_text).strip()
                if len(answer_text) > 10:  # 过滤掉太短的内容
                    answers.append(answer_text)

        # 格式化答案列表：1. 答案1 2. 答案2 ...
        if answers:
            result["answer_list"] = " ".join([f"{i+1}. {ans}" for i, ans in enumerate(answers)])

        self.logger.debug(f"详情解析完成: 问题ID={question_id}, 答案数={len(answers)}")
        return result

    def crawl_details(self, question_ids: List[str], output_csv: str = "360_qa_detail.csv",
                      start_idx: int = 0, max_count: Optional[int] = None,
                      show_progress: bool = True) -> List[Dict]:
        """
        批量爬取问题详情

        Args:
            question_ids: 问题ID列表
            output_csv: 输出CSV文件路径
            start_idx: 起始索引
            max_count: 最大爬取数量，None表示全部
            show_progress: 是否显示进度

        Returns:
            详情数据列表
        """
        self.logger.info("=" * 50)
        self.logger.info("开始详情页爬取任务")
        self.logger.info(f"配置: 起始索引={start_idx}, 最大数量={max_count if max_count else '全部'}, 输出文件={output_csv}")

        if max_count is not None:
            question_ids = question_ids[start_idx:start_idx + max_count]
        else:
            question_ids = question_ids[start_idx:]

        total = len(question_ids)
        if total == 0:
            msg = "没有需要爬取的问题ID"
            print(msg)
            self.logger.warning(msg)
            return []

        self.logger.info(f"待爬取问题数量: {total}")

        details = []
        success_count = 0
        fail_count = 0

        for idx, qid in enumerate(question_ids, 1):
            if show_progress:
                print(f"[{idx}/{total}] 正在爬取问题 {qid}...")
                self.logger.info(f"[{idx}/{total}] 爬取问题ID: {qid}")

            try:
                html = self.get_detail_page(qid)
                detail = self.parse_detail(html, qid)
                details.append(detail)
                success_count += 1

                if show_progress:
                    content_preview = detail["question_content"][:30] if detail["question_content"] else "无内容"
                    has_answers = bool(detail["answer_list"])
                    print(f"    -> 问题: {content_preview}... | 有答案: {'是' if has_answers else '否'}")

            except Exception as e:
                fail_count += 1
                msg = f"-> 失败: {e}"
                if show_progress:
                    print(f"    {msg}")
                self.logger.error(f"问题ID {qid}: {msg}", exc_info=True)
                # 添加失败记录
                details.append({
                    "id": qid,
                    "question_content": "",
                    "answer_list": "",
                    "source_url": f"{self.BASE_URL}/q/{qid}",
                    "error": str(e)
                })

            # 请求间隔
            if idx < total:
                time.sleep(self.delay)

        # 输出统计
        print(f"\n===== 详情爬取完成 =====")
        print(f"总计: {total} 个问题")
        print(f"成功: {success_count}")
        print(f"失败: {fail_count}")
        self.logger.info("=" * 50)
        self.logger.info("详情页爬取任务完成")
        self.logger.info(f"统计: 总计={total}, 成功={success_count}, 失败={fail_count}")

        # 保存结果
        self._save_results(details, output_csv)

        return details

    def _save_results(self, details: List[Dict], csv_path: str, json_path: str = None):
        """保存爬取结果到CSV文件"""
        self.logger.info(f"保存结果到CSV: {csv_path}")
        # 保存CSV（简化版：问题id、问题内容、答案列表、源链接）
        if details:
            fieldnames = ["问题id", "问题内容", "答案列表", "源链接"]
            with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for d in details:
                    row = {
                        "问题id": d.get("id", ""),
                        "问题内容": d.get("question_content", ""),
                        "答案列表": d.get("answer_list", ""),
                        "源链接": d.get("source_url", "")
                    }
                    writer.writerow(row)
            msg = f"已保存CSV到: {csv_path}"
            print(msg)
            self.logger.info(f"{msg}, 共{len(details)}条记录")


def debug_page(page_num: int):
    """调试特定页码 - 用于排查问题"""
    crawler = QihuWendaCrawler()
    logger = crawler.logger

    print(f"调试第 {page_num} 页:")
    logger.info(f"开始调试第 {page_num} 页")
    html = crawler.get_page(page_num)

    print(f"HTML长度: {len(html)} 字符")
    logger.info(f"HTML长度: {len(html)} 字符")

    # 检查是否为空白页
    is_empty = crawler._is_empty_page(html)
    print(f"是否为空页: {is_empty}")
    logger.info(f"是否为空页: {is_empty}")

    # 解析问题
    questions = crawler.parse_question_list(html)
    print(f"解析到 {len(questions)} 条问题")
    logger.info(f"解析到 {len(questions)} 条问题")

    if questions:
        print("前3条问题:")
        for i, q in enumerate(questions[:3], 1):
            print(f"  {i}. {q['title'][:30]}... (ID: {q['id']})")
        logger.debug(f"前3条问题: {[q['title'][:30] for q in questions[:3]]}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "detail":
            # 详情页爬取模式
            csv_path = sys.argv[2] if len(sys.argv) > 2 else "360_qa.csv"
            start_idx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            max_count = int(sys.argv[4]) if len(sys.argv) > 4 else None
            detail_crawler = QihuWendaDetailCrawler(delay=10.0)
            ids = detail_crawler.get_question_ids_from_csv(csv_path)
            detail_crawler.crawl_details(ids, start_idx=start_idx, max_count=max_count)
        else:
            # 调试指定页码
            try:
                page = int(command)
                debug_page(page)
            except ValueError:
                print("用法:")
                print("  python crawler.py          # 爬取问题列表")
                print("  python crawler.py detail [csv_path] [start_idx] [max_count]  # 爬取详情")
                print("  python crawler.py [页码]   # 调试指定页码")
    else:
        main()


def main_detail():
    """主函数 - 从CSV爬取问题详情"""
    import json

    csv_path = input("请输入CSV文件路径 (直接回车默认360_qa.csv): ").strip()
    csv_path = csv_path if csv_path else "360_qa.csv"

    start_idx_str = input("请输入起始索引 (直接回车默认0): ").strip()
    start_idx = int(start_idx_str) if start_idx_str else 0

    max_count_str = input("请输入最大爬取数量 (直接回车表示全部): ").strip()
    max_count = int(max_count_str) if max_count_str else None

    print(f"\n开始爬取详情页...")
    print(f"  - CSV文件: {csv_path}")
    print(f"  - 起始索引: {start_idx}")
    print(f"  - 最大数量: {max_count if max_count else '全部'}")

    crawler = QihuWendaDetailCrawler(delay=10.0)
    crawler.logger.info(f"详情爬取任务: CSV={csv_path}, 起始索引={start_idx}, 最大数量={max_count}")
    ids = crawler.get_question_ids_from_csv(csv_path)
    details = crawler.crawl_details(ids, start_idx=start_idx, max_count=max_count)

    # 输出示例
    if details:
        print("\n===== 结果预览 =====")
        for i, d in enumerate(details[:3], 1):
            print(f"\n[{i}] 问题ID: {d['id']}")
            content = d['question_content'][:50] + "..." if len(d['question_content']) > 50 else d['question_content']
            print(f"    问题内容: {content}")
            if d.get('answer_list'):
                answer_preview = d['answer_list'][:100] + "..." if len(d['answer_list']) > 100 else d['answer_list']
                print(f"    答案列表: {answer_preview}")
            print(f"    源链接: {d.get('source_url', '')}")

        crawler.logger.info(f"结果预览: 前3条数据已显示")
