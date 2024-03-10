import config
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from config import PAYMENTS_TOKEN
from yoomoney import Client, Quickpay

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
TOK =  PAYMENTS_TOKEN

@dp.message(Command('start')) 
async def buy(message: types.Message):
    new = message.from_user.id
    quicklipay = Quickpay(
        receiver="################################",
        quickpay_form="Shop",
        targets="Sponsor",
        paymentType="SB",
        sum=5000, #summ money
        label=new,
    )
    item1 = InlineKeyboardButton(text="Оплатить", url=f'{quicklipay.base_url}')
    item2 = InlineKeyboardButton(text="Проверить оплату", callback_data="check_payment")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[item1, item2]])
    await bot.send_message(message.from_user.id, "Оплатите доступ", reply_markup=keyboard)

@dp.callback_query(F.data == "check_payment")
async def send_random_value(callback: types.CallbackQuery):
    history = Client.operation_history(label=callback.from_user.id)
    for operation in history.operations:
        if operation.status =="success":
            await bot.send_message(callback.from_user.id, text="Оплата получена", show_alert=True)
    else:
        await bot.send_message(callback.from_user.id, text="Оплата не получена", show_alert=True)

async def main():
    await dp.start_polling(bot, skip_updates=False)
if __name__ == "__main__":
    asyncio.run(main())
