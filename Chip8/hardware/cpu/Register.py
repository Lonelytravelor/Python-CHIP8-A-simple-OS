"""
    寄存器：CHIP8有16个通用8位数据寄存器，V0~VF。VF寄存器存放进位标识。还有一个地址寄存器叫做I，2个字节的长度。
    类：寄存器，模拟仿真寄存器，可以读写寄存器中的数据，同时支持进位和借位，同时支持初始化寄存器长度
"""


class Register:
    def __init__(self, bits):
        self.value = 0
        self.bits = bits

    """
        检查进位
    """
    def checkCarry(self):
        hexValue = hex(self.value)[2:]

        if len(hexValue) > self.bits / 4:
            self.value = int(hexValue[-int(self.bits / 4):], 16)
            return 1
        return 0

    """
        检查借位
    """
    def checkBorrow(self):
        if self.value < 0:
            self.value = abs(self.value)
            return 0
        return 1

    """
        读取寄存器中的数值
    """
    def readValue(self):
        return hex(self.value)

    """
        向着寄存器写新的数值
    """
    def setValue(self, value):
        self.value = value
