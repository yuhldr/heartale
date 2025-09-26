"""阅读app 相关的webapi"""
import datetime
import json
import time

import aiohttp

from heartale.servers import BookData, Server
from heartale.tools import data2url

# 常量定义
CHAP_POS = "durChapterPos"
CHAP_INDEX = "durChapterIndex"
CHAP_TITLE = "durChapterTitle"
CHAP_TXT_N = "durChapterTxtN"
TIMEOUT = aiohttp.ClientTimeout(total=10)


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
        self.book_data = {}
        self.bd = BookData()

        super().__init__("legado")

    async def initialize(self):

        self.book_data = await self._get_book_shelf(0)
        self.book_name = self.book_data["name"]

        self.bd.set_chap_names(await self._get_chapter_list(self.book_data),
                               self.book_data[CHAP_INDEX])
        self.bd.update_chap_txts(await self._get_book_txt(self.book_data),
                                 self.book_data[CHAP_POS])

        return self.book_name + " " + self.bd.get_chap_name()

    async def next(self):
        """下一步

        Returns:
            _type_: _description_
        """
        if self.bd.is_chap_end():
            self.bd.chap_n += 1
            s = self.bd.get_chap_name()

            self.book_data[CHAP_POS] = 0
            self.book_data[CHAP_INDEX] = self.bd.chap_n
            self.book_data[CHAP_TITLE] = s

            self.bd.update_chap_txts(await self._get_book_txt(self.book_data))

            return s

        txt = self.bd.chap_txts[self.bd.chap_txt_n]
        await self._save_book_progress(self.book_data)
        self.bd.chap_txt_n += 1

        return txt

    async def _get_book_shelf(self, book_n: int):
        """异步获取书架信息

        Args:
            book_n (int): 第几本书

        Returns:
            dict: 书籍信息
        """
        url = f"{get_base_url(self.conf)}/getBookshelf"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=TIMEOUT) as response:
                resp_json = await response.json(content_type=None)

        return resp_json["data"][book_n]

    async def _get_chapter_list(self, book_data: dict):
        """异步获取书章节目录

        Args:
            book_data (dict): 书籍信息

        Returns:
            list: 章节目录，包含title等
        """
        url = f"{get_base_url(self.conf)}/getChapterList?{bu(book_data)}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=TIMEOUT) as response:
                resp_json = await response.json(content_type=None)

        return [d["title"] for d in resp_json["data"]]

    async def _get_book_txt(self, book_data: dict):
        """异步获取书某一章节的文本

        Args:
            book_data (dict): 书籍信息

        Returns:
            str: 某一章节的文字
        """
        url = f"{get_base_url(self.conf)}/getBookContent"
        params = f"{bu(book_data)}&index={book_data[CHAP_INDEX]}"

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}?{params}", timeout=TIMEOUT) as response:
                resp_json = await response.json(content_type=None)

        return resp_json["data"]

    async def _save_book_progress(self, book_data: dict):
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
            "name": self.book_name,
            "author": book_data["author"],
            CHAP_INDEX: self.bd.chap_n,
            CHAP_POS: self.bd.get_chap_txt_pos(),
            "durChapterTime": dct,
            CHAP_TITLE: self.bd.get_chap_name(),
        }

        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{get_base_url(self.conf)}/saveBookProgress",
                                    data=json_data,
                                    headers=headers,
                                    timeout=TIMEOUT) as response:
                resp_json = await response.json(content_type=None)

                if not resp_json["isSuccess"]:
                    raise ValueError(f'进度保存错误！\n{resp_json["errorMsg"]}')
