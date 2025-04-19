from aiogram import Dispatcher
from .handlers.buttons import router_buttons
from .handlers.help import router_help
from .handlers.photo import router_photo
from .handlers.registration import router_registration
from .handlers.start import router_start

dp = Dispatcher()
dp.include_router(router_start)
dp.include_router(router_buttons)
dp.include_router(router_help)
dp.include_router(router_photo)
dp.include_router(router_registration)
