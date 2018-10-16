#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import string
import shutil
import json
import sys
import os


TEMP_PATH = "/Templates/"
KBUILD_VERBOSE = "kbuild_verbose.mk"
TEMPLATES_PATH = "/Templates/template.mk"
JLINK_COMMAND_FILE_PATH = "/Templates/commandfile.jlink"
PARAM_PATH = "/Templates/parameter.json"
YCM_EXTRA_CONF_PATH = "/Templates/.ycm_extra_conf.py"
GDBINIT_PATH = "/Templates/.gdbinit"


def update_autoload_script(template_file_path, device):
    """ 往自动下载的模板里填充DEVICE """

    """ device: target device name """
    assert isinstance(device, str)
    """ template_file_path: template file path """
    assert isinstance(template_file_path, str)

    with open(template_file_path, 'r') as f:
        template_mk = string.Template(f.read())
        template_mk = template_mk.substitute(DEVICE=device)
        return template_mk


def update_kbuild_verbose(path_file):
    """ 获取kbuild_verbose内容 """

    """ path_file: kbuild_verbose template file """
    assert isinstance(path_file, str)

    with open(path_file, 'r') as f:
        return f.read()


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


def add_Q(string, key, echo):
    index = string.find(key)
    if index != -1:
        string = string[:index] + "$(Q)" + string[index:]
        string = "\t@echo %s $@\n" % (echo) + string
    return string


def handle_makefile(makefile_path):
    """ 从旧makefile中提取信息(Target),以及将makefile中的内容以行为划分放入列表中 """
    assert isinstance(makefile_path, str) is True
    with open(makefile_path) as f:
        makefile = f.read().split('\n')
        p = makefile.index("# target")
        target = makefile[p + 2]
        target = target[target.find("=") + 2:]

        """ 整理一下C_SOURCES文件顺序 """
        c_sources_start = makefile.index("C_SOURCES =  \\") + 1
        c_sources_end = makefile.index("# ASM sources")
        temp = sorted(
            set(makefile[c_sources_start:c_sources_end]))
        temp.reverse()
        del(makefile[c_sources_start:c_sources_end])
        p = c_sources_start
        for i in temp:
            if len(i) == 0:
                continue
            if i[-1] != '\\':
                i += '\\'
            makefile.insert(p, i)
            p += 1
        makefile.insert(p, '')

        """ 加入$(Q) """
        i = 0
        while i < len(makefile):
            makefile[i] = add_Q(makefile[i], "$(CC)", "CC")
            makefile[i] = add_Q(makefile[i], "$(AS)", "AS")
            makefile[i] = add_Q(makefile[i], "$(SZ)", "SZ")
            makefile[i] = add_Q(makefile[i], "$(HEX)", "CP")
            makefile[i] = add_Q(makefile[i], "$(BIN)", "CP")
            i += 1

        return (makefile, {"target": target})


def update_makefile(makefile_list, autoload_list, gcc_path, kbuild_list):
    """ 往makefile中添加autoload和GCC_PATH内容 """
    makefile_list.extend(autoload_list)

    p = makefile_list.index("# target") - 1
    for i in kbuild_list:
        makefile_list.insert(p, i)
        p += 1

    p = makefile_list.index("ifdef GCC_PATH")
    makefile_list.insert(p, "GCC_PATH = " + gcc_path)

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
    mk_kbuild_verbose = update_kbuild_verbose(
        app_folder_path + TEMP_PATH + KBUILD_VERBOSE)
    data = handle_makefile(target_folder_path + "/Makefile")

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
            param['GCC_PATH'],
            mk_kbuild_verbose.split('\n'))

        """ 重写makefile文件 """
        new_makefile = open(target_folder_path + "/makefile", 'w')
        new_makefile.write('\n'.join(makefile))
        new_makefile.close()

    """ 复制ycm与gdbinit """
    shutil.copy(app_folder_path + YCM_EXTRA_CONF_PATH, target_folder_path)
    shutil.copy(app_folder_path + GDBINIT_PATH, target_folder_path)


if __name__ == "__main__":
    main()
