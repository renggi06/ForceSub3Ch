import sys
import os
import time
import traceback
import asyncio
import shutil
import heroku3
import psutil
from datetime import datetime

import aiofiles
from functools import wraps
from plugins.lagu import humanbytes
from database.pyrogram import admins_only, get_text
from git.exc import GitCommandError, InvalidGitRepositoryError
from os import environ, execle, path, remove
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from database.bans_sql import ban, unban, all_banned
from config import OWNER_ID, ADMINS, BOT_USERNAME, LOG_FILE_NAME, HEROKU_API_KEY, HEROKU_APP_NAME, USERBOT_PREFIX
from bot import Bot
from database.pastebin import paste
from database.keyboard import ikb


callback = "log_paste"


@Bot.on_message(filters.command("logs") & filters.user(OWNER_ID))
async def logs_chat(_, message):
    time = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    caption = f"""
𝗪𝗮𝗸𝘁𝘂 : {time}
𝗧𝗶𝗽𝗲 𝗟𝗼𝗴 : 𝙴𝚛𝚛𝚘𝚛
"""
    try:
        await message.reply_document(
            LOG_FILE_NAME, caption=caption
        )
    except ValueError:
        await message.reply_text("**LOGS ARE EMPTY**")


@Bot.on_callback_query(filters.regex(callback))
async def paste_log_neko(_, cq: CallbackQuery):
    if cq.from_user.id not in OWNER_ID:
        return await cq.answer(
            "Stop clicking at whichever thing you come across."
        )
    async with aiofiles.open(LOG_FILE_NAME, mode="r") as f:
        link = await paste(await f.read())
    message: Message = cq.message
    return await message.edit_caption(
        f"{message.caption.markdown}\n**Paste:** {link}"
    )

@Bot.on_message(filters.command("tagall") & ~filters.edited & ~filters.bot)
@admins_only
async def tagall(client, message):
    sh = get_text(message)
    if not sh:
        sh = "Hi!"
    mentions = ""
    async for member in client.iter_chat_members(message.chat.id):
        mentions += member.user.mention + " "
    n = 4096
    kk = [mentions[i : i + n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"<b>{sh}</b> \n{i}"
        await client.send_message(message.chat.id, j, parse_mode="html")

@Bot.on_message(filters.regex(pattern='.*#all.*') & ~filters.edited & ~filters.bot)
@admins_only
async def tagall(client, message):
    sh = get_text(message)
    if not sh:
        sh = "Hi!"
    mentions = ""
    async for member in client.iter_chat_members(message.chat.id):
        mentions += member.user.mention + " "
    n = 4096
    kk = [mentions[i : i + n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"<b>{sh}</b> \n{i}"
        await client.send_message(message.chat.id, j, parse_mode="html")

@Bot.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    await message.reply_text(
        text=f"🖥 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗸 𝗦𝗶𝘀𝘁𝗲𝗺 𝗕𝗼𝘁 @{BOT_USERNAME} 💫\n\n🤖 𝗕𝗼𝘁 𝗩𝗲𝗿𝘀𝗶𝗼𝗻: V2.9.1\n\n💾 𝗗𝗶𝘀𝗸 𝗨𝘀𝗮𝗴𝗲,\n ↳Total Disk Space:{total} \n ↳Used:{used}({disk_usage}%) \n ↳Free:{free} \n\n🎛 𝗛𝗮𝗿𝗱𝘄𝗮𝗿𝗲 𝗨𝘀𝗮𝗴𝗲,\n↳CPU Usage:{cpu_usage}% \n ↳RAM Usage:{ram_usage}%",
        parse_mode="Markdown",
        quote=True
    )




@Bot.on_message(filters.regex(pattern='.*thanks.*') & filters.user(OWNER_ID))
async def _tiktok(Bot, update):
  await update.reply('You are welcome sir') 

