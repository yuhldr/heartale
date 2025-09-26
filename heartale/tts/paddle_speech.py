"""文本转语音文件"""


from heartale.tts import HTS


class PaddleSpeechTTS(HTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.tts = None
        super().__init__("paddlespeech")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["paddlespeech"])
        # pylint: disable=C0415
        from paddlespeech.cli.tts.infer import TTSExecutor
        self.tts = TTSExecutor()

    async def download(self, text, file):
        self.tts(text=text, output=file)
