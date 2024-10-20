"""主文件"""
import asyncio
import time

from servers import Server
from tools.cache import get_cache_mp3, rm_cache_mp3
from tools.config import get_config, get_config_server, get_config_tts_download
from tools.constant import get_servers, get_ttses
from tts import TTS, play_mp3


def get_server(conf_all) -> Server:
    """基础类的扩展

    Args:
        conf_all (dict): 完整配置

    Returns:
        Server: _description_
    """
    key, conf_server = get_config_server(conf_all)

    for s in get_servers():
        if s.key == key:
            s.set_conf(conf_server)
            return s

    print(f"未知的服务 {key}")
    return None

def get_tts(conf_all) -> TTS:
    """获取tts服务

    Args:
        conf_all (dict): _description_

    Returns:
        TTS: _description_
    """

    key, conf_tts = get_config_tts_download(conf_all)

    for tts in get_ttses():
        if tts.key == key:
            tts.set_conf(conf_tts)
            return tts

    print(f"未知的服务 {key}")
    return None


def print_test(i, chap, text, file):
    """_summary_

    Args:
        i (_type_): _description_
        chap (_type_): _description_
        text (_type_): _description_
        file (_type_): _description_
    """
    print(f"\n\n*** {i}/{chap} ***")
    print(file)
    if len(text) > 20:
        print(f"{text[:20]} ...")
    else:
        print(text[:20])


async def main(chap=1000, play_min=100):
    """主函数，两个条件只要满足一个就停止

    Args:
        chap (int, optional): 默认听1000段落，自动停止. Defaults to 1000.
        play_min (int, optional): 默认播放100分钟，读完当前章节自动停止. Defaults to 100.
    """
    # https://github.com/gedoor/legado
    # 获取当前第一本书的信息
    st = time.time()
    rm_cache_mp3()

    conf = get_config()

    tts = get_tts(conf)
    lg = get_server(conf)

    # 下载和播放章节
    mp3_file = f'{get_cache_mp3(f"{time.time()}")}.mp3'
    await tts.download(await lg.initialize(), mp3_file)

    # 默认听100章节，自动停止
    for _i in range(chap):
        # 默认播放100分钟，一段结束再停止
        if time.time() - st > play_min * 60:
            print(f"阅读时间{(time.time() - st)/60}分钟 > {play_min}分钟")
            break

        # 并行播放和下载任务
        task_play = play_mp3(mp3_file, conf)

        text = await lg.next()
        print_test(_i, chap, text, mp3_file)

        mp3_file = f'{get_cache_mp3(f"{time.time()}")}.mp3'
        task_download = tts.download(text, mp3_file)

        await asyncio.gather(task_play, task_download)


async def test_play():
    """测试tts和mpv播放音频"""
    txt = "恭喜！配置成功！快打开阅读app，并修改ip地址吧！"
    file = "test.webm"
    conf = get_config()

    await get_tts(conf).download(txt, file)
    await play_mp3(file, conf)


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(test_play())
