import time
import random
from data.settings import SLEEP_ACCOUNT
from other.add_loguru import logger


def sleep_account():
    logger.debug(f'🕐 sleep between accounts')
    time.sleep(random.randint(SLEEP_ACCOUNT[0], SLEEP_ACCOUNT[1]))
