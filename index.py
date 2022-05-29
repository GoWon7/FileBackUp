import json
import os


def write_json(d: dict):
    with open('index.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(d, indent=4, ensure_ascii=False))


def load_json():
    with open('index.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def path_normalize(path: str):
    if os.path.exists(path):
        path = path.replace('\\', '/')
        if path[-1] != '/':
            path += '/'
        return path
    else:
        return -1  # 该路径不存在


def get_path(name: str):
    return load_json()[name]


def new_path(name: str, origin_path: str, backup_path: str):
    origin_path = path_normalize(origin_path)
    if origin_path == -1:
        return -2  # 原始路径不存在
    backup_path = path_normalize(backup_path)
    if backup_path == -1:
        return -3  # 备份路径不存在
    try:
        d = load_json()
        if name in d:
            return -1  # 名称已存在
        d[name] = [origin_path, backup_path]
        write_json(d)
        return 0
    except FileNotFoundError:
        write_json({name: [origin_path, backup_path]})


def delete_path(name: str):
    d = load_json()
    try:
        del d[name]
    except KeyError:
        return -1  # 不存在此名称
    write_json(d)
    return 0


def change_path_name(old_name: str, new_name: str):
    d = load_json()
    if new_name in d:
        return -1  # 新名称以存在
    try:
        d[new_name] = d[old_name]
        del d[old_name]
    except KeyError:
        return -2  # 旧名称不存在
    write_json(d)
    return 0


# new_path('origin', 'C:\File\Project\Python\DiskBackUp\origin', 'C:\File\Project\Python\DiskBackUp\\backup')
# change_path_name('origin', 'amazing')
