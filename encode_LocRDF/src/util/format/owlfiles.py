import os


def get_xxx_files(path: str, xxx: str):
    """
    获取该路径下所有的 xxx 文件
    """
    files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(f'.{xxx}'):
                files.append(file)
    return files


def get_owl_files(path: str):
    """
    获取该路径下所有的 owl 文件
    """
    return get_xxx_files(path, 'owl')


def get_nt_files(path: str):
    """
    获取该路径下所有的 nt 文件
    """
    return get_xxx_files(path, 'nt')
