#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import string
import shutil
import json
import sys
import os


TEMPLATES_PATH = "/Templates/template.mk"
JLINK_COMMAND_FILE_PATH = "/Templates/commandfile.jlink"
PARAM_PATH = "/Templates/parameter.json"
YCM_EXTRA_CONF_PATH = "/Templates/.ycm_extra_conf.py"
GDBINIT_PATH = "/Templates/.gdbinit"


def update_autoload_script(template_file_path, device,):
    """ 往自动下载的模板里填充DEVICE """

    """ device: target device name """
    assert isinstance(device, str)
    """ template_file_path: template file path """
    assert isinstance(template_file_path, str)

    with open(template_file_path, 'r') as f:
        template_mk = string.Template(f.read())
        template_mk = template_mk.substitute(DEVICE=device)
        return template_mk


def update_jlink_commandfile(commandfile_path, target_name):
    """ 往jlink command file中添加目标文件名 """

    """ jlink command file 模板文件 """
    assert isinstance(commandfile_path, str)
    """ 目标文件名 """
    assert isinstance(target_name, str)

    with open(commandfile_path, 'r') as f:
        commandfile = string.Template(f.read())
        commandfile = commandfile.substitute(TARGET=target_name)
        return commandfile


def get_makefile(makefile_path):
    """ 从旧makefile中提取信息(Target),以及将makefile中的内容以行为划分放入列表中 """
    assert isinstance(makefile_path, str) is True
    with open(makefile_path) as f:
        makefile = f.read().split('\n')
        p = makefile.index("# target")
        target = makefile[p + 2]
        target = target[target.find("=") + 2:]
        return (makefile, {"target": target})


def update_makefile(makefile_list, autoload_list, bin_path):
    """ 往makefile中添加autoload和BINPATH内容 """
    makefile_list.extend(autoload_list)

    p = makefile_list.index("BINPATH = ")
    makefile_list[p] += bin_path
    return makefile_list


def main():
    parse = argparse.ArgumentParser(
        description='stm32cubemx makefile complete')

    parse.add_argument('-D', '--device', action='store',
                       dest='device_name', help='target device')

    """ 本脚本目录 """
    app_folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    """ 执行目录"""
    target_folder_path = os.getcwd()

    results = parse.parse_args()
    if results.device_name is None:
        print("please input target device name")
        return

    mk_autoload = update_autoload_script(
        app_folder_path + TEMPLATES_PATH,
        results.device_name)
    data = get_makefile(target_folder_path + "/Makefile")

    """ 重写commandfile.jlink """
    commandfile = update_jlink_commandfile(
        app_folder_path + JLINK_COMMAND_FILE_PATH, data[1]['target'])
    new_commandfile = open(target_folder_path + "/commandfile.jlink", 'w')
    new_commandfile.write(commandfile)
    new_commandfile.close()

    with open(app_folder_path + PARAM_PATH, 'r') as f:
        param = json.load(f)
        makefile = update_makefile(
            data[0],
            mk_autoload.split('\n'),
            param['BINPATH'])

        """ 重写makefile文件 """
        new_makefile = open(target_folder_path + "/makefile", 'w')
        new_makefile.write('\n'.join(makefile))
        new_makefile.close()

    """ 复制ycm与gdbinit """
    shutil.copy(app_folder_path + YCM_EXTRA_CONF_PATH, target_folder_path)
    shutil.copy(app_folder_path + GDBINIT_PATH, target_folder_path)


if __name__ == "__main__":
    main()
