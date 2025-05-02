from aiogram import Dispatcher
from .handlers.buttons import router_buttons
from .handlers.help import router_help
from .handlers.photo import router_photo
from .handlers.start import router_start
from .handlers.subscription import router_subscription


dp = Dispatcher()

# Серьезные вещи
dp.include_router(router_start)
dp.include_router(router_subscription)

# Пока всякие смешные штуки
dp.include_router(router_buttons)
dp.include_router(router_help)
dp.include_router(router_photo)

