import asyncio
import datetime
import logging
import random  # nosec

from pysolar import solar

logger = logging.getLogger(__package__)


async def update_color(latitude, longitude, leds, clouds, interval=5):
    warm, cold = leds
    max_cloud_duration = 30
    cloudy = 0
    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        sun_altitude_deg = solar.get_altitude(latitude, longitude, now)
        logger.info("Sun altitude: %.1fº", sun_altitude_deg)

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
        await asyncio.sleep(interval)
