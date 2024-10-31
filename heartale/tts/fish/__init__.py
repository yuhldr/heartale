"""fish speech"""

from heartale.tts import TTS


class FishTTS(TTS):
    """获取待阅读文本的基础类
    """

    def __init__(self):
        self.com = None
        self.data = {}
        super().__init__("fish")

    def set_conf(self, conf, py_libs=None):
        super().set_conf(conf, [])
        # pylint: disable=C0415
        from heartale.tts.fish.commons import ServeReferenceAudio
        from heartale.tts.fish.file import audio_to_bytes, read_ref_text

        references = []
        for a, t in self.conf.get("audio_text", {}).items():
            references.append(ServeReferenceAudio(
                audio=audio_to_bytes(a), text=read_ref_text(t)))

        self.data = {
            # "text": text,
            "references": references,
            "reference_id": None,
            "normalize": True,
            "format": "wav",
            "mp3_bitrate": 64,
            "opus_bitrate": -1000,
            "max_new_tokens": 0,
            "chunk_length": 200,
            "top_p": 0.7,
            "repetition_penalty": 1.2,
            "temperature": 0.7,
            "streaming": False,
            "use_memory_cache": "on-demand",
            "seed": None,
        }

    async def download(self, text, file):
        if text[-1] != "。":
            text += "。"
        # pylint: disable=C0415
        import aiohttp
        import ormsgpack

        # audio_text = {
        #     "/home/yuh/a13.mp3": "英老头一指点去，他的身躯突然炸开，四分五裂，元神被斩 ，死于非命。其他诸多神族心中悚然，急忙各自后退。"
        # }
        from heartale.tts.fish.commons import ServeTTSRequest
        self.data["text"] = text
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.conf["url_tts"],
                data=ormsgpack.packb(ServeTTSRequest(**self.data),
                                     option=ormsgpack.OPT_SERIALIZE_PYDANTIC),
                headers={
                    "authorization": "Bearer YOUR_API_KEY",
                    "content-type": "application/msgpack",
                },
            ) as response:
                if response.status == 200:
                    with open(file, "wb") as audio_file:
                        audio_file.write(await response.read())
                    print(f"Audio has been saved to '{file}'.")
                else:
                    print(f"Request failed with status code {response.status}")

                    error_data = await response.json()  # 异步读取 JSON
                    print(error_data)
