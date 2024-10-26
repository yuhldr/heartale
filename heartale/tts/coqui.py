"""转中文有些问题，容易跳词"""


from heartale.tts import TTS


class CoquiTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """
        self.tts = None
        super().__init__("coqui")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["torch", "TTS"])
        import torch  # pylint: disable=C0415
        from TTS.api import TTS as Ctts  # pylint: disable=C0415

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using {device} for TTS")
        self.tts = Ctts(self.conf["model"]).to(device)

    async def download(self, text, file):
        """异步文本转音频，并保存本地

        Args:
            text (str): 文本
            file (str): 保存的音频文件
        """
        self.tts.tts_to_file(text=text, file_path=file)
