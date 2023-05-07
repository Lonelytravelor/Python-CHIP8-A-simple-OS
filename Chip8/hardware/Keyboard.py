import sys

import pygame

"""
    类：抽象的键盘
    作用:它的作用就是模拟一个键盘，只提供最基本的硬件服务
    备注：keyDict作用是为了模拟CHIP8的指令集，所以转化一下
"""


class Keyboard:
    """
        初始化键盘类，模拟键盘拥有十六个按键，没有被按下为False，反之为True
    """
    def __init__(self):
        self.keys = []
        '''
        Chip8       My Keys
        ---------   ---------
        1 2 3 C     1 2 3 4
        4 5 6 D     q w e r
        7 8 9 E     a s d f
        A 0 B F     z x c v
        '''
        self.keyDict = {
            49: 1,
            50: 2,
            51: 3,
            52: 0xc,
            113: 4,
            119: 5,
            101: 6,
            114: 0xd,
            97: 7,
            115: 8,
            100: 9,
            102: 0xe,
            122: 0xa,
            120: 0,
            99: 0xb,
            118: 0xf
        }
        for i in range(0, 16):
            self.keys.append(False)

    '''
        按下指定键盘
    '''
    def keyDown(self, key):
        targetKey = self.keyDict[key]
        self.keys[targetKey] = True

    '''
        恢复指定键盘
    '''
    def keyUp(self, key):
        targetKey = self.keyDict[key]
        self.keys[targetKey] = False

    """
        获取Keys列表
    """
    def getKeys(self):
        return self.keys

    """
        获取Dict中指定index上的值
    """
    def getDictOfIndex(self, index):
        return self.keyDict[index]

    """
        获取Keys中指定index上的值
    """
    def getKeyOfIndex(self, index):
        return self.keys[index]
