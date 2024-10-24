'申请github学生包，然后去微软官网申请，可以免费用一年'
# https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts

import azure.cognitiveservices.speech as speechsdk

from heartale.tts import TTS


class AzureTTS(TTS):
    """文本转语音文件
    """

    def __init__(self):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """
        super().__init__("azure")

    async def download(self, text, file):
        """_summary_

        Args:
            text (str): _description_
            file (str): _description_

        Returns:
            bool: _description_
        """

        if len(self.conf["key"]) == 0:
            print("请在配置文件中填写Azure的key")
            return "请在配置文件中填写Azure的key"

        speech_config = speechsdk.SpeechConfig(
            subscription=self.conf["key"], region=self.conf["region"])

        audio_config = speechsdk.audio.AudioOutputConfig(filename=file)
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config)

        # 使用SSML设置语音速度
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
        result = speech_synthesizer.speak_ssml_async(ssml_text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesis failed: {result.reason}")
            raise ValueError(f"Speech synthesis failed: {result.reason}")

        return True
