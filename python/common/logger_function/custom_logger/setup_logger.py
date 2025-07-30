import json
import os
import re
from datetime import datetime
from logging import Logger, config, getLogger


def _create_log_folder(log_filename: str) -> None:
    """
    指定されたログファイルパスからディレクトリを抽出し、存在しない場合は作成する。

    Args:
        log_filename (str): ログファイルのパス。ディレクトリ部分が存在しない場合は作成される。

    Returns:
        None
    """
    dirpath = os.path.dirname(log_filename)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)


def _update_log_conf(log_conf: dict) -> None:
    """
    ログ設定辞書内のログファイルパスに `{date:<format>}` プレースホルダが含まれている場合、
    実行時の日付でフォーマットし、ログファイル名を更新する。
    また、ログファイルの出力先ディレクトリが存在しない場合は作成する。

    Args:
        log_conf (dict): `logging.config.dictConfig` に渡す形式のログ設定辞書。

    Returns:
        None
    """
    filename = log_conf["handlers"]["fileHandler"]["filename"]
    _create_log_folder(filename)

    match = re.search(r"{([a-zA-Z0-9]+):(%[^}]+)}", filename)
    if match:
        if match.group(1) == "date":
            # ログファイル名に実行日付を付与
            date = datetime.now().strftime(match.group(2))
            filename = re.sub(r"{date:(%[^}]+)}", date, filename)
            log_conf["handlers"]["fileHandler"]["filename"] = filename


def create_logger(log_config_path: str = "log_config.json", name: str = "__main__") -> Logger:
    """
    JSON形式のログ設定ファイルを読み込み、ロガーを初期化して返す。
    ログファイル名に `{date:<format>}` プレースホルダが含まれている場合、実行時の日付に置換する。

    Args:
        log_config_path (str): ログ設定ファイル（JSON）のパス。デフォルトは "log_config.json"。
        name (str): 取得するロガーの名前。デフォルトは "__main__"。

    Returns:
        Logger: 初期化されたロガーインスタンス。
    """
    with open(log_config_path) as f:
        log_conf = json.load(f)

    _update_log_conf(log_conf)

    config.dictConfig(log_conf)
    return getLogger(name)
