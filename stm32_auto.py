#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import string
import sys
import os


TEMPLATES_PATH = "/Templates/template.mk"


def fill_template(template_file_path, device,):
    """ 往自动下载的模板里填充DEVICE """

    """ device: target device name """
    assert isinstance(device, str)
    """ template_file_path: template file path """
    assert isinstance(template_file_path, str)

    with open(template_file_path, 'r') as f:
        template_mk = string.Template(f.read())
        template_mk = template_mk.substitute(DEVICE=device)
        return template_mk


def extract_information(makefile_path):
    """ 从旧makefile中提取信息(Target) """
    assert isinstance(makefile_path, str) is True
    with open(makefile_path) as f:
        makefile = f.read().split('\n')
        p = makefile.index("# target")
        target = makefile[p+2]
        target = target[target.find("=")+2:]
        return {"target": target}


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

    mk_autoload = fill_template(
        app_folder_path + TEMPLATES_PATH,
        results.device_name)
    data = extract_information(target_folder_path+"/Makefile")
    print(data)



if __name__ == "__main__":
    main()
