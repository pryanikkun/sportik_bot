from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router

router_registration = Router()


class Reg(StatesGroup):
    age = State()
    city = State()


@router_registration.message(Command('registrate'))
async def reg_first(message: Message, state: FSMContext):
    await state.set_state(Reg.age)
    await message.answer("Сколько тебе лет? (цифоркой)")


@router_registration.message(Reg.age)
async def reg_second(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Reg.city)
    await message.answer("В каком городе ты живешь?")


@router_registration.message(Reg.city)
async def reg_third(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    print(data)
    await message.answer(
        f"Ты живешь в {data.get('city')} и тебе {data.get('age')} лет. (￣▽￣)ノ"
    )
    await state.clear()
