"""文字转语音"""
import asyncio
import copy
import os

from heartale.tools import check_library_installed
from heartale.tools.config import get_config_tts_play


class HTS:
    """获取待阅读文本的基础类
    """

    def __init__(self, key: str):
        """_summary_

        Args:
            key (str): 用于配置中区分使用本地什么服务
        """

        self.key = key
        self.conf = {}

    def set_conf(self, conf, py_libs=None):
        """设置配置信息，并可以初始化一些服务，比如import第三方库，防止未使用的TTS导致内存占用过大

        Args:
            conf (dict): 配置信息
            py_libs (list, optional): 依赖的第三方库. Defaults to None.

        Raises:
            ImportError: _description_
        """
        self.conf = conf
        if py_libs is not None:
            for py_lib in py_libs:
                if not check_library_installed(py_lib):
                    raise ImportError(f"请安装{py_lib}库: pip install {py_lib}")

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
