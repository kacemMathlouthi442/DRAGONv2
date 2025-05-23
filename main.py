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
        await bot.send_message(chat_id=7674917466,text=get_user_first_name(int(args[1]))+' unbanned successfully!')
        try:
            await bot.unban_chat_member(chat_id=-1002420776698, user_id=int(args[1]))
            await bot.send_message(chat_id=7674917466,text="User "+get_user_first_name(int(args[1]))+" has been unbanned from the channel.")
        except Exception as e:
            await bot.send_message(chat_id=7674917466,text="Failed to unban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")

@dp.message(Command("ban")) # DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if user_id == 7674917466 or user_id == 7575518830:
        args = message.text.split(maxsplit=1)
        set_banned(int(args[1]),True)
        await bot.send_message(chat_id=7674917466,text=get_user_first_name(int(args[1]))+' banned successfully!')

        for msg_id in range(message.message_id - 200, message.message_id):
            try:
                await bot.delete_message(chat_id=int(args[1]), message_id=msg_id)
            except:
                pass
        try:
            await bot.ban_chat_member(chat_id=-1002420776698, user_id=int(args[1]))
            await bot.send_message(chat_id=7674917466,text="User "+get_user_first_name(int(args[1]))+" has been banned from the channel.")
        except Exception as e:
            await bot.send_message(chat_id=7674917466,text="Failed to ban user: "+str(e))
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
            await bot.send_message(chat_id=7674917466,text='🆕 *New user*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_first_name(iduser))+'`\n*User ID*\: `'+str(iduser)+'`\n*Total users*\: '+str(get_user_count()),parse_mode='MarkdownV2')
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
    if is_user_banned(user_id)==False:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("❌ Please add your activation key. /redeem [activation key]")
        elif args[1] == 'PTd82e519c42cc97d5066b4423c718c8a132ebaf07dab24d32':
            sleep(1)
            await message.answer("⌛ Please wait.")
            sleep(5)
            redeem_token(user_id,True)
            await message.answer("✅ API Token redeemed successfuly!")
        else:
            if args[1] == 'DRAGONOTP-F4awb4Vf1KJp7P4LhCa1':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 1-Day key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-F4awb4Vf1KJp7P4LhCa2':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 2-Days key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-F4awb4Vf1KJp7P4LhCa7':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 1-Week key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-F4awb4Vf1KJp7P4LhC14':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 2-Weeks key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-F4awb4Vf1KJp7P4LhC30':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 1-Month key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an IP activator.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-F4awb4Vf1KJp7P4LhC60':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ 2-Months key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you can't redeem the key, you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-C4awb4Vf1KJp7P4LhCaN':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ Custom key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP-C4awb4Vf1KJp7P4LhClT':
                if is_user_useAPI(user_id):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(5)
                    await message.answer("✅ LifeTime key redeemed successfuly!")
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
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram you have to buy an APi token.\n\nContact the support to buy one.",reply_markup=keyboard)
            elif args[1] == 'DRAGONOTP1-C4awb4Vf1KJp7P4LhCaN':
                sleep(1)
                await message.answer("⌛ Please wait.")
                sleep(5)
                await message.answer("✅ Premium key redeemed successfuly!")
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
                    await bot.send_message(chat_id=7674917466,text="User "+get_user_first_name(user_id)+" has been banned from the channel.")
                except Exception as e:
                    await bot.send_message(chat_id=7674917466,text="Failed to ban user: "+str(e))
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
                    await message.answer("❌ ERROR[302]\n\n Sorry your country doesen't support the spofing.\n\nYou have to Buy a premium access.\n\n❕ the call from your country it's soo expensive in the premium access you will get a full control of the bot but you have to cost more.\nSorry for your time and thanks for your attention.\nContact the support to buy a premium subscription.",reply_markup=keyboard)
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

• 🕐 1 Day Access \— *$25*

• 🕑 2 Days Access \— *$30*

• 🗓️ 1 Week Plan \— *$40*

• 🗓️ 2 Weeks Plan \— *$55*

• 📆 1 Month Plan \— *$70*

• 📆 2 Months Plan \— *$100*

• ♾️ Lifetime Access \— *$350*

━━━━━━━━━━━━━━━━━━━

📩 How to Activate
After completing your payment\:

Take a screenshot of your payment confirmation\.

Send it to *SUPPORT* to verify and activate your subscription\.

❓ Need Help?
Have questions or need a different wallet option?
📬 Contact *SUPPORT* \— we’re here to assist\.""",parse_mode='MarkdownV2',reply_markup=keyboard)
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
