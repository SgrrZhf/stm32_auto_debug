
## 项目说明
为stm32cubemx生成的Makefile加入自动下载与调试功能

## 实现原理
1. 载入"Makefile"，添加相关命令，并生成新的"makefile"
2. 从"Makefile"中获取目标文件名target，并生成commandfile.jlink脚本用于下载target.bin文件
3. 复制一份事先写好的gdbinit文件，用于调试时自动连接jlinkgdbserver,并在main开头加入断点，然后运行到main处停下
