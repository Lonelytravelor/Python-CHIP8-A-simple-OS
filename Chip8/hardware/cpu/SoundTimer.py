import os
from hardware.cpu.DelayTimer import DelayTimer


class SoundTimer(DelayTimer):
    def __init__(self):
        DelayTimer.__init__(self)

    def beep(self):
        if self.timer > 1:
            os.system('play --no-show-progress --null --channels 1 synth %s triangle %f' % (self.timer / 60, 440))
            self.timer = 0
