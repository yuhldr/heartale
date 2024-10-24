'''配置'''

import os
import shutil


def get_cache_path():
    """_summary_

    Returns:
        _type_: _description_
    """
    return os.getenv("HOME") + "/.cache/bpy/"


if not os.path.exists(get_cache_path()):
    os.mkdir(get_cache_path())


def get_cache_mp3(file):
    """_summary_

    Args:
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    return f"{get_cache_path()}/mp3/{file}"


if not os.path.exists(get_cache_mp3("")):
    os.mkdir(get_cache_mp3(""))


def rm_cache_mp3():
    """清理缓存
    """
    mp3_path = get_cache_mp3("")
    if os.path.exists(mp3_path):
        shutil.rmtree(mp3_path)
    os.mkdir(mp3_path)
