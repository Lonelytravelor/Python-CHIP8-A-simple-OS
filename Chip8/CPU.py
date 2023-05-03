import random
from Register import Register
from SoundTimer import SoundTimer
from DelayTimer import DelayTimer
from Stack import Stack


"""
    类：模拟CPU，包含寄存器，栈，PC指针，时钟周期，以及指令集和执行指令
"""
class CPU:

    """
        用于初始化CPU信息，包括内存，寄存器，栈，PC指针，时钟周期
    """
    def __init__(self):
        # CHIP8有16个通用8位数据寄存器，V0~VF。VF寄存器存放进位标识。
        self.Registers = []
        for i in range(16):
            self.Registers.append(Register(8))
        # 地址寄存器叫做I，2个字节的长度。
        self.IRegister = Register(16)
        # PC指针
        self.ProgramCounter = 0x200
        # 初始化栈
        self.stack = Stack()
        # 初始化时钟
        self.delayTimer = DelayTimer()
        self.soundTimer = SoundTimer()

    """
        获取Timer定时器1 
    """
    def getDelayTimer(self):
        return self.delayTimer

    """
        获取Timer定时器2    
    """
    def getSoundTimer(self):
        return self.soundTimer

    """                               
        获取PC指针                        
    """
    def getPc(self):
        return self.ProgramCounter

    """
        指令集，操作码+根据指令执行指定的指令
    """
    def execOpcode(self, opcode, os):
        # print(opcode)

        if opcode[0] == '0':

            if opcode[1] != '0':
                # 0NNN

                print("ROM attempts to run RCA 1802 program at <0x" + opcode[1:] + '>')

            else:
                if opcode == '00e0':
                    # 00E0
                    # disp_clear()
                    os.sysCall_screen_clear()

                elif opcode == '00ee':
                    # 00EE
                    # return;

                    self.ProgramCounter = self.stack.pop()

        elif opcode[0] == '1':
            # 1NNN
            # goto NNN;

            self.ProgramCounter = int(opcode[1:], 16) - 2

        elif opcode[0] == '2':
            # 2NNN
            # *(0xNNN)()

            self.stack.push(self.ProgramCounter)
            self.ProgramCounter = int(opcode[1:], 16) - 2

        elif opcode[0] == '3':
            # 3XNN
            # if(Vx==NN)

            vNum = int(opcode[1], 16)
            targetNum = int(opcode[2:], 16)

            if self.Registers[vNum].value == targetNum:
                self.ProgramCounter += 2

        elif opcode[0] == '4':
            # 4XNN
            # if(Vx!=NN)

            vNum = int(opcode[1], 16)
            targetNum = int(opcode[2:], 16)

            if self.Registers[vNum].value != targetNum:
                self.ProgramCounter += 2

        elif opcode[0] == '5':
            # 5XY0
            # if(Vx==Vy)

            v1 = int(opcode[1], 16)
            v2 = int(opcode[2], 16)

            if self.Registers[v1].value == self.Registers[v2].value:
                self.ProgramCounter += 2

        elif opcode[0] == '6':
            # 6XNN
            # Vx = NN

            vNum = int(opcode[1], 16)
            targetNum = int(opcode[2:], 16)

            self.Registers[vNum].value = targetNum

        elif opcode[0] == '7':
            # 7XNN
            # Vx += NN

            vNum = int(opcode[1], 16)
            targetNum = int(opcode[2:], 16)

            self.Registers[vNum].value += targetNum
            self.Registers[vNum].checkCarry()

        elif opcode[0] == '8':
            if opcode[3] == '0':
                # 8XY0
                # Vx=Vy

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value = self.Registers[v2].value

            elif opcode[3] == '1':
                # 8XY1
                # Vx=Vx|Vy

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value = self.Registers[v1].value | self.Registers[v2].value

            elif opcode[3] == '2':
                # 8XY2
                # Vx=Vx&Vy

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value = self.Registers[v1].value & self.Registers[v2].value

            elif opcode[3] == '3':
                # 8XY3
                # Vx=Vx^Vy

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value = self.Registers[v1].value ^ self.Registers[v2].value

            elif opcode[3] == '4':
                # 8XY4
                # Vx += Vy

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value += self.Registers[v2].value

                self.Registers[0xf].value = self.Registers[v1].checkCarry()

            elif opcode[3] == '5':
                # 8XY5
                # Vx -= Vy

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value -= self.Registers[v2].value

                self.Registers[0xf].value = self.Registers[v1].checkBorrow()

            elif opcode[3] == '6':
                # 8XY6
                # Vx>>1

                v1 = int(opcode[1], 16)
                leastBit = int(bin(self.Registers[v1].value)[-1])

                self.Registers[v1].value = self.Registers[v1].value >> 1
                self.Registers[0xf].value = leastBit

            elif opcode[3] == '7':
                # 8XY7
                # Vx=Vy-Vx

                v1 = int(opcode[1], 16)
                v2 = int(opcode[2], 16)

                self.Registers[v1].value = self.Registers[v2].value - self.Registers[v1].value

                self.Registers[0xf].value = self.Registers[v1].checkBorrow()

            elif opcode[3] == 'e':
                # 8XYE
                # Vx<<=1

                v1 = int(opcode[1], 16)
                mostBit = int(bin(self.Registers[v1].value)[2])

                self.Registers[v1].value = self.Registers[v1].value << 1
                self.Registers[0xf].value = mostBit

        elif opcode[0] == '9':
            # 9XY0
            # if(Vx!=Vy)

            v1 = int(opcode[1], 16)
            v2 = int(opcode[2], 16)

            if self.Registers[v1].value != self.Registers[v2].value:
                self.ProgramCounter += 2

        elif opcode[0] == 'a':
            # ANNN
            # I = NNN

            addr = int(opcode[1:], 16)

            self.IRegister.value = addr

        elif opcode[0] == 'b':
            # BNNN
            # PC=V0+NNN

            addr = int(opcode[1:], 16)

            self.ProgramCounter = self.Registers[0].value + addr - 2

        elif opcode[0] == 'c':
            # CXNN
            # Vx=rand()&NN

            vNum = int(opcode[1], 16)
            targetNum = int(opcode[2:], 16)

            rand = random.randint(0, 255)

            self.Registers[vNum].value = targetNum & rand

        elif opcode[0] == 'd':
            # DXYN
            # draw(Vx,Vy,N)

            Vx = int(opcode[1], 16)
            Vy = int(opcode[2], 16)
            N = int(opcode[3], 16)

            addr = self.IRegister.value
            sprite = os.sysCall_memory_readList(addr, addr + N)

            for i in range(len(sprite)):
                if type(sprite[i]) == str:
                    sprite[i] = int(sprite[i], 16)

            if os.sysCall_screen_draw(self.Registers[Vx].value, self.Registers[Vy].value, sprite):
                self.Registers[0xf].value = 1
            else:
                self.Registers[0xf].value = 0

        elif opcode[0] == 'e':
            if opcode[2:] == '9e':
                # EX9E
                # if(key()==Vx)

                Vx = int(opcode[1], 16)
                key = self.Registers[Vx].value
                if os.sysCall_keyBoard_getKeyOfIndex(key):
                    self.ProgramCounter += 2

            elif opcode[2:] == 'a1':
                # EXA1
                # if(key()!=Vx)

                Vx = int(opcode[1], 16)
                key = self.Registers[Vx].value
                if not os.sysCall_keyBoard_getKeyOfIndex(key):
                    self.ProgramCounter += 2

        elif opcode[0] == 'f':
            if opcode[2:] == '07':
                # FX07
                # delay_timer(Vx)

                Vx = int(opcode[1], 16)
                self.Registers[Vx].value = self.delayTimer.readTimer()

            elif opcode[2:] == '0a':
                # FX0A
                # Vx = get_key()

                Vx = int(opcode[1], 16)
                key = None

                while True:
                    os.sysCall_keyboard_handler()
                    isKeyDown = False

                    for i in range(os.sysCall_keyBoard_getKeysLength):
                        if os.sysCall_keyBoard_getKeyOfIndex(i):
                            key = i
                            isKeyDown = True

                    if isKeyDown:
                        break

                self.Registers[Vx].value = key

            elif opcode[2:] == '15':
                # FX15
                # delay_timer(Vx)

                Vx = int(opcode[1], 16)
                value = self.Registers[Vx].value

                self.delayTimer.setTimer(value)

            elif opcode[2:] == '18':
                # FX18
                # sound_timer(Vx)

                Vx = int(opcode[1], 16)
                value = self.Registers[Vx].value

                self.soundTimer.setTimer(value)

            elif opcode[2:] == '1e':
                # FX1E
                # I += Vx

                Vx = int(opcode[1], 16)
                self.IRegister.value += self.Registers[Vx].value

            elif opcode[2:] == '29':
                # FX29
                # I = sprite_addr[Vx]

                Vx = int(opcode[1], 16)
                value = self.Registers[Vx].value

                self.IRegister.value = value * 5

            elif opcode[2:] == '33':
                # FX33
                '''
                set_BCD(Vx);
                *(I+0)=BCD(3);
                *(I+1)=BCD(2);
                *(I+2)=BCD(1);
                '''

                Vx = int(opcode[1], 16)
                value = str(self.Registers[Vx].value)

                fillNum = 3 - len(value)
                value = '0' * fillNum + value

                for i in range(len(value)):
                    os.sysCall_memory_write(self.IRegister.value + i, int(value[i]))

            elif opcode[2:] == '55':
                # FX55
                # reg_dump(Vx, &I)

                Vx = int(opcode[1], 16)
                for i in range(0, Vx + 1):
                    os.sysCall_memory_write(self.IRegister.value + i, self.Registers[i].value)

            elif opcode[2:] == '65':
                # FX65
                # reg_load(Vx, &I)

                Vx = int(opcode[1], 16)
                for i in range(0, Vx + 1):
                    self.Registers[i].value = os.sysCall_memory_read(self.IRegister.value + i)

        self.ProgramCounter += 2


