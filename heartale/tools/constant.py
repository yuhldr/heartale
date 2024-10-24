'常量'
from heartale.servers import Server
from heartale.servers.legado import LegadoServer
from heartale.servers.txt import TxtServer
from heartale.tts import TTS
from heartale.tts.edge import EdgeTTS
from heartale.tts.ms_azure import AzureTTS


def get_servers() -> list[Server]:
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        LegadoServer(),
        TxtServer(),
    ]


def get_ttses() -> list[TTS]:
    """获取所有服务

    Returns:
        dict: 所有服务
    """

    return [
        EdgeTTS(),
        AzureTTS(),
    ]
