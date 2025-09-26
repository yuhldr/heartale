'''配置'''

import os
import shutil
import sys

if sys.platform.startswith('win'):
    ld = os.getenv('LOCALAPPDATA', "") or os.getenv('APPDATA', "")
    PATH_CACHE_DIR = os.path.join(ld, "heartale")
else:
    xdg_cache_home = os.getenv('XDG_CACHE_HOME')
    if xdg_cache_home is None:
        home = os.path.expanduser("~")
        xdg_cache_home = os.path.join(home, '.cache')
    PATH_CACHE_DIR = os.path.join(xdg_cache_home, "heartale")
os.makedirs(PATH_CACHE_DIR, exist_ok=True)


def get_cache_mp3(file):
    """_summary_

    Args:
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    return f"{PATH_CACHE_DIR}/mp3/{file}"


os.makedirs(get_cache_mp3(""), exist_ok=True)


def rm_cache_mp3():
    """清理缓存
    """
    mp3_path = get_cache_mp3("")
    if os.path.exists(mp3_path):
        shutil.rmtree(mp3_path)
    os.mkdir(mp3_path)
