#(©)Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from bot import Bot
import youtube_dl
from youtube_search import YoutubeSearch
import requests
import os
from config import ADMINS
from datetime import datetime
from helper_func import encode, get_message_id



## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Teruskan Pesan Pertama dari Saluran DB (dengan Kutipan)..\n\atau Kirim Tautan Posting Saluran DB", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=30)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Gagal\n\Postingan yang Diteruskan ini bukan dari Saluran DB saya atau Tautan ini diambil dari Saluran DB", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Teruskan Pesan Pertama dari Saluran DB (dengan Kutipan)..\n\atau Kirim Tautan Posting Saluran DB", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=30)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Gagal\n\nPostingan yang Diteruskan ini bukan dari Saluran DB saya atau Tautan ini diambil dari Saluran DB", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    first = message.from_user.first_name
    username = None if not message.from_user.username else '@' + message.from_user.username
    id = message.from_user.id
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 BAGIKAN LINK", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>SUPPORT  BYE <a href='https://t.me/joinchat/ch4zradg1gJjM2M1'>𝘼𝙣𝙖𝙩𝙝𝙚𝙢𝙖</a></b>\n\n<b>👤 Admin:</b> {first} \n<b>🏷️ Username:</b> {username} \n<b>⚡ ID admin:</b> /n<b>📎 Link:</b> <a href='{link}'>Salin</a>", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.command('help') & filters.private)
async def _help(client: Client, message: Message):
  await message.reply_text("""Hai, Apa kabar? terimakasih telah menggunakan saya

<b>Perintah utama :</b>
 •/start - memulai penggunaan bot
 •/help - melihat bantuan dan perintah bot
""", 
reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "FUN", callback_data = "fun"
                    ), 
                     InlineKeyboardButton(
                        "FILES",  callback_data = "files"
                    ), 
                    InlineKeyboardButton(
                        "SPESIAL", callback_data = "spesial"
                    )
                ], [
                   InlineKeyboardButton(
                        "AUTHOR BOT", callback_data = "author"
                    )
            ]
           ]
        ),
    )

@Bot.on_message(filters.command('info'))
async def me(c, m):
    """ This will be sent when /me command was used"""

    me = await c.get_users(m.from_user.id)
    text = "𝗜𝗻𝗳𝗼 𝗗𝗲𝘁𝗮𝗶𝗹 𝗣𝗮𝘀𝗰𝗼𝗹 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺:\n\n"
    text += f"🦚 First Name: <code>{me.first_name}</code>\n"
    text += f"🐧 Last Name: <code>{me.last_name}</code>\n" if me.last_name else ""
    text += f"👁 Username: @{me.username}\n" if me.username else ""
    text += f"👤 User Id: <code>{me.id}</code>\n"
    text += f"💬 DC ID: {me.dc_id}\n" if me.dc_id else ""
    text += f"✔ Is Verified By TELEGRAM: <code>{me.is_verified}</code>\n" if me.is_verified else ""
    text += f"👺 Is Fake: {me.is_fake}\n" if me.is_fake else ""
    text += f"💨 Is Scam: {me.is_scam}\n" if me.is_scam else ""
    text += f"📃 Language Code: {me.language_code}\n" if me.language_code else ""

    await m.reply_text(text, quote=True)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Teruskan Pesan Pertama dari Saluran DB (dengan Kutipan)..\n\atau Kirim Tautan Posting Saluran DB", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=30)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Gagal\n\nPostingan yang Diteruskan ini bukan dari Saluran DB saya atau Tautan ini diambil dari Saluran DB", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    first = message.from_user.first_name
    username = None if not message.from_user.username else '@' + message.from_user.username
    id = message.from_user.id
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 BAGIKAN LINK", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>SUPPORT  BYE <a href='https://t.me/joinchat/ch4zradg1gJjM2M1'>𝘼𝙣𝙖𝙩𝙝𝙚𝙢𝙖</a></b>\n\n<b>👤 Admin:</b> {first} \n<b>🏷️ Username:</b> {username} \n<b>⚡ ID admin:</b> \n<b>📎 Link:</b> <a href='{link}'>Salin</a></b>\n\n{link}", quote=True, reply_markup=reply_markup)

@Bot.on_message(filters.user(ADMINS) & filters.command('ping'))
async def ping_signal(client: Client, message: Message):
    start = datetime.now()
    tauk = await message.reply('Pong!')
    end = datetime.now()
    m_s = (end - start).microseconds/ 1000
    await tauk.edit(f"<b>Pong! ⚡ </b>\n {m_s} ms")
    
@Bot.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(client: Client, message: Message):
  return await message.reply_text("<b>✅ Anathema Bot Telah online ! </b>") 
    

@Bot.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(client: Client, message: Message):
	await message.reply_text("""Hubungi gua di pm untuk melihat bantuan""", 
	reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝘽𝙖𝙣𝙩𝙪𝙖𝙣",
                        url=f"t.me/{client.username}",
                    )
                ]
            ]
        ),
    )
