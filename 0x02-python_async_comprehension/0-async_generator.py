#!/usr/bin/env python3
"""python async comprehension"""


import asyncio
from random import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """async_generator: yields random number between 0 and 10"""
    for i in range(10):
        await asyncio.sleep(1)
        yield random() * 10
