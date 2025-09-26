"""不推荐，很机器人"""


from heartale.tts import HTS


class GTTS(HTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.gtts = None

        super().__init__("gtts")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["gtts"])

        from gtts import gTTS  # pylint: disable=C0415
        self.gtts = gTTS

    async def download(self, text, file):
        self.gtts(text, lang=self.conf["language"]).save(file)
