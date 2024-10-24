"""文本转语音文件"""

import edge_tts

from heartale.tts import TTS


class EdgeTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """

        super().__init__("edge")

    async def download(self, text, file):
        """异步文本转音频，并保存本地

        Args:
            text (str): 文本
            file (str): 保存的音频文件
        """
        communicate = edge_tts.Communicate(
            text, self.conf["voice"], rate=self.conf["rate"])
        await communicate.save(file)
