from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db import create_users_table, add_user, redeem_token, set_subscribed, set_banned,get_user_count, is_user_useAPI, user_exists, is_user_banned,is_user_subscribed
import os
from keepalive import keep_alive
from dotenv import load_dotenv

keep_alive()

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if is_user_banned(user_id)==False: 
        if user_exists(user_id):
            add_user(message.from_user)
            count = get_user_count()
            await message.reply("Welcome! You're now registered.")
            await bot.send_message(chat_id=7674917466,text=message.from_user.first_name+'added to users list successfully\nall users are'+str(count))
        else:
            await message.reply("Welcome! You're already registed.")
    else:
        await message.reply("You're banned.")


@dp.message_handler(commands=["redeem"])
async def redeem_handler(message: types.Message):
    user_id=message.from_user.id
    if is_user_banned(user_id)==False:
        args = message.text.split(maxsplit=1)
        if len(args)<1:
            await message.reply("Usage: /redeem YOUR_API_TOKEN")
        elif args[1] == 'apitoken':
            await message.reply("✅ api token redeemed")
            redeem_token(user_id,True)
        elif is_user_useAPI(user_id)==False:
            await message.reply("✅ you have to get api token first")
        elif is_user_useAPI(user_id):
            if args[1] == '1daykey':
                await message.reply("✅ 1 day key redeem succesfully")
                set_subscribed(user_id,True)
    else:
        await message.reply("You're banned.")

@dp.message_handler(commands=["ban"])
async def ban_handler(message: types.Message):
    user_id=message.from_user.id
    args = message.text.split(maxsplit=1)
    if user_id == 7674917466:
        set_banned(int(args[1]), True)
        await message.reply("🚫 user have been banned.")
    else:
        await message.reply("🚫 Only admin can ban.")


@dp.message_handler(commands=["call"])
async def ban_handler(message: types.Message):
    user_id=message.from_user.id
    if is_user_banned(user_id)==False:
        if is_user_subscribed(user_id):
            await message.reply("you have to buy premium key")
        else:
            await message.reply("you have to subscribe first")

async def on_startup(dp):
    create_users_table()
    print("Bot started.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)