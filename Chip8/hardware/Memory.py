"""
    类：模拟内存，仿真内存，使得CPU可以访问内存中的数据，支持读写初始化等
"""
from application.Font import Font


class Memory:

    """
        初始化内存，给定大小进行初始化，初始化为0    
    """
    def __init__(self, size):
        self.memory = []
        for i in range(size):
            self.memory.append(0x0)
        self.fonts = Font.fonts
        for i in range(len(self.fonts)):
            self.memory[i] = self.fonts[i]
    """
        指定位置写数据 
    """
    def write(self, offset, date):
        self.memory[offset] = date

    """
        指定位置读数据 
    """
    def read(self, offset):
        return self.memory[offset]