import sys

import pygame

from CPU import CPU
from Keyboard import Keyboard
from Memory import Memory
from Screen import Screen

"""
    类：模拟操作系统，完成各个部分的协调，包括从给CPU发送指令，内存中读取数据，通知屏幕显示信息等等
"""


class OS:
    def __init__(self):
        self.cpu = CPU()
        self.keyBoard = Keyboard()
        self.screen = Screen()
        self.memory = Memory(4096)
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT + 1, int(1000 / 60))

    def sysCall_keyBoard_keyUp(self, key):
        self.keyBoard.keyUp(key)

    def sysCall_keyBoard_keyDown(self, key):
        self.keyBoard.keyDown(key)

    def sysCall_keyBoard_getKeyOfIndex(self, index):
        return self.keyBoard.getKeyOfIndex(index)

    def sysCall_keyBoard_getKeys(self):
        return self.keyBoard.getKeys()

    def sysCall_keyBoard_getKeysLength(self):
        return len(self.keyBoard.getKeys())

    def sysCall_keyBoard_getKeyDictOfIndex(self, index):
        return self.keyBoard.getDictOfIndex(index)

    def sysCall_memory_write(self, offset, data):
        self.memory.write(offset, data)

    def sysCall_memory_read(self, offset):
        return self.memory.read(offset)

    def sysCall_memory_readList(self, begin, last):
        return self.memory.memory[begin:last]

    def sysCall_screen_clear(self):
        self.screen.clear()

    def sysCall_screen_draw(self, Vx, Vy, sprite):
        self.screen.draw(Vx, Vy, sprite)

    def sysCall_screen_display(self):
        self.screen.display()

    def sysCall_keyboard_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.USEREVENT + 1:
                self.cpu.getDelayTimer().countDown()
            elif event.type == pygame.KEYDOWN:
                try:
                    self.sysCall_keyBoard_keyDown(event.key)
                except:
                    pass
            elif event.type == pygame.KEYUP:
                try:
                    self.sysCall_keyBoard_keyUp(event.key)
                except:
                    pass

    """
        获取操作码，处理并执行指令
    """
    def sysCall_CPU_execution(self):
        index = self.cpu.getPc()
        high = self.hexHandler(self.memory.read(index))
        low = self.hexHandler(self.memory.read(index+1))
        opcode = high + low
        self.cpu.execOpcode(opcode, self)

    """
        获取操作码，处理并执行指令
    """
    def sysCall_CPU_soundTimerBeep(self):
        self.cpu.getSoundTimer().beep()

    def hexHandler(self, Num):
        newHex = hex(Num)[2:]     # hex(20), hex(-20)  # 转换成十六进制
        if len(newHex) == 1:
            newHex = '0' + newHex

        return newHex