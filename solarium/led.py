import asyncio
import logging

import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory

logger = logging.getLogger(__package__)


class PWMLED(gpiozero.PWMLED):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name")
        self.power_state = kwargs.pop("power_state")
        self.power_state.callbacks.append(self.turn_off)
        super().__init__(*args, **kwargs)

    def turn_off(self, value):
        if not value:
            self.value = int(value)

    @gpiozero.PWMLED.value.setter
    def value(self, value):
        gpiozero.PWMLED.value.fset(self, value * self.power_state)

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


class PowerToggleMixin:
    def __init__(self, *args, power_led=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.power = 1
        self.power_led = power_led
        self.callbacks = []

    def toggle(self):
        logger.info("Toggle: %i -> %i", self.power, not self.power)
        self.power ^= 1
        self.power_led.value = not self.power
        for func in self.callbacks:
            func(self)

    def __bool__(self):
        return bool(self.power)

    def __int__(self):
        return self.power

    def __mul__(self, other):
        return int(self) * other

    def __rmul__(self, other):
        return other * int(self)

    async def listen(self):
        while True:
            self.value
            await asyncio.sleep(1)


class PowerToggle(PowerToggleMixin, gpiozero.Button):
    pass


def init(
    host="localhost",
    warm_pin=12,
    cold_pin=13,
    power_pin=17,
    power_led_pin=26,
    frequency=100,
):
    logger.debug("warm LED: %s:%d@%dHz", host, warm_pin, frequency)
    logger.debug("cold LED: %s:%d@%dHz", host, cold_pin, frequency)
    factory = PiGPIOFactory(host=host)

    power_led = gpiozero.LED(power_led_pin, pin_factory=factory)
    power_button = PowerToggle(power_pin, pin_factory=factory, power_led=power_led)
    power_button.when_pressed = lambda: power_button.toggle()
    warm = PWMLED(warm_pin, name="warm", power_state=power_button, pin_factory=factory)
    cold = PWMLED(cold_pin, name="cold", power_state=power_button, pin_factory=factory)
    warm.frequency = frequency
    cold.frequency = frequency

    return warm, cold, power_button
