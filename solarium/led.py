import asyncio
import logging

import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory

logger = logging.getLogger(__package__)


class PWMLED(gpiozero.PWMLED):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name")
        self.power_state = kwargs.pop("power_state")
        super().__init__(*args, **kwargs)

    async def fade(self, value, transition=3, interval=0.05):
        logger.debug("%s: power %s", self.name, self.power_state)
        logger.debug("%s: %s -> %s (%ss)", self.name, self.value, value, transition)
        value *= self.power_state
        diff = value - self.value
        parts = transition / interval
        increments = diff / parts
        i = 0
        while transition > i:
            self.value = max(min(1, self.value + increments), 0)
            await asyncio.sleep(interval)
            i += interval


class PowerToggle:
    def __init__(self):
        self.power = 1

    def __call__(self):
        self.power ^= 1

    def __bool__(self):
        return bool(self.power)

    def __int__(self):
        return self.power

    def __mul__(self, other):
        return int(self) * other

    def __rmul__(self, other):
        return other * int(self)


def init(host="localhost", warm_pin=12, cold_pin=13, power_pin=17, frequency=220):
    logger.debug("warm LED: %s:%d@%dHz", host, warm_pin, frequency)
    logger.debug("cold LED: %s:%d@%dHz", host, cold_pin, frequency)
    factory = PiGPIOFactory(host=host)

    power_button = gpiozero.Button(power_pin, pin_factory=factory)
    power_state = PowerToggle()
    power_button.when_pressed = power_state
    warm = PWMLED(warm_pin, name="warm", power_state=power_state, pin_factory=factory)
    cold = PWMLED(cold_pin, name="cold", power_state=power_state, pin_factory=factory)
    warm.frequency = frequency
    cold.frequency = frequency

    return warm, cold
