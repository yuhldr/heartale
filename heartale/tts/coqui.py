"""转中文有些问题，容易跳词"""


import re

from heartale.tts import HTS


class CoquiTTS(HTS):
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
        from TTS.api import TTS  # pylint: disable=C0415
        self.tts = TTS(self.conf["model"]).to(self.conf["device"])

    async def download(self, text, file):

        text = re.sub(r'[“”]', '', text)
        text = re.sub(r'[…？！\n]', '。', text)
        if text[-1] != "。":
            text += "。"
        if self.tts is None:
            raise ValueError("初始化错误")
        self.tts.tts_to_file(text=text, file_path=file)
