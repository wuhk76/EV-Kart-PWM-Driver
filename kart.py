import json
import pigpio
import keyboard
class Kart:
    def __init__(self):
        self.pi = pigpio.pi()
        self.mid = 0.0
        self.delta = 0.5
        self.freq = 1000
        self.pins = [17, 27]
    def load(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.mid = config.get('mid', self.mid)
                self.delta = config.get('delta', self.delta)
                self.freq = config.get('freq', self.freq)
                self.pins = config.get('pins', self.pins)
        except FileNotFoundError:
            pass
    def write(self, power, ratio):
        power = max(0, min(1, power))
        ratio = max(-1, min(1, ratio))
        aratio = max(-1, min(1, ratio + self.mid))
        bratio = max(-1, min(1, ratio - self.mid))
        dutya = int(255 * max(0, min(1, power + power * aratio)))
        dutyb = int(255 * max(0, min(1, power - power * bratio)))
        self.pi.set_PWM_frequency(self.pins[0], self.freq)
        self.pi.set_PWM_frequency(self.pins[1], self.freq)
        self.pi.set_PWM_dutycycle(self.pins[0], dutya)
        self.pi.set_PWM_dutycycle(self.pins[1], dutyb)
    def kill(self):
        self.pi.set_PWM_dutycycle(self.pins[0], 0)
        self.pi.set_PWM_dutycycle(self.pins[1], 0)
        self.pi.stop()
    def main(self):
        power = 0.0
        ratio = 0.0
        delta = max(-1, min(1, self.delta))
        running = True
        while running:
            ratio = 0.0
            if keyboard.is_pressed('q'):
                running = False
            else:
                for j in range(10):
                    if keyboard.is_pressed(f'{j}'):
                        power = j / 9.0
                if keyboard.is_pressed('left'):
                    ratio = -delta
                elif keyboard.is_pressed('right'):
                    ratio = delta
                self.write(power, ratio)
kart = Kart()
kart.load()
try:
    kart.main()
except:
    pass
kart.kill()