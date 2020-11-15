import asyncio
import logging
import sys

import click

from . import led
from .utils import update_color

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"

logger = logging.getLogger(__package__)


@click.command()
@click.argument("latitude", type=float)
@click.argument("longitude", type=float)
@click.option(
    "--clouds",
    "-c",
    default=0.2,
    help="Cache of clouds between. Between 0 and 1, default 0.2.",
)
@click.option(
    "--host", "-h", default="localhost", help="PiGPIO host, default: localhost"
)
@click.option("--warm", default=12, help="Warm LED GPIO pin, default: 12")
@click.option("--cold", default=13, help="Warm LED GPIO pin, default: 13")
@click.option(
    "--verbosity", "-v", default=0, count=True, help="Increase output verbosity."
)
def main(latitude, longitude, clouds, host, warm, cold, verbosity):
    setup_logging(verbosity)
    leds = led.init(host, warm, cold)
    asyncio.run(update_color(latitude, longitude, leds, clouds))


def get_logging_level(verbosity):
    level = logging.WARNING
    level -= verbosity * 10
    if level < logging.DEBUG:
        level = logging.DEBUG
    return level


def setup_logging(verbosity):
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setLevel(get_logging_level(verbosity))
    hdlr.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(hdlr)
    logger.setLevel(get_logging_level(verbosity))


if __name__ == "__main__":
    sys.exit(main())
