'申请github学生包，然后去微软官网申请，可以免费用一年'
# https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts

from heartale.tts import TTS


class AzureTTS(TTS):
    """文本转语音文件
    """

    def __init__(self):
        self.sc = None
        self.aoc = None
        self.ss = None
        self.rs = None
        super().__init__("azure")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, ["azure.cognitiveservices.speech"])

        if len(self.conf["key"]) == 0:
            raise ValueError("请在配置文件中填写Azure的key")
        # pylint: disable=C0415
        import azure.cognitiveservices.speech as speechsdk

        self.aoc = speechsdk.audio.AudioOutputConfig
        self.ss = speechsdk.SpeechSynthesizer
        self.rs = speechsdk.ResultReason.SynthesizingAudioCompleted

        self.sc = speechsdk.SpeechConfig(self.conf["key"], self.conf["region"])

    async def download(self, text, file):
        ssml_text = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
            xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="{self.conf['language']}">
            <voice name="{self.conf['voice']}">
                <prosody rate="{self.conf['rate']}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """

        result = self.ss(self.sc, self.aoc(file))\
            .speak_ssml_async(ssml_text).get()
        if result.reason != self.rs:
            print(f"Speech synthesis failed: {result.reason}")
            raise ValueError(f"Speech synthesis failed: {result.reason}")

        return True
