'fish-speech内置'
from pathlib import Path
from typing import List, Set, Tuple, Union

from loguru import logger
from natsort import natsorted

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".m4a",
    ".wma",
    ".aac",
    ".aiff",
    ".aif",
    ".aifc",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
}


def audio_to_bytes(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not file_path or not Path(file_path).exists():
        return None
    with open(file_path, "rb") as wav_file:
        wav = wav_file.read()
    return wav


def read_ref_text(ref_text):
    """_summary_

    Args:
        ref_text (_type_): _description_

    Returns:
        _type_: _description_
    """
    path = Path(ref_text)
    if path.exists() and path.is_file():
        with path.open("r", encoding="utf-8") as file:
            return file.read()
    return ref_text


def list_files(
    path: Union[Path, str],
    extensions: Set[str] = None,
    sort: bool = True,
) -> List[Path]:
    """List files in a directory.

    Args:
        path (Path): Path to the directory.
        extensions (set, optional): Extensions to filter. Defaults to None.
        recursive (bool, optional): Whether to search recursively. Defaults to False.
        sort (bool, optional): Whether to sort the files. Defaults to True.

    Returns:
        list: List of files.
    """

    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Directory {path} does not exist.")

    files = [file for ext in extensions for file in path.rglob(f"*{ext}")]

    if sort:
        files = natsorted(files)

    return files


def load_filelist(path: Union[Path, str]) -> List[Tuple[Path, str, str, str]]:
    """
    Load a Bert-VITS2 style filelist.
    """

    files = Set()
    results = []
    count_duplicated, count_not_found = 0, 0

    language_to_languages = {
        "zh": ["zh", "en"],
        "jp": ["jp", "en"],
        "en": ["en"],
    }

    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            splits = line.strip().split("|", maxsplit=3)
            if len(splits) != 4:
                logger.warning(f"Invalid line: {line}")
                continue

            filename, speaker, language, text = splits
            file = Path(filename)
            language = language.strip().lower()

            if language == "ja":
                language = "jp"

            assert language in ["zh", "jp",
                                "en"], f"Invalid language {language}"
            languages = language_to_languages[language]

            if file in files:
                logger.warning(f"Duplicated file: {file}")
                count_duplicated += 1
                continue

            if not file.exists():
                logger.warning(f"File not found: {file}")
                count_not_found += 1
                continue

            results.append((file, speaker, languages, text))

    if count_duplicated > 0:
        logger.warning(f"Total duplicated files: {count_duplicated}")

    if count_not_found > 0:
        logger.warning(f"Total files not found: {count_not_found}")

    return results
