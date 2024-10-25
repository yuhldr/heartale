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

        super().__init__("gtts")

    async def download(self, text, file):
        """异步文本转音频，并保存本地

        Args:
            text (str): 文本
            file (str): 保存的音频文件
        """
        from gtts import gTTS  # pylint: disable=C0415

        gTTS(text, lang=self.conf['language']).save(file)
