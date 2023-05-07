import pygame

"""
    模拟屏幕,支持初始化屏幕,渲染,清除等操作,因为是使用的pygame进行模拟而不是真的屏幕,所以使用的是pygame的类进行拓展
"""
class Screen:
    pygame.init()

    def __init__(self):
        self.name = "Screen"
        self.height = 32
        self.width = 64
        self.resolution = self.height * self.width
        self.grid = []
        self.zeroColor = [0, 0, 50]
        self.oneColor = [255, 255, 255]
        self.size = 10
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(0)
            self.grid.append(line)
        self.emptyGrid = self.grid[:]
        self.screen = pygame.display.set_mode([self.width * self.size, self.height * self.size])

    def draw(self, Vx, Vy, sprite):
        collision = False

        spriteBits = []
        for i in sprite:
            binary = bin(i)
            line = list(binary[2:])
            fillNum = 8 - len(line)
            line = ['0'] * fillNum + line

            spriteBits.append(line)

        for i in range(len(spriteBits)):
            # line = ''
            for j in range(8):
                try:
                    if self.grid[Vy + i][Vx + j] == 1 and int(spriteBits[i][j]) == 1:
                        collision = True

                    self.grid[Vy + i][Vx + j] = self.grid[Vy + i][Vx + j] ^ int(spriteBits[i][j])
                    # line += str(int(spriteBits[i][j]))
                except:
                    continue

            # print(line)

        return collision

    def clear(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j] = 0

    def display(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                cellColor = self.zeroColor

                if self.grid[i][j] == 1:
                    cellColor = self.oneColor

                pygame.draw.rect(self.screen, cellColor, [j * self.size, i * self.size, self.size, self.size], 0)

        pygame.display.flip()
