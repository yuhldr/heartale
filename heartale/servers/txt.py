"""阅读本地txt文件"""
import os
import pathlib
from datetime import datetime

from heartale.servers import BookData, Server
from heartale.tools import (cal_file_md5, detect_encoding, get_data,
                            parse_volumes_and_chapters, save_data)
from heartale.tools.config import PATH_CONFIG_DIR

PATH_FILE = "path_file"
# 第几章
KEY_CHAP_N = "chap_n"
# 这一章第几个字
KEY_CHAP_TXT_POS = "chap_txt_pos"
KEY_ENCODING = "encoding"
LAST_READ_DATE = "last_read_date"


class TxtServer(Server):
    """阅读app相关的webapi"""

    def __init__(self):
        """初始化应用API

        Args:
            conf (dict): 配置 conf["legado"]
        """
        # 书籍位置
        self.path_file = ""
        # 编码格式
        self.ec = ""
        # 阅读进入文件位置
        self.path_read_p = ""
        self.bd = BookData()

        super().__init__("txt")

    async def initialize(self):
        """异步初始化"""
        if PATH_FILE not in self.conf:
            return "请设置待阅读的txt文件所在路径"

        self.path_file = self.conf[PATH_FILE]
        print(f"文件位置：{self.path_file}")
        os.makedirs(f"{PATH_CONFIG_DIR}/txts/", exist_ok=True)

        if not os.path.exists(self.path_file):
            self.bd.update_chap_txts("请检查设置的文件路径是否正确", 0)
            return "路径错误，文件不存在"

        file_ = pathlib.Path(self.path_file)
        self.book_name = file_.stem

        if file_.suffix != ".txt":
            self.bd.update_chap_txts("请检查设置的文件后缀名", 0)
            return f"此方式只支持txt文件，而不是{file_.suffix}"

        md5 = cal_file_md5(self.path_file)
        self.path_read_p = f"{PATH_CONFIG_DIR}/txts/{md5}.json"

        rp = self._get_read_progress()
        self._get_book_encoding(rp)
        chap_n = rp.get(KEY_CHAP_N, 0)
        chap_txt_pos = rp.get(KEY_CHAP_TXT_POS, 0)
        print(f"上次读取的位置：{chap_n}, {chap_txt_pos}")

        chap_names, chap_p2s, chap_content = parse_volumes_and_chapters(
            self._get_book_content(), chap_n)
        self.bd.set_chap_names(chap_names, chap_n, chap_p2s=chap_p2s)

        self.bd.update_chap_txts(chap_content, chap_txt_pos)
        return self.book_name + " " + self.bd.get_chap_name()

    async def next(self):
        """下一步

        Returns:
            str: 需要转音频的文本
        """
        print(f"当前位置：{self.bd.chap_txt_n}/{len(self.bd.chap_txts)}")

        if self.bd.is_chap_end():
            self.bd.chap_n += 1

            self.bd.update_chap_txts(
                self.bd.get_chap_content(self._get_book_content()))
            return self.bd.get_chap_name()

        txt = self.bd.chap_txts[self.bd.chap_txt_n]
        self._save_read_progress()
        self.bd.chap_txt_n += 1

        return txt

    def _get_read_progress(self):
        """读取阅读进度
        """
        data_default = {PATH_FILE: self.path_file,
                        KEY_CHAP_N: 0,
                        KEY_CHAP_TXT_POS: 0}
        data = get_data(self.path_read_p, data_default)
        if data[PATH_FILE] != self.path_file:
            print(f"文件位置不一致：{data[PATH_FILE]} -> {self.path_file}")

        return data

    def _save_read_progress(self):
        """异步保存阅读进度

        Args:
            book_data (dict): 书籍信息

        Raises:
            ValueError: 当进度保存出错时抛出异常
        """

        # 构建请求数据
        data = {
            PATH_FILE: self.path_file,
            KEY_CHAP_N: self.bd.chap_n,
            KEY_CHAP_TXT_POS: self.bd.get_chap_txt_pos(),
            KEY_ENCODING: self.ec,
            LAST_READ_DATE: datetime.now().isoformat(),
        }
        save_data(self.path_read_p, data)

    def _get_book_encoding(self, rp):
        self.ec = detect_encoding(self.path_file)
        if self.ec is None:
            self.ec = self.conf["encoding"]
            if len(self.ec) == 0:
                if KEY_ENCODING not in rp:
                    self.ec = "utf-8"
                self.ec = rp[KEY_ENCODING]

    def _get_book_content(self):
        file_content = ""
        try:
            with open(self.path_file, "r", encoding=self.ec) as f:
                file_content = f.read()
        except (UnicodeDecodeError, UnicodeError):
            with open(self.path_file, "r", encoding=self.ec, errors='ignore') as f:
                file_content = f.read()
            return f"{self.book_name}，txt文件使用{self.ec}解码可能出现错误，请修改配置中解码方法，或核对txt文件"
        return file_content
