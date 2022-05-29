import os
import json

path1 = 'C:/File/Project/Python/DiskBackUp/origin/'
path2 = 'C:/File/Project/Python/DiskBackUp/backup/'

path3 = 'C:/File/图片/'

unit = ['Byte', 'KB', 'MB', 'GB', 'TB', 'PB']


def write_json(file_name, d: dict):
    with open(f'path/{file_name}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(d, indent=4, ensure_ascii=False))


def load_json(file_name: str):
    with open(f'path/{file_name}.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def size_unit(n: int):
    unit_index = 0
    if n < 1024:
        return str(n) + ' Byte'
    while n > 1024:
        n /= 1024
        unit_index += 1
    return '{:.1f} '.format(n) + unit[unit_index]


def dir_list(path: str):  # 生成文件结构字典，值为文件大小
    d = {}
    for file_name in os.listdir(path):
        file = path + file_name
        if os.path.isfile(file):
            d[file_name] = os.path.getsize(file)
        elif os.path.isdir(file):
            d[file_name] = dir_list(file + '/')
    return d


def load(d: dict):
    for i in d:
        if type(d[i]) is int:
            pass
        elif type(d[i]) is dict:
            for j in load(d[i]):
                yield


def different_dict(new_dict: dict, old_dict: dict):
    new_list = {}
    modify_list = {}
    delete_list = {}
    new_dir = []
    delete_dir = []

    def new_all(d: dict, path: str):
        new_dir.append(path[0: -1])
        for i in d:
            if type(d[i]) is int:
                new_list[path + i] = [0, d[i]]
            elif type(d[i]) is dict:
                new_all(d[i], path + i + '/')

    def delete_all(d: dict, path: str):
        for i in d:
            if type(d[i]) is int:
                delete_list[path + i] = [d[i], 0]
            elif type(d[i]) is dict:
                delete_dir.append(path + i)
                delete_all(d[i], path + i + '/')

    def check(new: dict, old: dict, path: str = ''):
        for key in list(new.keys()):
            if type(new[key]) is int:
                try:
                    if new[key] != old[key]:
                        modify_list[path + key] = [old[key], new[key]]
                    del old[key]
                except KeyError:
                    new_list[key] = [0, new[key]]
            elif type(new[key]) is dict:
                try:
                    check(new[key], old[key], path + key + '/')
                    del old[key]
                except KeyError:
                    new_all(new[key], path + key + '/')
        if len(old) != 0:
            delete_all(old, path)

    check(new_dict, old_dict)
    return {'new': new_list, 'modify': modify_list, 'delete': delete_list, 'new_dir': new_dir, 'delete_dir': delete_dir}


def print_different_list(d: dict):
    translate = {'new': '新增', 'modify': '修改', 'delete': '删除', 'new_dir': '新增', 'delete_dir': '删除'}
    out = False
    for i in d:
        if type(d[i]) is dict and d[i] != {}:
            out = True
            print(translate[i] + '文件：')
            for j in d[i]:
                old_size = size_unit(d[i][j][0])
                new_size = size_unit(d[i][j][1])
                print('\t{:<96s} | {} -> {}'.format(j, old_size, new_size))
            print()
        elif type(d[i]) is list and d[i] != []:
            out = True
            print(translate[i] + '文件夹：')
            for k in d[i]:
                print('\t' + k)
            print()
    return out


if __name__ == '__main__':
    # main(path1, 'origin')
    a = different_dict(dir_list(path1), load_json('origin'))
    print_different_list(a)
    # print(dir_list(path1))
    # print(load_json('origin'))
