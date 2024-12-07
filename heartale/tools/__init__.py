"""一些工具"""
import hashlib
import json
import os
import re
import time
import urllib


def split_text(text_all, dcp=0):
    """重新划分段落，防止太短

    Args:
        text_all (dict): 书json
        dcp (int, optional): 分段转音频，第几段. Defaults to 0.

    Returns:
        _type_: result（分割以后的文本数组）, p2s（每个字符在这个章节的索引位置）, n_last（记录的索引位置是第几个分割文本）
    """
    result = []
    p2s = [0]
    text = ""
    n_last = 0

    last = 0
    text_list = text_all.strip().split("\n")
    for i, line in enumerate(text_list):
        text += line + "\n"
        # 至少一段，如果一段没超过100个字，把下一段也连上，还不够100,继续
        # 如果这个章节最后，也算上
        if len(text) > 100 or i == len(text_list) - 1:

            if last <= dcp <= last + len(text):
                n_last = len(result)

            result.append(text)
            # 这个分割是第几个字符，方便保存进度
            p2s.append(last + len(text))

            last = last + len(text)
            text = ""

    if n_last > 0:
        n_last -= 1

    return result, p2s, n_last


def data2url(url):
    """将书籍信息URL编码

    Args:
        url (str): url

    Returns:
        str: 编码以后的图书信息url
    """
    return urllib.parse.quote(url)


def cal_file_md5(file_path, chunk_size=8192):
    """计算文件md5

    Args:
        file_path (str): _description_
        chunk_size (int, optional): _description_. Defaults to 8192.

    Returns:
        str: _description_
    """
    st = time.time()
    # 创建一个MD5哈希对象
    md5_hash = hashlib.md5()

    # 按块读取文件并更新MD5对象
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            md5_hash.update(chunk)

    # 获取MD5哈希值（以十六进制表示）
    print(f"计算文件md5耗时：{time.time() - st}")
    return md5_hash.hexdigest()


def save_data(file_path, data):
    """保存数据到文件

    Args:
        file_path (str): 文件路径
        data (_type_): 数据
    """

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_data(file_path, data_defaul=None):
    """保存数据到文件

    Args:
        file_path (str): 文件路径
        data (_type_): 数据
    """

    if not os.path.exists(file_path) and data_defaul is not None:
        return data_defaul

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_library_installed(library_name):
    """某个库是否被安装

    Args:
        library_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        __import__(library_name)
        return True
    except ImportError:
        return False


def detect_encoding(file_path):
    """
    Detect the encoding of a given file by attempting to read it with different encodings.

    Args:
        file_path (str): The path to the file whose encoding is to be detected.

    Returns:
        str: The detected encoding if successful, otherwise None.
    """

    encodings = ['utf-8', 'gbk', 'gb2312', 'big5']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                file.read()
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue

    return None  # 未能检测到编码


def parse_volumes_and_chapters(file_content, chap_n):
    """匹配 "第xx卷" 和 "第xx章"

    Args:
        file_content (str): _description_

    Returns:
        _type_: _description_
    """

    # 匹配 "第xx卷" 和 "第xx章"
    volume_pattern = r'^第([一二三四五六七八九十\d]+)卷\s*(.*)'  # 匹配卷号
    chapter_pattern = r'^第([一二三四五六七八九十百千\d]+)章\s*(.*)'  # 匹配章号

    current_volume = None
    chap_names = []
    p2s = []
    chap_content = ""

    # 按行解析文本
    # print(file_content)
    ss = file_content.split("\n")
    words = 0
    for line in ss:
        words += len(line + "\n")
        # 匹配卷号
        volume_match = re.search(volume_pattern, line)
        if volume_match:
            current_volume = volume_match.group()  # 获取当前卷
            continue  # 继续找章

        # 匹配章号
        chapter_match = re.search(chapter_pattern, line)
        if chapter_match:
            current_chapter = chapter_match.group()
            if current_volume:
                chap_names.append(f"{current_volume} {current_chapter}")
            else:
                chap_names.append(f"{current_chapter}")
            p2s.append(words)

        if len(p2s) == chap_n:
            chap_content += line + "\n"

    return chap_names, p2s, chap_content


def get_proxy_url():
    """获取代理地址

    Returns:
        str: 代理地址，如果没有设置代理则返回 None
    """
    http_p = os.getenv("http_proxy")
    if http_p:
        return http_p
    https_p = os.getenv("https_proxy")
    if https_p:
        return https_p

    return None
