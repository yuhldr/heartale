"""不推荐，很机器人"""


from heartale.tts import TTS


class GTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """
        self.gtts = None

        super().__init__("gtts")

    def set_conf(self, conf):
        super().set_conf(conf)

        from gtts import gTTS  # pylint: disable=C0415
        self.gtts = gTTS

    async def download(self, text, file):
        """异步文本转音频，并保存本地

        Args:
            text (str): 文本
            file (str): 保存的音频文件
        """
        self.gtts(text, lang=self.conf["language"]).save(file)
