'''获取文本并自动跳转的配置'''

from heartale.tools import split_text


class BookData():
    """_summary_
    """

    def __init__(self):
        # 章节目录
        self.chap_names = []
        # 章节目录所在位置
        self.chap_p2s = []
        # 这次是从第几个章节开始读的
        self.chap_n0 = 0
        # 现在是第几个章节
        self.chap_n = 0
        # 某章节的文本分割
        self.chap_txts = []
        # 某章节的文本分割所在位置
        self.chap_txt_p2s = [0]
        # 某章节的文本分割位置
        self.chap_txt_n = 0

    def set_chap_names(self, chap_names, chap_n, chap_p2s=None):
        """初始化数据

        Args:
            chap_names (list): 章节名
            chap_n (int): 上次读到哪个章节了
            chap_txt_pos (int, optional): 上次读到这个的哪个位置. Defaults to -1.
            chap_p2s (list, optional): 章节在全文中的分割位置. Defaults to None.
        """
        # 防止保存数据太多
        self.chap_n0 = chap_n
        self.chap_n = self.chap_n0

        self.chap_names = chap_names[self.chap_n:200]
        if chap_p2s is not None:
            self.chap_p2s = chap_p2s[self.chap_n:200]
        else:
            self.chap_p2s = None

    def get_chap_name(self):
        """获取章节名字"""
        return self.chap_names[self.chap_n-self.chap_n0]

    def update_chap_txts(self, chap_content, chap_txt_pos=0):
        """分割章节的文本

        Args:
            chap_content (str): 章节文本
            chap_txt_pos (int): 已经读到这个章节的什么位置
        """
        self.chap_txts, self.chap_txt_p2s, self.chap_txt_n = \
            split_text(chap_content, chap_txt_pos)

    def get_chap_content(self, book_content):
        """获取self.chap_n的章节内容

        Args:
            book_content (str): 书的完整内容

        Returns:
            str: self.chap_n章节的内容
        """
        if self.chap_p2s is None:
            print("未设置")
        n = self.chap_n - self.chap_n0
        return book_content[self.chap_p2s[n]:self.chap_p2s[n+1]]

    def get_chap_txt_pos(self):
        """本章节的位置，需要保存

        Returns:
            _type_: _description_
        """
        return self.chap_txt_p2s[self.chap_txt_n]

    def is_chap_end(self):
        """这一章节是不是要结束了

        Returns:
            _type_: _description_
        """
        if self.chap_txt_n >= len(self.chap_txts):
            return True
        return False


class Server:
    """获取待阅读文本的基础类
    """

    def __init__(self, key: str):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """

        self.key = key
        # 书名
        self.book_name = ""
        self.conf = None

    def set_conf(self, conf):
        """设置配置信息"""
        self.conf = conf

    async def initialize(self):
        """异步初始化一些操作

        Returns:
            str: 比如书名等待阅读的文本
        """
        if not self.conf:
            print("请先设置配置信息")
        return "initialize"

    async def next(self):
        """接下来要阅读的文本，并保存本地阅读进度等信息
        """
        print("next")
        return "每次调用请自动刷新文本，并保存阅读信息"
