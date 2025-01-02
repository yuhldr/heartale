'fish-speech内置'
from typing import List, Literal, Optional

from pydantic import BaseModel


class ServeReferenceAudio(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    audio: bytes
    text: str

    def test(self):
        """_summary_
        """
        print("xx")

    def test2(self):
        """_summary_
        """
        print("xx")


class ServeTTSRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    text: str
    # Annotated[int, conint(ge=100, le=300, strict=True)]
    chunk_length: int = 200
    # Audio format
    format: Literal["wav", "pcm", "mp3"] = "wav"
    mp3_bitrate: Literal[64, 128, 192] = 128
    # References audios for in-context learning
    references: List[ServeReferenceAudio] = []
    # Reference id
    # For example, if you want use https://fish.audio/m/7f92f8afb8ec43bf81429cc1c9199cb1/
    # Just pass 7f92f8afb8ec43bf81429cc1c9199cb1
    reference_id: str = None
    seed: int = None
    use_memory_cache: Literal["on-demand", "never"] = "never"
    # Normalize text for en & zh, this increase stability for numbers
    normalize: bool = True
    mp3_bitrate: Optional[int] = 64
    opus_bitrate: Optional[int] = -1000
    # Balance mode will reduce latency to 300ms, but may decrease stability
    latency: Literal["normal", "balanced"] = "normal"
    # not usually used below
    streaming: bool = False
    max_new_tokens: int = 1024
    # Annotated[float, Field(ge=0.1, le=1.0, strict=True)]
    top_p: float = 0.7
    # Annotated[float, Field(ge=0.9, le=2.0, strict=True)]
    repetition_penalty: float = 1.2
    # Annotated[float, Field(ge=0.1, le=1.0, strict=True)]
    temperature: float = 0.7

    def test(self):
        """_summary_
        """
        print("xx")

    def test2(self):
        """_summary_
        """
        print("xx")
