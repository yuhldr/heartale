"""配置"""
import os

from heartale.tools import get_data, save_data

PATH_CONFIG_DIR = f'{os.getenv("HOME")}/.config/heartale/'
os.makedirs(PATH_CONFIG_DIR, exist_ok=True)

PATH_CONFIG = f'{PATH_CONFIG_DIR}/config.json'

CONFIG_DATA = None


DEFAULT_CONFIG = {
    "version": 1,
    "server": {
        "key": "txt",
        "legado": {
            "ip": "192.168.1.6",
            "port": "1122"
        },
        "txt": {
            "path_file": "/tmp/test.txt",
            "encoding": ""
        }
    },
    "tts": {
        "play": {
            "code": [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet"
            ]
        },
        "download": {
            "key": "edge",
            "edge": {
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+30%"
            },
            "azure": {
                "key": "",
                "region": "japanwest",
                "language": "zh-CN",
                "voice": "zh-CN-XiaoxiaoNeural",
                "rate": "+30%"
            },
            "gtts": {
                "language": "zh-CN"
            },
            "coqui": {
                "model": "tts_models/zh-CN/baker/tacotron2-DDC-GST"
            },
            "paddlespeech":{},
        }
    }
}


def get_config(path=PATH_CONFIG):
    """获取配置

    Args:
        path (_type_, optional): _description_. Defaults to PATH_CONFIG.

    Returns:
        dict: 配置数据
    """

    if not os.path.exists(path):
        print("配置文件不存在，已创建默认配置文件")
        save_data(PATH_CONFIG, DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    data = get_data(path)
    if "version" not in data or data["version"] != DEFAULT_CONFIG["version"]:
        save_data(PATH_CONFIG, DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    return data


def get_config_server(conf_all):
    """获取服务配置

    Args:
        conf_all (dict): 配置数据

    Returns:
        dict: 服务配置
    """

    conf_servers = conf_all["server"]
    conf_server_key = conf_servers["key"]
    conf_server = conf_servers[conf_server_key]

    return conf_server_key, conf_server


def get_config_tts_play(conf_all):
    """获取tts配置

    Args:
        conf_all (dict): 配置数据

    Returns:
        dict: tts配置
    """

    return conf_all["tts"]["play"]


def get_config_tts_download(conf_all):
    """获取tts配置

    Args:
        conf_all (dict): 配置数据

    Returns:
        dict: tts配置
    """

    conf_ttss = conf_all["tts"]["download"]
    conf_tts_key = conf_ttss["key"]
    conf_tts = conf_ttss[conf_tts_key]
    return conf_tts_key, conf_tts
