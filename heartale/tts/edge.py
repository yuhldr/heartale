"""文本转语音文件"""


from heartale.tts import TTS


class EdgeTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.communicate = None
        super().__init__("edge")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["edge_tts"])
        import edge_tts  # pylint: disable=C0415
        self.communicate = edge_tts.Communicate

    async def download(self, text, file):
        await self.communicate(
            text, self.conf["voice"], rate=self.conf["rate"]).save(file)
