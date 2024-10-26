"""文本转语音文件"""


from heartale.tts import TTS


class EdgeTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """
        self.communicate = None
        super().__init__("edge")

    def set_conf(self, conf):
        """设置配置

        Args:
            conf (dict): 配置
        """
        super().set_conf(conf)
        import edge_tts  # pylint: disable=C0415
        self.communicate = edge_tts.Communicate

    async def download(self, text, file):
        """异步文本转音频，并保存本地

        Args:
            text (str): 文本
            file (str): 保存的音频文件
        """
        await self.communicate(
            text, self.conf["voice"], rate=self.conf["rate"]).save(file)
