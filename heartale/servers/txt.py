"""阅读本地txt文件"""
import os
import pathlib

from heartale.servers import Server
from heartale.tools import cal_file_md5, get_data, save_data, split_text
from heartale.tools.config import PATH_CONFIG_DIR

PATH_FILE = "path_file"
KEY_POS = "pos"


class TxtServer(Server):
    """阅读app相关的webapi"""

    def __init__(self):
        """初始化应用API

        Args:
            conf (dict): 配置 conf["legado"]
        """
        # 书籍位置
        self.path_file = ""
        # 阅读进入文件位置
        self.path_read_p = ""

        # 要阅读的，并且分割好的文本list
        self.txts = []
        # 当前读到txts的第几个了
        self.txt_n = 0
        # 每个 txt_n 对应的在原文中的位置
        self.p2s = []
        super().__init__("txt")

    async def initialize(self):
        """异步初始化"""
        if PATH_FILE not in self.conf:
            return "请设置待阅读的txt文件所在路径"

        self.path_file = self.conf[PATH_FILE]
        print(f"文件位置：{self.path_file}")

        if not os.path.exists(self.path_file):
            self.txts, self.p2s, self.txt_n = ["请检查设置的文件路径是否正确"], [0], 0
            return "路径错误，文件不存在"

        file_ = pathlib.Path(self.path_file)
        self.book_name = file_.stem

        if file_.suffix != ".txt":
            self.txts, self.p2s, self.txt_n = ["请检查设置的文件后缀名"], [0], 0
            return f"此方式只支持txt文件，而不是{file_.suffix}"

        md5 = cal_file_md5(self.path_file)
        self.path_read_p = f"{PATH_CONFIG_DIR}/txts/{md5}.json"

        pos = self._get_read_progress()[KEY_POS]
        print(f"上次读取的位置：{pos}")

        with open(self.path_file, "r", encoding="utf-8", errors='ignore') as f:
            self.txts, self.p2s, self.txt_n = split_text(f.read(), pos)
        print(len(self.txts), len(self.p2s), self.txt_n)

        return self.book_name

    async def next(self):
        """下一步

        Returns:
            str: 需要转音频的文本
        """
        print(f"当前位置：{self.txt_n}")
        txt = self.txts[self.txt_n]
        self._save_read_progress()

        if self.txt_n >= len(self.txts):
            return "已经读完了"

        self.txt_n += 1
        return txt

    def _get_read_progress(self):
        """读取阅读进度
        """
        data_default = {PATH_FILE: self.path_file, KEY_POS: 0}
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
            KEY_POS: self.p2s[self.txt_n],
        }

        save_data(self.path_read_p, data)
