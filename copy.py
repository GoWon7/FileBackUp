import shutil
import os
import sys

import tree
import index


def copy_file(origin_path: str, backup_path: str, file_list: list):
    for i in file_list:
        shutil.copyfile(origin_path + i, backup_path + i)


def modify_file(origin_path: str, backup_path: str, file_list: list):
    for i in file_list:
        print('a')
        shutil.copy(origin_path + i, backup_path + i + '.temp')
        os.remove(backup_path + i)
        os.rename(backup_path + i + '.temp', backup_path + i)


def delete_file(backup_path: str, file_list):
    for i in file_list:
        os.remove(backup_path + i)


def make_dir(backup_path: str, dir_list: list):
    for i in dir_list:
        if not os.path.exists(backup_path + i):
            os.makedirs(backup_path + i)


def delete_dir(path: str, dir_list: list):
    for i in reversed(dir_list):
        try:
            os.rmdir(path + i)
        except FileNotFoundError:
            pass


def main(paths: list, d: dict):
    make_dir(paths[1], d['new_dir'])
    copy_file(paths[0], paths[1], list(d['new'].keys()))
    modify_file(paths[0], paths[1], list(d['modify'].keys()))
    delete_file(paths[1], list(d['delete'].keys()))
    delete_dir(paths[1], d['delete_dir'])


def main_main():
    name = 'origin'
    paths = index.load_json()[name]
    d = tree.different_dict(tree.dir_list(paths[0]), tree.dir_list(paths[1]))
    a = tree.print_different_list(d)
    if a:
        if input('y: 确定备份    n: 停止备份\n请输入：') == 'y':
            main(paths, d)
        else:
            sys.exit()
    else:
        print('文件未发生变动。')
        sys.exit()


if __name__ == '__main__':
    main_main()
