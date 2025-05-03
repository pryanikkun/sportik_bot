import logging

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from app_notification.db import (
    save_subscription,
    get_subscription_by_user,
    stop_subscription,
)

from ..keyboards.inline import (
    days_keyboard,
    inline_types,
    inline_hours,
    inline_minutes,
    inline_unsub
)
router_subscription = Router()


async def get_beautiful_schedule(schedule: dict) -> str:
    """Преобразование расписания в красивый вид"""
    days_dict = {
        0: 'пн',
        1: 'вт',
        2: 'ср',
        3: 'чт',
        4: 'пт',
        5: 'сб',
        6: 'вс'
    }
    days = schedule.get('days')
    hour = schedule.get('hour')
    minutes = schedule.get('minutes')
    if minutes == 0:
        minutes = '00'
    if hour < 10:
        hour = f"0{hour}"
    days_str = (
        'ежедневно' if days == list(range(7))
        else ', '.join([days_dict[day] for day in days])
    )
    return f"{days_str} в {hour}:{minutes}"


@router_subscription.message(Command('subscription_list'))
async def sub_list(message: Message):
    """Показать список подписок."""
    subscriptions = await get_subscription_by_user(message.from_user.id)
    if not subscriptions:
        await message.answer(
            "У тебя пока нет подписок. "
            "Ты можешь подписаться на них с помощью /subscribe"
        )
        return
    text = "Вот твои подписки:\n"
    for sub in subscriptions:
        schedule_str = await get_beautiful_schedule(sub.schedule)
        text += f"{sub.type.name.title()}: {schedule_str}\n"
    await message.answer(text)


@router_subscription.message(Command('unsubscribe'))
async def unsub(message: Message):
    """Отписаться от подписки."""
    await message.answer(
        "Тыкни подписку, от которой хочешь отписаться",
        reply_markup=await inline_unsub(message.from_user.id),
    )


@router_subscription.callback_query(F.data.startswith("unsub_"))
async def unsub_callback(callback: CallbackQuery):
    """Обработка отписки."""
    subscription_id = int(callback.data.split("_")[1])
    try:
        await stop_subscription(subscription_id)
    except Exception:
        logging.exception(
            f"Проблемы с удалением подписки {subscription_id}"
        )
        await callback.answer("Что-то пошло не так, попробуй позже")
        return
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        "Всё, не буду больше тебе писать\n"
        "(шучу (¬‿¬ ), жду твоих подписочек)"
    )


class SubState(StatesGroup):
    user_id = State()
    type = State()
    hour = State()
    minutes = State()
    days = State()


@router_subscription.message(Command('subscribe'))
async def sub_type(message: Message, state: FSMContext):
    """Начало оформления подписки. Выбор типа."""
    await state.set_state(SubState.user_id)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(SubState.type)
    await message.answer(
        "Ну вот ты и дошел до регистрации. Готовься, придётся много тыкать.\n"
        "Начнем с простого. Выбери о чем ты хочешь получать напоминание?\n"
        "PS - если хочешь выбрать несколько напоминаний, но не все, "
        "нужно подписаться на каждое по отдельности. \n"
        "PPS - если ты выберешь тип, на который уже подписан, "
        "то я обновлю настройки предыдущей подписки",
        reply_markup=inline_types,
    )


@router_subscription.callback_query(SubState.type, F.data.startswith("type_"))
async def sub_days(callback: CallbackQuery, state: FSMContext):
    """Сохранение типа подписки и выбор дня."""
    choice = callback.data.split("_")[1]
    await state.update_data(type=int(choice))
    await callback.message.edit_reply_markup()
    await state.set_state(SubState.days)
    await callback.message.answer(
        "Предупреждаю, раз в неделю я точно буду тебя тормошить, "
        "но есть возможность ограничить моё рвение здесь и сейчас.\n"
        "В какие дни я могу тебе писать?\n",
        reply_markup=days_keyboard(),
    )


@router_subscription.callback_query(SubState.days, F.data.startswith("day_"))
async def process_days_selection(callback: CallbackQuery, state: FSMContext):
    """Процесс выбора дней."""
    choice = callback.data.split("_")[1]
    day_number = int(choice)
    data = await state.get_data()
    selected_days = data.get("days", [])

    if day_number in selected_days:
        selected_days.remove(day_number)
    else:
        selected_days.append(day_number)

    await state.update_data(days=selected_days)

    # Обновляем клавиатуру
    await callback.message.edit_reply_markup(
        reply_markup=days_keyboard(selected_days)
    )
    await callback.answer()


@router_subscription.callback_query(SubState.days, F.data.startswith("days_"))
async def process_days_done(callback: CallbackQuery, state: FSMContext):
    """Завершение выбора дней. Переход к выбору часов."""
    choice = callback.data.split("_")[1]
    if choice == 'all':
        selected_days = list(range(7))
    else:
        data = await state.get_data()
        selected_days = data.get("days", [])

    if not selected_days:
        await callback.answer("Нужно выбрать хотя бы один день!",
                              show_alert=True)
        return

    await state.update_data(days=selected_days)
    await callback.message.edit_reply_markup()
    await state.set_state(SubState.hour)
    await callback.message.answer(
        "Фух, с днями разобрались, дело за малым.\n"
        "Какой час ты хочешь установить? "
        "(Учти, именно в этот час я буду высылать напоминание в выбранные дни)",
        reply_markup=inline_hours,
    )


@router_subscription.callback_query(SubState.hour, F.data.startswith("hour_"))
async def sub_hours(callback: CallbackQuery, state: FSMContext):
    """Сохранение выбора часа. Переход к выбору минут."""
    choice = callback.data.split("_")[1]
    await state.update_data(hour=int(choice))
    await callback.message.edit_reply_markup()
    await state.set_state(SubState.minutes)
    await callback.message.answer(
        "Теперь минуты... (начинается барабанная дробь ヾ( `ー´)シ)",
        reply_markup=inline_minutes,
    )


@router_subscription.callback_query(F.data == "cancel")
async def sub_cancel(callback: CallbackQuery, state: FSMContext):
    """Отмена подписки."""
    await callback.message.edit_reply_markup()
    await callback.message.answer("Штош, тогда в следующий раз 〜〜(／￣▽)／")
    await state.clear()


@router_subscription.callback_query(SubState.minutes, F.data.startswith("min_"))
async def sub_final(callback: CallbackQuery, state: FSMContext):
    """Сохранение выбора минут. Завершение оформления подписки."""
    choice = callback.data.split("_")[1]
    await state.update_data(minutes=int(choice))
    await callback.message.edit_reply_markup()
    data = await state.get_data()
    user_id = data.get('user_id')
    type = data.get('type')
    schedule = {
        'hour': data.get('hour'),
        'minutes': data.get('minutes'),
        'days': data.get('days')
    }
    try:
        await save_subscription(
            user_id=user_id,
            schedule=schedule,
            type_id=type
        )
    except Exception:
        logging.exception(
            f"Проблемы с подпиской у пользователя {user_id}"
            f" на тип {type} c расписанием {schedule}")
        await callback.message.answer("Что-то пошло не так, попробуй позже")
        return

    await callback.message.answer(
        "Регистрация завершена ＼(≧▽≦)／ \n"
        "И я всё запомнил. \n\n"
        "Хочешь подписаться на что-то ещё? Тыкни /subscribe\n"
        "Если хочешь глянуть все свои подписки, то /subscription_list\n"
        "Вдруг передумал и хочешь отписаться от чего-то тыкай /unsubscribe\n"
    )
    await state.clear()
