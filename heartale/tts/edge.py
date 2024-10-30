"""文本转语音文件"""


from heartale.tools import get_proxy_url
from heartale.tts import TTS


class EdgeTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.com = None
        self.proxy = None
        super().__init__("edge")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["edge_tts"])

        self.proxy = get_proxy_url()
        print(f"使用代理 {self.proxy}")

        import edge_tts  # pylint: disable=C0415
        self.com = edge_tts.Communicate

    async def download(self, text, file):
        print(self.proxy)
        await self.com(text, self.conf["voice"],
                       rate=self.conf["rate"],
                       proxy=self.proxy).save(file)
