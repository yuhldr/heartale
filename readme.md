# 摸鱼听书

> 写程序很多时候是重复工作，听音乐没细胞，那就听听书洗洗脑子吧

## 原因

> [阅读 app](https://github.com/gedoor/legado) 听书很方便，但是我喜欢带着电脑上的头戴式耳机，所以想在电脑上听书

- 需要结合 [阅读 app](https://github.com/gedoor/legado)
- 可以免费用 `微软晓晓听书`
- 阅读进度与手机同步

> 👍 现在也支持阅读本地 txt 文件，并自动记录阅读进度，中断以后继续朗读而不重头开始

## 使用方法

如果你在使用 `python3` 下面的很容易

### 环境配置

> 只需配置一次

1. [这里](https://github.com/yuhldr/heartale/releases/tag/beta)下载并安装 `heartale*.whl`

   非 linux 系统可能需要设置播放程序，看最后详细说明

2. 测试是否修改成功

   终端输入

   ```bash
   echo "配置成功！" > /tmp/test.txt && heartale
   ```

   如果听到 "test，配置成功"，说明没问题

### 朗读类型

默认 `txt`，设置中

```json
"server": {
    "key": "txt",
...
}
```

#### 本地 txt 文件

修改本地配置 `~/.config/bpy/config.json`，其中的

```json
"txt":{
    "path_file": "/tmp/test.txt"
}
```

中的 `/tmp/test.txt` 改为 你的书籍文件所在路径

#### 阅读 app

1. 打开 `阅读app` 的 web 服务

   手机与电脑同一个`局域网`，然后打开 [阅读 app](https://github.com/gedoor/legado)，设置中点开 `Web服务`，注意那个 ip 地址（`:` 后面是端口）

2. 修改本地配置文件 `~/.config/bpy/config.json`

   其中

   ```json
   "ip": "192.168.1.6",
   "port": "1122"
   ```

   里面的 `192.168.1.6` 改成刚才你看到的 `ip`，端口 `1122` 一般不用改

3. 修改如下内容中的 `txt` 为 `legado`

   ```json
   "server": {
       "key": "txt",
   ...
   }
   ```

### 运行

终端运行

```bash
heartale
```

### 其他配置

配置文件路径

```bash
~/.config/bpy/config.json
```

完整配置文件，如果修改错误，可以这里找到原始文件，还原

```json
{
  "version": 1,
  "server": {
    "key": "txt",
    "legado": {
      "ip": "192.168.1.6",
      "port": "1122"
    },
    "txt": {
      "path_file": "/tmp/test.txt"
    }
  },
  "tts": {
    "play": {
      "code": ["paplay"]
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
      }
    }
  }
}
```

### 音频播放程序

默认针对 linux，使用 `paplay`，资源消耗极小

```json
"tts": {
    "play": {
        "code": [
            "paplay"
        ]
    },
...
}
```

可以用 ffmpeg

```json
"tts": {
    "play": {
        "code": ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]
    },
    ...
}
```

也可以用 `mpv`

```json

"tts": {
    "play": {
        "code": ["mpv"]
    },
    ...
}
```

#### TTS 转语音

- tts-edge

  > 免费，不用设置密钥，但是音色少

  ```py
  {
      # 支持的语言和音色：edge-tts --list-voices
      "voice": "zh-CN-XiaoxiaoNeural",
      # 语速
      "rate": "+30%"
  }
  ```

  推荐的音色：

  - XiaoxiaoNeural

- azure

  > 学生有免费额度，必须申请并设置密钥 🔑，音色更多

  ```py
  {
      # 密钥必须设置
      "key": "你自己的密钥xxxxx",
      # 区域与你申请密钥选择的区域有关
      "region": "你申请的区域比如：japanwest",
      # 看这里多语言、语音选择：https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts
      "language": "zh-CN",
      "voice": "zh-CN-XiaoxiaoNeural",
      # 语速
      "rate": "+30%"
  }
  ```

  推荐的音色：

  - XiaoxiaoNeural
  - XiaochenNeural
  - XiaochenMultilingualNeural
  - XiaoshuangNeural
  - XiaoyouNeural

## 贡献说明

请保证严格遵守 `pylint`

```bash
pylint $(git ls-files '*.py')
```

## 后续开发说明

- 大概会做 ui
- 大概会做朗读本地 pdf、txt 等格式文本
