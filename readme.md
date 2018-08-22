
## 项目说明
为stm32cubemx生成的Makefile加入自动下载与调试功能

## 适配版本
STM32CubeMX v4.26.1
由于这个版本修复了之前生成Makefile的种种问题，所以脚本对源文件内容做修改的内容是添加了GCC_PATH变量，以及对C_SOURCES的内容做了排序

## 实现原理
1. 载入"Makefile"，添加相关命令，并生成新的"makefile"
2. 从"Makefile"中获取目标文件名target，并生成commandfile.jlink脚本用于下载target.bin文件
3. 复制一份事先写好的gdbinit文件，用于调试时自动连接jlinkgdbserver,并在main开头加入断点，然后运行到main处停下

## 使用说明
1. 根据自己的需求修改Templates中的文件
其中commandfile.jlink是jlink脚本文件，用于一键下载bin文件
parameter.json是配置文件,需要指定本机gcc-arm-none-eabi的目录
template.mk是makefile需要添加的的内容的模板，无需修改
2. 在STM32CubeMX生成的工程下运行stm32_auto.py
```
~/code/project/stm32_autoconfig_tools/stm32_auto.py -D STM32L152CB
```
-D参数用于指定目标芯片型号

