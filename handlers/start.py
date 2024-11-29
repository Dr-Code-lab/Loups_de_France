from loader import dp
from aiogram.filters import CommandStart
from aiogram.types import Message
from db import insert_user_record, update_user_referrals
from keyboards.inline import keyboard, keyboard_game
from log import logger


@dp.message(CommandStart())
async def to_command_start(message: Message):
    """
    This handler receives messages with `/start` command
    """
    # Получаем аргументы из команды
    print("START!", type(message.chat.id), type(message.chat.username), type(message.date), message.text)
    print("!!!!", message)
    # Извлекаем реферальный ID из текста сообщения
    command_args = message.text.split(maxsplit=1)
    referral_id = command_args[1] if len(command_args) > 1 else None
    print("?????", type(referral_id), referral_id)
    logger.info(type(message.chat.id), str(message))
    user_data = dict(id=message.chat.id, name=message.chat.username, date=message.date, referral_id=referral_id)
    await insert_user_record(user_data)
    if referral_id:
        await update_user_referrals(referral_id=referral_id, new_referral_id=str(message.chat.id))
    await message.answer(f"Выберите действие:", reply_markup=keyboard)
    await message.answer(f"Сыграем?", reply_markup=keyboard_game.as_markup())