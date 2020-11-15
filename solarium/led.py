import asyncio
import logging

import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory

logger = logging.getLogger(__package__)


class PWMLED(gpiozero.PWMLED):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name")
        super().__init__(*args, **kwargs)

    async def fade(self, value, transition=3, interval=0.05):
        logger.debug("%s: %s -> %s (%ss)", self.name, self.value, value, transition)
        diff = value - self.value
        parts = transition / interval
        increments = diff / parts
        i = 0
        while transition > i:
            self.value = max(min(1, self.value + increments), 0)
            await asyncio.sleep(interval)
            i += interval


def init(host="localhost", warm_pin=12, cold_pin=13, frequency=400):
    logger.debug("warm LED: %s:%d@%dHz", host, warm_pin, frequency)
    logger.debug("cold LED: %s:%d@%dHz", host, cold_pin, frequency)
    factory = PiGPIOFactory(host=host)
    cold = PWMLED(warm_pin, name="cold", pin_factory=factory)
    warm = PWMLED(cold_pin, name="warm", pin_factory=factory)
    cold.frequency = frequency
    warm.frequency = frequency
    return warm, cold
