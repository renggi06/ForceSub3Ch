#(©)Codexbotz
import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, FORCE_MSG, URL_GROUP, URL_VIRAL, CPT_SATU, START_MSG, CPT_DUA, OWNER_ID, CPT_TIGA, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, START_IMG
from helper_func import subscribed, subscriber, subscribe, encode, decode, get_messages
from database.support import users_info
from database.sql import add_user, query_msg

#=====================================================================================##

USERS_LIST = """<b>📂 Total:</b>\n\n📈 Pelanggan - {}\n🔒 Terblokir- {}"""

WAIT_MSG = """"<b>Memproses ...</b>"""

REPLY_ERROR = """<code>Gunakan perintah ini dengan replay ke pesan telegram apa pun tanpa spasi.</code>"""


#=====================================================================================##


@Bot.on_message(filters.command('start') & filters.private & subscribed & subscriber & subscribe)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    user_name = '@' + message.from_user.username if message.from_user.username else None
    await add_user(id, user_name)
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Mohon tunggu dan bersabar...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Ops Telah terjadi kesalahan..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(CPT_SATU, url= client.invitelink)
     
                ],
                [
                    InlineKeyboardButton(CPT_DUA, url= URL_VIRAL)
     
                ],
                [ 
                   InlineKeyboardButton(CPT_TIGA, url=URL_GROUP)
                ],

                [
                   InlineKeyboardButton("🛠 𝘼𝙪𝙩𝙝𝙤𝙧 𝘽𝙤𝙩", url=f"https://t.me/Hyoneechan")
                ]
                
            ]
        )
        await message.reply_animation(
                START_IMG, 
                caption = START_MSG.format(
                message.from_user.first_name,
                
            ),
            reply_markup = reply_markup,   
            quote = True
     ) 
 
    return


@Bot.on_message(filters.command('start') & filters.private)
async def not_join(client: Client, message: Message):
    text = "<b>Hai Untuk menggunakan bot ini Lo wajib bergabung pada channel (porn/viral) dan group dibawah ini</b>"
    message_text = message.text
    try:
        command, argument = message_text.split()
        text = text + f" <b>Setelah itu silahkan mulai ulang tekan tulisan biru ini <a href='https://t.me/{client.username}?start={argument}'>Ulang</a></b>"
    except ValueError:
        pass
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙋𝙤𝙧𝙣", url = client.invitelink), InlineKeyboardButton("𝙂𝙧𝙤𝙪𝙥 𝙎𝙖𝙣𝙜𝙚", url= URL_GROUP)], [InlineKeyboardButton("𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙑𝙞𝙧𝙖𝙡", url = URL_VIRAL) ]])
    await message.reply(
        text = text,
        reply_markup = reply_markup,
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.user(ADMINS) & filters.command('users'))
async def subscribers_count(bot, m: Message):
    id = m.from_user.id
    if id not in ADMINS:
        return
    msg = await m.reply_text(WAIT_MSG)
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]
    await m.delete()
    await msg.edit(USERS_LIST.format(active, blocked))


@Bot.on_message(filters.user(ADMINS) & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(bot, m: Message):
    id = m.from_user.id
    if id not in ADMINS:
        return
    if (" " not in m.text) and ("broadcast" in m.text) and (m.reply_to_message is not None):
        query = await query_msg()
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id,
                    caption=m.caption,
                    reply_markup=m.reply_markup
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception:
                pass
    else:
        msg = await m.reply_text(REPLY_ERROR, m.message_id)
        await asyncio.sleep(8)
        await msg.delete()
