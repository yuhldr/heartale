'常量'
from heartale.servers.legado import LegadoServer
from heartale.servers.txt import TxtServer
from heartale.tts.coqui import CoquiTTS
from heartale.tts.edge import EdgeTTS
from heartale.tts.fish import FishTTS
from heartale.tts.g_tts import GTTS
from heartale.tts.ms_azure import AzureTTS
from heartale.tts.paddle_speech import PaddleSpeechTTS


def get_servers():
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        LegadoServer(),
        TxtServer(),
    ]


def get_ttses():
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        EdgeTTS(),
        AzureTTS(),
        GTTS(),
        CoquiTTS(),
        PaddleSpeechTTS(),
        FishTTS()
    ]
