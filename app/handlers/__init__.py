from .commands import router as commands_router
from .about import router as about_router


def setup_handlers(dp):
    dp.include_router(commands_router)
    dp.include_router(about_router)
