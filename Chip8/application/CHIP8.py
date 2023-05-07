import sys

import pygame

from OperationSystem.OS import OS

"""
    类:应用程序:/games/...的文件们则是应用程序的一种,实际上是指令的集合
    作用:这里实现了读取程序的功能以及主循环(或者说应用程序本身)
"""


class Chip8:
    def __init__(self):
        self.os = OS()

    '''
        读取程序（游戏）加载到Memory中
    '''

    def readProg(self, filename):
        rom = self.convertProg(filename)

        offset = int('0x200', 16)
        for i in rom:
            self.os.sysCall_memory_write(offset, i)
            offset += 1

    '''
        转化程序（游戏）
    '''

    def convertProg(self, filename):
        rom = []

        with open(filename, 'rb') as f:
            wholeProgram = f.read()

            for i in wholeProgram:
                opcode = i
                rom.append(opcode)

        return rom

    """
        这里实现了应用程序:包括一个死循环,请求OS处理键盘时间,请求CPU执行,请求屏幕进行显示等等
    """

    def mainLoop(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(300)
            self.os.sysCall_keyboard_handler()
            self.os.sysCall_CPU_soundTimerBeep()
            self.os.sysCall_CPU_execution()
            self.os.sysCall_screen_display()


# 这里实现了CHIP8,然后将做好的程序加载到内存中,并运行该应用程序
chip8 = Chip8()
chip8.readProg(sys.argv[1])
chip8.mainLoop()
