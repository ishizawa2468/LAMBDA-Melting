import os

from typing import List, Optional

def get_files_list(
        path: str,
        includes: Optional[List[str]] = None,
        excludes: Optional[List[str]] = None,
        exclude_hide: bool = True,
        debug: bool = False
) -> List[str]:
    # パスの存在チェック
    if not os.path.isdir(path):
        raise ValueError(f"Invalid path: {path} is not a directory.")

    return_list = []
    files_list = os.listdir(path)
    if debug: print(f"Files in directory: {files_list}")

    for file in files_list:
        if debug: print(f"Processing file: {file}")

        # 隠しファイルのスキップ
        if exclude_hide and file.startswith('.'):
            if debug: print(f"Skipping hidden file: {file}")
            continue

        # includes判定
        if includes:
            if not any(include in file for include in includes):
                if debug: print(f"File does not match includes: {file}")
                continue

        # excludes判定
        if excludes:
            if any(exclude in file for exclude in excludes):
                if debug: print(f"File matches excludes: {file}")
                continue

        # 条件を全て満たしたファイルを追加
        return_list.append(file)
        if debug: print(f"File added: {file}")

    return return_list
