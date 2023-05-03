# Python-CHIP8
使用Python实现CHIP8模拟器

本文参照:https://github.com/AlpacaMax/Python-CHIP8-Emulator 进行重构,根据抽象的思想完成模块的划分与解耦,以来模拟一个简单的操作系统的流程与实现.

注意:当前为1.0版本,还有一些小的错误未修改,如有问题,感谢反馈与修正!

本文前提:
1. CPU就是无情的执行指令的机器
2. 操作系统上的应用程序就是指令的集合
3. 操作系统/应用程序 = 状态机 = 值 + 指令

说明:
在这个程序中主要是包含了以下几个部分
硬件:
  屏幕:负责渲染图像
  Memory:内存,存储数据,支持读写
  键盘:输入设备,多个按键,有按下和松开两种状态
  CPU:CPU的仿真
    Stack:栈
    PC:pc指针
    Timeer:定时器
    寄存器:寄存器

说明:
1. 我希望硬件抽象为一个独立的个体,例如Memory只抽象为具有一个读写能力的储存设备,屏幕只抽象为一个渲染设备等等.
2. 抽象遵从 硬件--操作系统--应用程序 架构,所有的硬件只负责自己的工作,应用程序的指令都通过syscall请求操作系统去完成

Usage
pip3 install pygame
sudo apt install sox
git clone git@github.com:Lonelytravelor/Python-CHIP8.git
cd Python-CHIP8-Emulator
python3 chip8.py games/<Your game>
