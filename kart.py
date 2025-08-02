import pigpio
import keyboard
class Kart:
    def __init__(self):
        self.pi = pigpio.pi()
    def write(self, power, ratio, freq = 1000):
        power = max(0, min(1, power))
        ratio = max(-1, min(1, ratio))
        dutya = int(255 * max(0, min(1, power + power * ratio)))
        dutyb = int(255 * max(0, min(1, power - power * ratio)))
        self.pi.set_PWM_frequency(17, freq)
        self.pi.set_PWM_frequency(27, freq)
        self.pi.set_PWM_dutycycle(17, dutya)
        self.pi.set_PWM_dutycycle(27, dutyb)
    def kill(self):
        self.pi.set_PWM_dutycycle(17, 0)
        self.pi.set_PWM_dutycycle(27, 0)
        self.pi.stop()
kart = Kart()
power = 0.0
ratio = 0.0
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
            ratio = -0.5
        elif keyboard.is_pressed('right'):
            ratio = 0.5
        kart.write(power, ratio)
kart.kill()