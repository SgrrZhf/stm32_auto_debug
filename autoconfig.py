#!/usr/bin/env python3

import sys
import os
import shutil
import string
import json

if len(sys.argv) < 2:
    print("argument is not enough, please check the input argument.")
    quit()

app_folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))
target_folder_path = os.getcwd()

'''copy .ycm_extra_conf.py to the specified directory'''
shutil.copy(
    app_folder_path +
    "/Templates/.ycm_extra_conf.py",
    target_folder_path)
shutil.copy(
    app_folder_path +
    "/Templates/.gdbinit",
    target_folder_path)

'''get necessary message from target_folder_path Makefile'''
with open(target_folder_path + "/Makefile", 'r+') as makefile_file:

    # 查找makefile中TARGET的内容
    while True:
        line_content = makefile_file.readline()
        if len(line_content) == 0:
            break
        if line_content.find("TARGET") != -1:
            target = line_content[(line_content.find("=") + 2):-1]
            break

    # 将target写入新的commandfile.jlink
    if target is not None:
        shutil.copy(
            app_folder_path +
            "/Templates/commandfile.jlink",
            target_folder_path)
        with open(target_folder_path + "/commandfile.jlink", 'r+') as f:
            commandfile_str = string.Template(f.read())
            commandfile_str = commandfile_str.substitute(TARGET=target)
            f.seek(0)
            f.truncate()
            f.write(commandfile_str)
    else:
        print("Can not find correct TARGET! the Makefile may not exist.")
        quit()

    # 获取makefile调试规则的补充内容模板
    with open(app_folder_path + "/Templates/template.mk") as f:
        template_mk = string.Template(f.read())
        # 替换模板中的DEVICE参数
        template_mk = template_mk.substitute(DEVICE=sys.argv[1])

        # 将更新后的模板添加到makefile的指定位置
        makefile_file.seek(0)
        makefile_str = makefile_file.read().split("\n")
        template_mk = template_mk.split("\n")
        position = makefile_str.index("# clean up") - 1
        for s in template_mk:
            makefile_str.insert(position, s)
            position = position + 1

        # 为makefile中的BINPATH添加内容
        position = makefile_str.index("BINPATH = ")
        with open(app_folder_path + "/Templates/parameter.json") as param_file:
            param = json.load(param_file)
            makefile_str[position] = makefile_str[position] + param["BINPATH"]

        # 将新内容重新写入makefile中
        with open(target_folder_path + "/makefile", "w") as f:
            f.write("\n".join(makefile_str))

os.system("ctags -R")
print("finish...")
