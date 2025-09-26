"""文本转语音文件"""


from heartale.tools import get_proxy_url
from heartale.tts import HTS


class EdgeTTS(HTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.com = None
        self.proxy = None
        self.err = None
        super().__init__("edge")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["edge_tts"])

        self.proxy = get_proxy_url()
        print(f"使用代理 {self.proxy}")

        import edge_tts  # pylint: disable=C0415
        self.com = edge_tts.Communicate
        self.err = edge_tts.exceptions

    async def download(self, text, file):
        if self.com is None or self.err is None:
            raise ValueError("初始化错误")
        try:
            await self.com(text, self.conf["voice"],
                           rate=self.conf["rate"],
                           proxy=self.proxy).save(file)
        except self.err.NoAudioReceived as e:
            print(f"下载失败：{text}\n{str(e)}")
            await self.download(f"文本空，{self.key} 跳过一次", file)
            return None
