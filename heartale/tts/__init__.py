"""文字转语音"""
import asyncio
import copy
import os

from heartale.tools.config import get_config_tts_play


class TTS:
    """获取待阅读文本的基础类
    """

    def __init__(self, key: str):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """

        self.key = key
        self.conf = None

    def set_conf(self, conf):
        """设置配置信息，并可以初始化一些服务，比如import第三方库，防止未使用的TTS导致内存占用过大

        Args:
            conf (_type_): _description_
        """
        self.conf = conf

    async def download(self, text, file):
        """下载
        """
        print(text, file)


async def play_mp3(file_path, conf_all: dict):
    """子线程阅读

    Args:
        file_path (str): 音频文件路径
        conf_all (dict): 所有配置
    """

    codes = copy.copy(get_config_tts_play(conf_all)["code"])
    codes.append(file_path)

    process = await asyncio.create_subprocess_exec(*codes)
    await process.communicate()
    os.remove(file_path)
