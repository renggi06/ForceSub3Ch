import imghdr
import os
from asyncio import gather
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (PeerIdInvalid, ShortnameOccupyFailed,
                             StickerEmojiInvalid, StickerPngDimensions,
                             StickerPngNopng, UserIsBlocked)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import Bot
from config import BOT_USERNAME
from database.files import (get_document_from_file_id,
                             resize_file_to_sticker_size, upload_document)
from database.stickerset import (add_sticker_to_set, create_sticker,
                                  create_sticker_set, get_sticker_set_by_name)



@Bot.on_message(filters.command("sticker_id") & ~filters.edited)
async def sticker_id(_, message: Message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply("Mohon Reply ke sebuah sticker.")

    if not reply.sticker:
        return await message.reply("Mohon Reply ke sebuah sticker.")

    await message.reply_text(f"<b>Info id Sticker:  </b><code>{reply.sticker.file_id}</code></>")


@Bot.on_message(filters.command("get_sticker") & ~filters.edited)
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("Mohon Reply ke sebuah sticker.")

    if not r.sticker:
        return await message.reply("Mohon Reply ke sebuah sticker.")

    m = await message.reply("Mengirim...")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)

