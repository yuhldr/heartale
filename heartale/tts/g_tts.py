"""不推荐，很机器人"""


from heartale.tts import TTS


class GTTS(TTS):
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
        """异步文本转音频，并保存本地

        Args:
            text (str): 文本
            file (str): 保存的音频文件
        """
        self.gtts(text, lang=self.conf["language"]).save(file)
