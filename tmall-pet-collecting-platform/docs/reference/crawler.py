"""
淘宝推荐商品爬虫

用于从淘宝API获取推荐商品数据
"""

import requests
import json
import hashlib
import os
import csv
import re
from typing import Dict, Optional, Any, List
import logging
import time
from urllib.parse import quote
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaobaoCrawler:
    """淘宝爬虫类"""

    def __init__(self):
        """初始化爬虫"""
        self.base_url = "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/"
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())
        self.app_key = "12574478"
        self._token = None

    def _extract_token(self) -> str:
        """
        从 Cookie 中提取 _m_h5_tk token

        Token 格式: xxx_xxx，取下划线前的部分
        """
        if self._token:
            return self._token

        cookie = self.session.headers.get('cookie', '')
        # 查找 _m_h5_tk 字段
        for item in cookie.split(';'):
            item = item.strip()
            if item.startswith('_m_h5_tk='):
                token_value = item.split('=')[1]
                # 取下划线前的部分
                self._token = token_value.split('_')[0]
                logger.info(f"提取到 token: {self._token[:8]}...")
                return self._token

        # 如果没有找到，使用默认值
        logger.warning("未能从 Cookie 中提取 token，使用默认值")
        self._token = "7707921f826e40e21ed8d016e79ad351"
        return self._token

    def _calculate_sign(self, data: str, timestamp: str) -> str:
        """
        计算签名

        签名算法: md5(token + "&" + timestamp + "&" + appKey + "&" + data)

        Args:
            data: 请求参数中的 data 字段（已 JSON 序列化）
            timestamp: 时间戳字符串

        Returns:
            32位 MD5 签名字符串
        """
        token = self._extract_token()
        # 构建签名字符串
        sign_str = token + "&" + timestamp + "&" + self.app_key + "&" + data
        logger.info(f"签名字符串: {sign_str[:50]}...")

        # 计算 MD5
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        return sign

    def _get_headers(self) -> Dict[str, str]:
        """
        获取请求头

        注意：实际使用时应将敏感信息存储在配置文件或环境变量中
        """
        return {
            'cookie': 't=2ccf9f6d65ef4b7c86e2f160535b961d; thw=cn; xlly_s=1; wk_cookie2=1177731bd34f0a81696b834ebfb11451; wk_unb=UNN13sASRxdOCQ%3D%3D; aui=3389837459; mt=ci=0_0; cna=Jq/TIRTnF24CAd73JVAJEIg4; lgc=hi%5Cu661F%5Cu6B87; dnk=hi%5Cu661F%5Cu6B87; tracknick=hi%5Cu661F%5Cu6B87; mtop_partitioned_detect=1; cookie2=262f9182cd73b229f92d87ae67e64b55; _tb_token_=738bd3116abbe; _samesite_flag_=true; _m_h5_tk=7707921f826e40e21ed8d016e79ad351_1770533010043; _m_h5_tk_enc=f2625da3f635b68ef8d2d3770644e6f1; sca=30c4311b; 3PcFlag=1770525468124; sgcookie=E100DVVmA%2Bqd6wqDP4BWhXPMAzJAsghSuwcHJ7twjZcA4FwaQVNpRqgYapKSBnublYo2UDHlzrJLDDOaC2DglHXRtoNRfcp8ZSf3cu1V4bvBXMg%3D; unb=3389837459; uc1=cookie14=UoYZaqFL1n1VEA%3D%3D&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=VT5L2FSpczFp&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=vt3=F8dD29DnEQIPQu%2FEVjI%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=CyTknzk5&id2=UNN13sASRxdOCQ%3D%3D; csg=0cc72968; cancelledSubSites=empty; cookie17=UNN13sASRxdOCQ%3D%3D; skt=4e30fbce00c8501c; existShop=MTc3MDUyNTQ4Mg%3D%3D; uc4=id4=0%40UgQ9fgRt7CLRvXlpB6r5dEemld1L&nk4=0%40CWM87AhJeP93CdtDcNXxlj0%3D; _cc_=URm48syIZQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E6%AE%8791; _nk_=hi%5Cu661F%5Cu6B87; cookie1=Vv0jEwL%2BUklq9nNg5iifBm1MiY6im9VscyvNz7KURVw%3D; tfstk=gVtZZFX1YcnwEelkULjq4cAEdkjOXil7Qn1fnKvcC1fMhAFDYKfQcAIskiRVTIC15Gx2JoJJHhMOcAI9BiImNbi50dpODQmr6acBKxXA0OAUdyUeBiImOJZmP0J91cqNHijmLMXVIRjcslbnLt6Gmlb0jyVh9tjcmtXGKyXlnP40mIvnLtChiibMiMDFH6fcmiD3pnxaY17iInh74-VbkNfkI6r008BNS_mRToqDYOJFZd0YmoxFQNxUpQ8WkNTDeaK6jmrdfL8hxT9tbkSkITR1OQmuYMvBKI_JJjE5JB-VohbTnvfHbB-OjCg04QSwgaxG8-qXUdfNY9xohzCBY1ODbwD74ZsHVajMR2h1lGWyihda3oAkdLtOJnlztsL1eMXWBcrFqdXc44FAKm0XDFP0uNXdL_MELs7HrfrEG6MbkrQnp95SUYzYkNXdL_MELrUA-BBFNYkP.; isg=BCYmhVS6czl_6SdK60Vobiz0d5yoB2rB8vDSsxDPEsklk8ateJe60Qxl648fO2LZ',
            'referer': 'https://new-s.taobao.com/?_input_charset=utf-8&clientPreloadId=preload_1770477440371&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E9%AB%98%E8%BE%BE%E6%A8%A1%E5%9E%8B&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.search_history.d2&ssid=s5-e&suggest_query=&tab=all&wq=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0'
        }

    def _get_params(self, keyword: str, page: int = 1, total_results: str = "4800",
                     bcoffset: str = "", ntoffset: str = "", source_s: str = "0") -> Dict[str, Any]:
        """
        获取查询参数

        Args:
            keyword: 搜索关键词
            page: 页码
            total_results: 总结果数
            bcoffset: BC偏移量
            ntoffset: NT偏移量
            source_s: 来源标识

        Returns:
            查询参数字典
        """
        timestamp = str(int(time.time() * 1000))

        # 构建搜索参数
        search_params = {
            "device": "HMA-AL00",
            "isBeta": "false",
            "grayHair": "false",
            "from": "nt_history",
            "brand": "HUAWEI",
            "info": "wifi",
            "index": "4",
            "rainbow": "",
            "schemaType": "auction",
            "elderHome": "false",
            "isEnterSrpSearch": "true",
            "newSearch": "false",
            "network": "wifi",
            "subtype": "",
            "hasPreposeFilter": "false",
            "prepositionVersion": "v2",
            "client_os": "Android",
            "gpsEnabled": "false",
            "searchDoorFrom": "srp",
            "debug_rerankNewOpenCard": "false",
            "homePageVersion": "v7",
            "searchElderHomeOpen": "false",
            "search_action": "initiative",
            "sugg": "_4_1",
            "sversion": "13.6",
            "style": "list",
            "ttid": "600000@taobao_pc_10.7.0",
            "needTabs": "true",
            "areaCode": "CN",
            "vm": "nw",
            "countryNum": "156",
            "m": "pc",
            "page": page,
            "n": 48,
            "q": keyword,
            "qSource": "url",
            "pageSource": "a21bo.jianhua/a.search_history.d2",
            "channelSrp": "",
            "tab": "all",
            "pageSize": 48,
            "totalPage": 100,
            "totalResults": total_results,
            "sourceS": source_s,
            "sort": "_coefp",
            "bcoffset": bcoffset,
            "ntoffset": ntoffset,
            "filterTag": "",
            "service": "",
            "prop": "",
            "loc": "",
            "start_price": None,
            "end_price": None,
            "startPrice": None,
            "endPrice": None,
            "itemIds": None,
            "p4pIds": None,
            "p4pS": None,
            "categoryp": "",
            "ha3Kvpairs": None,
            "myCNA": "Jq/TIRTnF24CAd73JVAJEIg4",
            "screenResolution": "2048x1152",
            "viewResolution": "781x1418",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
            "couponUnikey": "",
            "subTabId": "",
            "np": "",
            "clientType": "h5",
            "isNewDomainAb": "false",
            "forceOldDomain": "false"
        }

        # 构建 data 参数
        data_param = json.dumps({
            "appId": "34385",
            "params": json.dumps(search_params, ensure_ascii=False)
        }, separators=(',', ':'))

        # 计算签名
        sign = self._calculate_sign(data_param, timestamp)

        return {
            'jsv': '2.7.4',
            'appKey': self.app_key,
            't': timestamp,
            'sign': sign,
            'api': 'mtop.relationrecommend.wirelessrecommend.recommend',
            'v': '2.0',
            'timeout': '10000',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonp6',
            'data': data_param,
            'bx-ua': 'fast-load'
        }

    def _parse_jsonp_response(self, response_text: str) -> Optional[Dict]:
        """
        解析 JSONP 响应

        Args:
            response_text: JSONP 格式的响应文本，如 "mtopjsonp6({...})"

        Returns:
            解析后的数据字典，失败返回 None
        """
        try:
            # 移除 JSONP 回调函数名
            # 格式: mtopjsonp6({...})
            if 'mtopjsonp' in response_text:
                # 找到第一个 '(' 和最后一个 ')'
                start = response_text.find('(')
                end = response_text.rfind(')')
                if start != -1 and end != -1:
                    json_str = response_text[start + 1:end]
                    return json.loads(json_str)
            return json.loads(response_text)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"JSONP 解析失败: {e}")
            logger.debug(f"响应内容: {response_text[:200]}")
            return None

    def fetch_recommendations(self, keyword: str, page: int = 1, total_results: str = "4800",
                              bcoffset: str = "", ntoffset: str = "", source_s: str = "0") -> Optional[Dict]:
        """
        获取推荐商品数据

        Args:
            keyword: 搜索关键词
            page: 页码，默认为1
            total_results: 总结果数
            bcoffset: BC偏移量
            ntoffset: NT偏移量
            source_s: 来源标识

        Returns:
            响应数据字典，失败时返回None
        """
        try:
            params = self._get_params(keyword, page, total_results, bcoffset, ntoffset, source_s)
            logger.info(f"正在获取关键词 '{keyword}' 第 {page} 页的推荐数据...")

            response = self.session.get(
                self.base_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            logger.info(f"请求成功，状态码: {response.status_code}")

            # 解析 JSONP 响应
            data = self._parse_jsonp_response(response.text)
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return None

    def fetch_all_pages(self, keyword: str, max_pages: int = 10, delay: float = 1.0) -> List[Dict]:
        """
        批量获取多页数据

        Args:
            keyword: 搜索关键词
            max_pages: 最大获取页数
            delay: 每次请求之间的延迟（秒）

        Returns:
            所有页面的商品数据列表
        """
        all_items = []
        total_results = "4800"
        bcoffset = ""
        ntoffset = ""
        source_s = "0"

        for page in range(1, max_pages + 1):
            logger.info(f"正在获取第 {page}/{max_pages} 页...")

            # 获取当前页数据
            result = self.fetch_recommendations(
                keyword=keyword,
                page=page,
                total_results=total_results,
                bcoffset=bcoffset,
                ntoffset=ntoffset,
                source_s=source_s
            )

            if not result:
                logger.error(f"第 {page} 页获取失败")
                break

            # 检查响应状态
            ret = result.get('ret', [])
            if ret and 'FAIL' in str(ret[0]):
                logger.error(f"第 {page} 页 API 返回错误: {ret[0]}")
                break

            # 从 mainInfo 中提取下一页需要的参数
            main_info = result.get('data', {}).get('mainInfo', {})
            if main_info:
                total_results = main_info.get('totalResults', total_results)
                bcoffset = main_info.get('bcoffset', bcoffset)
                ntoffset = main_info.get('ntoffset', ntoffset)
                source_s = main_info.get('sourceS', source_s)
                logger.debug(f"更新参数: totalResults={total_results}, bcoffset={bcoffset}, ntoffset={ntoffset}, source_s={source_s}")

            # 提取商品数据
            items_array = result.get('data', {}).get('itemsArray', [])
            if not items_array:
                logger.warning(f"第 {page} 页没有商品数据，停止获取")
                break

            all_items.extend(items_array)
            logger.info(f"第 {page} 页获取到 {len(items_array)} 个商品，累计 {len(all_items)} 个")

            # 延迟，避免请求过快
            if page < max_pages:
                time.sleep(delay)

        logger.info(f"批量获取完成，共获取 {len(all_items)} 个商品")
        return all_items

    def save_to_file(self, data: Any, filename: str = 'taobao_data.json') -> bool:
        """
        将数据保存到文件

        Args:
            data: 要保存的数据
            filename: 文件名

        Returns:
            保存成功返回True，失败返回False
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到 {filename}")
            return True
        except IOError as e:
            logger.error(f"文件保存失败: {e}")
            return False

    @staticmethod
    def clean_html(text: str) -> str:
        """移除 HTML 标签"""
        if not text:
            return ""
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def extract_item_data(self, item: Dict[str, Any]) -> Dict[str, str]:
        """
        从单个商品数据中提取关键字段

        Args:
            item: 商品数据字典

        Returns:
            提取后的数据字典
        """
        # 基本信息
        item_id = item.get('item_id', '')
        title = self.clean_html(item.get('title', ''))
        nick = item.get('nick', '')

        # 价格信息
        price = item.get('price', '')
        price_show = item.get('priceShow', {})
        price_unit = price_show.get('unit', '')
        price_desc = price_show.get('priceDesc', '')

        # 销量和地区
        real_sales = item.get('realSales', '')
        procity = item.get('procity', '')

        # 图片和链接
        pic_path = item.get('pic_path', '')
        auction_url = item.get('auctionURL', '')

        # 店铺信息
        shop_info = item.get('shopInfo', {})
        shop_title = shop_info.get('title', '')
        shop_tag = item.get('shopTag', '')

        # 标签
        icons = item.get('icons', [])
        icon_tags = []
        for icon in icons:
            text = icon.get('text', '')
            if text:
                icon_tags.append(text)
        tags = ', '.join(icon_tags)

        # 商品属性
        structured_usp = item.get('structuredUSPInfo', [])
        usp_list = []
        for usp in structured_usp:
            prop_name = usp.get('propertyName', '')
            prop_value = usp.get('propertyValueName', '')
            if prop_name and prop_value:
                usp_list.append(f"{prop_name}:{prop_value}")
        properties = ' | '.join(usp_list)

        return {
            '商品ID': item_id,
            '商品标题': title,
            '价格': price,
            '价格单位': price_unit,
            '价格描述': price_desc,
            '卖家昵称': nick,
            '店铺名称': shop_title,
            '店铺标签': shop_tag,
            '销量': real_sales,
            '地区': procity,
            '标签': tags,
            '商品属性': properties,
            '图片链接': pic_path,
            '商品链接': auction_url
        }

    def export_to_csv(self, items: List[Dict], csv_file: str) -> bool:
        """
        将商品数据导出为 CSV 文件

        Args:
            items: 商品数据列表
            csv_file: CSV 文件路径

        Returns:
            导出成功返回 True，失败返回 False
        """
        if not items:
            logger.error("没有数据可导出")
            return False

        # 提取数据
        extracted_data = []
        for item in items:
            try:
                extracted_item = self.extract_item_data(item)
                extracted_data.append(extracted_item)
            except Exception as e:
                logger.warning(f"提取商品数据失败: {e}")
                continue

        # 定义字段顺序
        fieldnames = [
            '商品ID', '商品标题', '价格', '价格单位', '价格描述',
            '卖家昵称', '店铺名称', '店铺标签', '销量', '地区',
            '标签', '商品属性', '图片链接', '商品链接'
        ]

        # 保存为 CSV
        try:
            with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(extracted_data)
            logger.info(f"CSV 文件已保存到 {csv_file}，共 {len(extracted_data)} 条数据")
            return True
        except IOError as e:
            logger.error(f"CSV 文件保存失败: {e}")
            return False

    @staticmethod
    def cleanup_json_files(keyword: str, max_pages: int) -> None:
        """
        清理 JSON 文件

        Args:
            keyword: 搜索关键词
            max_pages: 页数
        """
        files_to_delete = []
        # 添加单页 JSON 文件
        for page in range(1, max_pages + 1):
            files_to_delete.append(f'{keyword}_page{page}.json')
        # 添加合并 JSON 文件
        files_to_delete.append(f'{keyword}_all_pages.json')

        deleted_count = 0
        for filename in files_to_delete:
            if Path(filename).exists():
                try:
                    os.remove(filename)
                    logger.info(f"已删除: {filename}")
                    deleted_count += 1
                except OSError as e:
                    logger.warning(f"删除 {filename} 失败: {e}")

        if deleted_count > 0:
            logger.info(f"清理完成，共删除 {deleted_count} 个 JSON 文件")


def main():
    """主函数"""
    import sys

    crawler = TaobaoCrawler()

    # 示例：搜索高达模型
    keyword = "高达模型"

    # 检查命令行参数
    if len(sys.argv) > 1:
        keyword = sys.argv[1]

    if len(sys.argv) > 2:
        max_pages = int(sys.argv[2])
    else:
        max_pages = 3  # 默认获取3页

    # 批量获取数据
    logger.info(f"开始批量获取 '{keyword}' 的数据，共 {max_pages} 页")
    all_items = crawler.fetch_all_pages(keyword, max_pages=max_pages, delay=1.0)

    if all_items:
        logger.info(f"批量获取完成，共获取 {len(all_items)} 个商品")

        # 导出为 CSV
        csv_file = f'{keyword}.csv'
        if crawler.export_to_csv(all_items, csv_file):
            logger.info(f"数据导出成功: {csv_file}")

            # 清理 JSON 文件
            crawler.cleanup_json_files(keyword, max_pages)
        else:
            logger.error("CSV 导出失败，保留 JSON 文件")
    else:
        logger.error("批量获取失败")


if __name__ == '__main__':
    main()
