class DelayTimer:
    def __init__(self):
        self.timer = 0

    def countDown(self):
        if self.timer > 0:
            self.timer -= 1

    def setTimer(self, value):
        self.timer = value

    def readTimer(self):
        return self.timer
