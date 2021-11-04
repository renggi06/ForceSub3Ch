import os
import json
import time
import asyncio

from asyncio.exceptions import TimeoutError

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

API_TEXT = """Hai {}, apa kabar? 

Gua juga dapat membuat String Session.
Untuk menghasilkan sesi string, kirimkan gua <code>API_ID</code> akun lo
"""
HASH_TEXT = "Ok Sekarang kirim <code>API_HASH</code> Lo untuk lanjut.\n\n<b>Tekan /cancel untuk membatalkan</b>."
PHONE_NUMBER_TEXT = (
    "📞 <i>Sekarang kirim no telepon akun Telegram lo"
    " Sertakan kode negara.</i>\n<b>Contoh:</b> <code>+6285124562345</code>\n\n"
    "<b>Tekan /cancel untuk membatalkan</b>."
)



@Client.on_message(filters.private & filters.command("pyrogram"))
async def generate_str(c, m):
    get_api_id = await c.ask(
        chat_id=m.chat.id,
        text=API_TEXT.format(m.from_user.mention),
        filters=filters.text
    )
    api_id = get_api_id.text
    if await is_cancel(m, api_id):
        return

    await get_api_id.delete()
    await get_api_id.request.delete()
    try:
        check_api = int(api_id)
    except Exception:
        await m.reply("<code>⚠️ API_ID Tidak valid !</code>\n\nTekan /pyrogram Untuk membuat kembali.")
        return

    get_api_hash = await c.ask(
        chat_id=m.chat.id, 
        text=HASH_TEXT,
        filters=filters.text
    )
    api_hash = get_api_hash.text
    if await is_cancel(m, api_hash):
        return

    await get_api_hash.delete()
    await get_api_hash.request.delete()

    if not len(api_hash) >= 30:
        await m.reply("<code>⚠️ API_HASH Tidak valid !</code><code>⚠️ API_ID Tidak valid !</code>\n\nTekan /pyrogram Untuk membuat kembali.")
        return

    try:
        client = Client(":memory:", api_id=api_id, api_hash=api_hash)
    except Exception as e:
        await c.send_message(m.chat.id ,f"<b>Terjadi Kesalahan</b><code>{str(e)}</code><code>⚠️ API_ID Tidak valid !</code>\n\nTekan /pyrogram Untuk membuat kembali.")
        return

    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()
    while True:
        get_phone_number = await c.ask(
            chat_id=m.chat.id,
            text=PHONE_NUMBER_TEXT
        )
        phone_number = get_phone_number.text
        if await is_cancel(m, phone_number):
            return
        await get_phone_number.delete()
        await get_phone_number.request.delete()

        confirm = await c.ask(
            chat_id=m.chat.id,
            text=f'🤔 Apakah <code>{phone_number}</code> benar? (y/n): \n\nKetik: <code>y</code> (jika iya)\nKetik: <code>n</code> (jika tidak)'
        )
        if await is_cancel(m, confirm.text):
            return
        if "y" in confirm.text.lower():
            await confirm.delete()
            await confirm.request.delete()
            break
    try:
        code = await client.send_code(phone_number)
        await asyncio.sleep(1)
    except FloodWait as e:
        await m.reply(f"__Mohon maaf lo harus menunggu {e.x} detik 😞__")
        return
    except ApiIdInvalid:
        await m.reply("<b>🕵‍♂ API_ID dan API_HASH lo tidak valid.</b>\n\nTekan /pyrogram Untuk membuat kembali.")
        return
    except PhoneNumberInvalid:
        await m.reply("<b>☎ Nomor telepon tele lo tidak valid.</b>\n\nTekan /pyrogram Untuk membuat kembali.")
        return

    try:
        sent_type = {"app": "Telegram App 💌",
            "sms": "SMS 💬",
            "call": "Phone call 📱",
            "flash_call": "phone flash call 📲"
        }[code.type]
        otp = await c.ask(
            chat_id=m.chat.id,
            text=(f"Gua sudah ngirim kode OTP Ke nomor <code>{phone_number}</code> melalui {sent_type}\n\n"
                  "Silakan masukkan OTP dalam format <code>1 2 3 4 5</code> <i>(beri spasi diantara nomor)</i>\n\n"
                  "Jika Bot tidak mengirim OTP maka coba /start ke Telegram App 💌\n\n"
                  "Tekan /cancel untuk membatalkan."), timeout=300)
    except TimeoutError:
        await m.reply("<b>⏰ Waktu habis:</b>Anda mencapai batas waktu 5 menit.\n\nTekan /pyrogram Untuk membuat kembali.")
        return
    if await is_cancel(m, otp.text):
        return
    otp_code = otp.text
    await otp.delete()
    await otp.request.delete()
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        await m.reply("<b>📵 OTP tidak valid</b>\n\nTekan /pyrogram Untuk membuat kembali.")
        return 
    except PhoneCodeExpired:
        await m.reply("<b>⌚ OTP kadaluwarsa</b>\n\nTekan /pyrogram Untuk membuat kembali.")
        return
    except SessionPasswordNeeded:
        try:
            two_step_code = await c.ask(
                chat_id=m.chat.id, 
                text="<code>🔐 Akun ini memiliki kode verifikasi dua langkah.\nMasukkan kode autentikasi faktor kedua lo.</code>\n\nTekan /cancel untuk membatalkan.",
                timeout=300
            )
        except TimeoutError:
            await m.reply("<b>⏰ Waktu habis:</b>Lo mencapai batas waktu 5 menit.\n\nTekan /pyrogram Untuk membuat kembali.")
            return
        if await is_cancel(m, two_step_code.text):
            return
        new_code = two_step_code.text
        await two_step_code.delete()
        await two_step_code.request.delete()
        try:
            await client.sign_in(password=password)
        except Exception as e:
            await m.reply(f"<b>⚠️ ERROR:</b><code>{str(e)}</code>")
            return
    except Exception as e:
        await c.send_message(m.chat.id ,f"<b>⚠️ ERROR:</b><code>{str(e)}</code>")
        return
    try:
        string_session = client.session.save()
        await client.send_message("me", f"<b>String session lo 👇</code>\n\n<code>{session_string}</code>\n\nTerimakasih sudah menggunakan {(await c.get_me()).mention}")
        text = "✅ Sukses membuat string session lo dan telah dikirim ke pesan tersimpan\nCek pesan tersimpan dengan menekan."
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="String Session ↗️", url=f"tg://openmessage?user_id={m.chat.id}")]]
        )
        await c.send_message(m.chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        await c.send_message(m.chat.id ,f"<b>⚠️ ERROR:</b><code>{str(e)}</code>")
        return
    try:
        await client.stop()
    except:
        pass


@Client.on_message(filters.private & ~filters.forwarded & filters.command('telethon'))
async def generate_session(bot, msg, telethon=True):
    await msg.reply("Starting {} Session Generation...".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'Please send your `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('Not a valid API_ID (which must be an integer). Please start generating session again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'Please send your `API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'Now please send your `PHONE_NUMBER` along with the country code. \nExample : `+19876543210`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("Sending OTP...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` and `API_HASH` combination is invalid. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`PHONE_NUMBER` is invalid. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "Please check for an OTP in official telegram account. If you got it, send OTP here after reading the below format. \nIf OTP is `12345`, **please send it as** `1 2 3 4 5`.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('Time limit reached of 10 minutes. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('OTP is invalid. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('OTP is expired. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'Your account has enabled two-step verification. Please provide the password.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('Time limit reached of 5 minutes. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('Invalid Password Provided. Please start generating session again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} STRING SESSION** \n\n`{}` \n\nGenerated by @StarkStringGenBot".format("TELETHON" if telethon else "PYROGRAM", string_session)
    await client.send_message("me", text)
    await client.disconnect()
    await phone_code_msg.reply("Successfully generated {} string session. \n\nPlease check your saved messages! \n\nBy @StarkBots".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the Process!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("Restarted the Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancelled the generation process!", quote=True)
        return True
    else:
        return False



@Client.on_callback_query(filters.regex('^close$'))
async def close(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("⛔ Proses string session dibatalkan.")
        return True
    return False

