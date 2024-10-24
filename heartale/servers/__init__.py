'''获取文本并自动跳转的配置'''


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
