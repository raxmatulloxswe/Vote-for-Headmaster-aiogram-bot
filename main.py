import asyncio
import logging
from loguru import logger
from bot import main as run_bot

import os

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    event_loop = asyncio.get_event_loop()

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        event_loop.create_task(run_bot())
        event_loop.run_forever()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info("Bot Stopped")
        event_loop.stop()
