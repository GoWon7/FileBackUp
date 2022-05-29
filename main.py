import sys

import index
import copy
import tree


def copy_():
    name = ''
    print('请选择需要备份的目录：')
    index_dict = index.load_json()
    d1 = {}
    for e, i in enumerate(index_dict):
        print(str(e + 1) + '.', i, index_dict[i][0], index_dict[i][1])
        d1[str(e + 1)] = i
    switch = input('请输入序号：')
    for i in range(3):
        try:
            name = d1[switch]
            break
        except KeyError:
            switch = input(f'输入有误，请重新输入。还可以输入{3 - i}次')
    if name != '':
        paths = index.load_json()[name]
        d = tree.different_dict(tree.dir_list(paths[0]), tree.dir_list(paths[1]))
        a = tree.print_different_list(d)
        if a:
            if input('y: 确定备份    n: 停止备份\n请输入：') == 'y':
                copy.main(paths, d)
                print('备份完成！')
                print('\n================================\n')
                main()
            else:
                print('\n================================\n')
                main()
        else:
            input('文件未发生变动,输入任意字符回到主菜单')
            main()
    else:
        print('\n================================\n')
        main()


def index_():
    switch = -1
    print('当前目录：')
    d = index.load_json()
    for i in d:
        print('{:<16s}{:<64s}{:<64s}'.format(i, d[i][0], d[i][1]))
    print()
    print('1.新建目录', '2.删除目录', '3.目录改名', '0.返回主界面', sep='\n')
    print()
    for i in range(3):
        switch = input('请输入序号：')
        if switch not in ['1', '2', '3', '0']:
            print(f'输入有误，请输入数字。还可以输入{3 - i}次')
        else:
            break
    print()

    if switch == '1':
        for i in range(3):
            a = index.new_path(input('请输入名称：'), input('请输入需要备份的文件夹路径：'), input('请输入备份目的路径：'))
            if a == -1:
                print(f'目录名称已存在，请重新输入。还可以输入{3 - i}次')
            elif a == -2:
                print(f'需要备份的文件夹不存在，请重新输入。还可以输入{3 - i}次')
            elif a == -3:
                print(f'目标备份路径不存在，请重新输入。还可以输入{3 - i}次')
            else:
                break
    elif switch == '2':
        a = index.delete_path(input('请输入需要删除的目录名：'))
        if a == -1:
            print('目录名不存在。')
    elif switch == '3':
        for i in range(3):
            a = index.change_path_name(input('请输入原名称：'), input('请输入新名称：'))
            if a == -1:
                print(f'新名称已存在，请重新输入。还可以输入{3 - i}次')
            elif a == -2:
                print(f'原目录名不存在，请重新输入。还可以输入{3 - i}次')
            else:
                break
    elif switch == '0':
        print('================================\n')
        main()
    print('\n================================\n')
    index_()


def main():
    print('1.备份文件', '2.修改目录', '0.退出程序', sep='\n')
    print()
    switch = input('请输入序号：')
    print('\n================================\n')

    if switch == '1':
        copy_()
    elif switch == '2':
        index_()
    elif switch == '0':
        sys.exit()
    else:
        print('输入错误')


if __name__ == '__main__':
    main()
