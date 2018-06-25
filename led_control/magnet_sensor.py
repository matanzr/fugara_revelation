from gpiozero import HoldMixin, DigitalInputDevice
import time
from collections import deque

class MagnetButton(HoldMixin, DigitalInputDevice):
    def __init__(
            self, pin=None, pull_up=True, bounce_time=None,
            hold_time=1, hold_repeat=False, pin_factory=None):
        super(MagnetButton, self).__init__(
            pin, pull_up, bounce_time, pin_factory=pin_factory
        )
        self.hold_time = hold_time
        self.hold_repeat = hold_repeat
        self._prev_change = time.time()
        self.when_activated = self.on_magnet
        self.when_magnet = None
        self.ttl = 0.25

        self.last_k = deque()
    
    def set_timeout(self, timeout):
        self.ttl = timeout

    def on_magnet(self, btn):
        self.last_k.append(self._last_changed - self._prev_change)
        if (len(self.last_k) > 9):
            self.last_k.popleft()
        self._prev_change = time.time()

        if self.when_magnet is not None: self.when_magnet(self)
    
    def estimated_rpm(self):
        if len(self.last_k) == 0: return 0
        avg = 0
        for i in self.last_k:
            avg += i
        return avg / float(len(self.last_k))
    
    def is_not_responding(self):
        if len(self.last_k) == 0: return True
        
        return self.ttl < self.last_k[-1]

if __name__ == "__main__":
    button = MagnetButton(16)

    while True:
        print button.last_k
        print button.estimated_rpm()
        time.sleep(1)