from .logging import *
from .check_subscription import *


def setup_middlewares(dp):
    dp.update.outer_middleware(LoggingMiddleware())
    # dp.update.outer_middleware(CheckSubscriptionMiddleware())
