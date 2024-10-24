"""阅读app 相关的webapi"""
import datetime
import json
import time

import aiohttp

from heartale.servers import Server
from heartale.tools import data2url, split_text

# 常量定义
CHAP_POS = "durChapterPos"
CHAP_INDEX = "durChapterIndex"
CHAP_TITLE = "durChapterTitle"


def get_base_url(conf):
    """_summary_

    Args:
        conf (_type_): _description_

    Returns:
        str: _description_
    """
    return f'http://{conf["ip"]}:{conf["port"]}'

def bu(book_data: dict):
    """_summary_

    Args:
        book_data (dict): _description_

    Returns:
        str: _description_
    """
    return f'url={data2url(book_data["bookUrl"])}'


class LegadoServer(Server):
    """阅读app相关的webapi"""

    def __init__(self):
        """初始化应用API

        Args:
            conf (dict): 配置 conf["legado"]
        """
        # 书籍信息
        self.book_data = None
        # 章节名字
        self.cls = None

        # 章节序号，按照self.cls计算的
        self.chap_n = 0

        # 要阅读的，并且分割好的文本list
        self.txts = []
        # 当前读到txts的第几个了
        self.txt_n = 0
        # 每个 txt_n 对应的在原文中的位置
        self.p2s = []
        super().__init__("legado")

    async def initialize(self):
        """异步初始化"""

        self.book_data = await self.get_book_shelf(0)

        self.cls = await self.get_chapter_list(self.book_data)
        self.cls = self.cls[self.book_data[CHAP_INDEX]:]
        self.book_name = self.book_data["name"]

        # 只取之后的章节名字，最多100章
        if len(self.cls) > 100:
            self.cls = self.cls[:100]

        return self.book_name

    async def next(self):
        """下一步

        Returns:
            _type_: _description_
        """

        if self.txt_n == len(self.txts):
            # 第一个是标题
            if len(self.txts) > 1:
                self.txt_n = 0
                self.chap_n += 1
                self.book_data[CHAP_POS] = 0
                self.book_data[CHAP_INDEX] += 1
                self.book_data[CHAP_TITLE] = self.cls[self.chap_n]

            book_txt = await self.get_book_txt(self.book_data)
            self.txts, self.p2s, self.txt_n = split_text(
                book_txt, self.book_data[CHAP_POS])

            return self.cls[self.chap_n]

        txt = self.txts[self.txt_n]
        self.book_data[CHAP_POS] = self.p2s[self.txt_n]
        await self.save_book_progress(self.book_data)
        self.txt_n += 1
        return txt

    async def get_book_shelf(self, book_n: int):
        """异步获取书架信息

        Args:
            book_n (int): 第几本书

        Returns:
            dict: 书籍信息
        """
        url = f"{get_base_url(self.conf)}/getBookshelf"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                resp_json = await response.json(content_type=None)

        return resp_json["data"][book_n]

    async def get_chapter_list(self, book_data: dict):
        """异步获取书章节目录

        Args:
            book_data (dict): 书籍信息

        Returns:
            list: 章节目录，包含title等
        """
        url = f"{get_base_url(self.conf)}/getChapterList?{bu(book_data)}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                resp_json = await response.json(content_type=None)

        return [d["title"] for d in resp_json["data"]]

    async def get_book_txt(self, book_data: dict):
        """异步获取书某一章节的文本

        Args:
            book_data (dict): 书籍信息

        Returns:
            str: 某一章节的文字
        """
        url = f"{get_base_url(self.conf)}/getBookContent"
        params = f"{bu(book_data)}&index={book_data[CHAP_INDEX]}"

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}?{params}", timeout=10) as response:
                resp_json = await response.json(content_type=None)

        return resp_json["data"]

    async def save_book_progress(self, book_data: dict):
        """异步保存阅读进度

        Args:
            book_data (dict): 书籍信息

        Raises:
            ValueError: 当进度保存出错时抛出异常
        """
        # 获取当前时间戳（毫秒）
        dct = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)

        # 构建请求数据
        data = {
            "name": book_data["name"],
            "author": book_data["author"],
            CHAP_INDEX: book_data[CHAP_INDEX],
            CHAP_POS: book_data[CHAP_POS],
            "durChapterTime": dct,
            CHAP_TITLE: book_data[CHAP_TITLE],
        }

        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{get_base_url(self.conf)}/saveBookProgress",
                                    data=json_data,
                                    headers=headers,
                                    timeout=10) as response:
                resp_json = await response.json(content_type=None)

                if not resp_json["isSuccess"]:
                    raise ValueError(f'进度保存错误！\n{resp_json["errorMsg"]}')
