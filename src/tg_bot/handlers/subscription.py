from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router
from asgiref.sync import sync_to_async

from app_notification.models import (
    NotificationType,
    NotificationSchedule,
    Subscription
)
from app_tg.models import TGUser

router_subscription = Router()

#TODO: НАПИСАТЬ КНОПКИ


@sync_to_async
def save_subscription(user_id, data):
    """Сохраняет подписку в БД"""
    schedule = {
        'periodicity': data.get('periodicity'),
        'hour': data.get('hour'),
        'minute': data.get('minute'),
        'week_days': data.get('week_days'),
    }
    user = TGUser.objects.get(id=user_id)
    db_schedule = NotificationSchedule.objects.get_or_create(
        **schedule
    )
    Subscription.objects.create(
        user=user,
        schedule=db_schedule,
        type=data.get('type')
    )


class Sub(StatesGroup):
    type = State()
    periodicity = State()
    hour = State()
    minute = State()
    week_days = State()


@router_subscription.message(Command('subscribe'))
async def sub_type(message: Message, state: FSMContext):
    await state.set_state(Sub.type)
    await message.answer(
        "На какой тип уведомления вы хотите подписаться?",
        reply_markup=NotificationType.get_keyboard()  # КНОПКИ
    )


@router_subscription.message(Sub.type)
async def sub_period(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    data = await state.get_data()
    if data.get('periodicity') == NotificationSchedule.NOPE:
        await state.clear()
        await message.answer(
            "Ладно, не буду уведомлять тебя. (￣▽￣)ノ"
        )
        await state.clear()
    else:
        await state.set_state(Sub.periodicity)
        await message.answer(
            "Какую периодичность вы хотите установить?",
            reply_markup=NotificationSchedule.get_keyboard()  # КНОПКИ
        )


@router_subscription.message(Sub.periodicity)
async def sub_hour(message: Message, state: FSMContext):
    await state.update_data(periodicity=message.text)
    await state.set_state(Sub.hour)
    await message.answer(
        "Какое час вы хотите установить?",
        reply_markup=NotificationSchedule.get_time_keyboard()  # КНОПКИ
    )


@router_subscription.message(Sub.hour)
async def sub_minute(message: Message, state: FSMContext):
    await state.update_data(hour=message.text)
    await state.set_state(Sub.minute)
    await message.answer(
        "И минуты, если нужно...",
        reply_markup=NotificationSchedule.get_time_keyboard()  # КНОПКИ
    )


@router_subscription.message(Sub.minute)
async def sub_minute(message: Message, state: FSMContext):
    await state.update_data(minute=message.text)
    data = await state.get_data()
    if data.get('periodicity') == NotificationSchedule.DAILY:
        await save_subscription(message.from_user.id, data)
        await message.answer(
            "Подписка успешно оформлена на ежедневные уведомления!"
        )
        await state.clear()
    else:
        await state.set_state(Sub.week_days)
        await message.answer(
            "В какие дни недели вы хотите получать уведомления?",
            reply_markup=NotificationSchedule.get_time_keyboard()  # КНОПКИ
        )


@router_subscription.message(Sub.week_days)
async def sub_week_days(message: Message, state: FSMContext):
    await state.update_data(week_days=message.text)
    data = await state.get_data()
    await save_subscription(message.from_user.id, data)
    await message.answer(
        "Подписка успешно оформлена. \n"
        "Вы можете узнать какие оповещения у вас есть по команде /schedules"
    )
    await state.clear()
