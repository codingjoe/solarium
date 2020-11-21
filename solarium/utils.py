import asyncio
import datetime
import logging
import os
import random  # nosec
from asyncio import subprocess

from pysolar import solar

logger = logging.getLogger(__package__)


async def update_color(latitude, longitude, leds, clouds, sound, interval=5):
    warm, cold = leds
    max_cloud_duration = 30
    cloudy = 0
    player = None
    if sound is not None and not os.path.isfile(sound):
        raise ValueError("File does not exist: %s" % sound)
    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        sun_altitude_deg = solar.get_altitude(latitude, longitude, now)
        logger.info("Sun altitude: %.1fº", sun_altitude_deg)

        if sound and player is None and sun_altitude_deg > -8:
            player = await subprocess.create_subprocess_exec(
                "ffplay", "-loop", "0", "-loglevel", "24", sound
            )

        if sun_altitude_deg > 16:
            if cloudy:
                cloudy -= interval
                asyncio.Task(warm.fade(0))
            else:
                cloudy = int(random.random() < clouds) * random.randrange(  # nosec
                    0, max_cloud_duration, interval
                )
                asyncio.Task(warm.fade(1))
            cold.value = 1
        elif sun_altitude_deg > 8:
            warm.value = 1
            asyncio.Task(cold.fade((sun_altitude_deg + 8) / 24))
        elif sun_altitude_deg > -8:
            cold.value = 0
            asyncio.Task(warm.fade(max((sun_altitude_deg + 8) / 16, 0.001)))
        else:
            cold.value = 0
            warm.value = 0
            if player is not None:
                player.terminate()
                player = None
        await asyncio.sleep(interval)
