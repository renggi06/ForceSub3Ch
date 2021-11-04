from io import BytesIO
from os import path, remove
from time import time

import img2pdf
from PIL import Image
from pyrogram import filters
from pyrogram.types import Message

from bot import Bot
from config import ADMINS
from database.sections import section


async def convert(
    main_message: Message,
    reply_messages,
    status_message: Message,
    start_time: float,
):
    m = status_message

    documents = []

    for message in reply_messages:
        if not message.document:
            return await m.edit("Sorry itu bukan Gambar tipe dokumen, dibatalkan!")

        if message.document.mime_type.split("/")[0] != "image":
            return await m.edit("Sorry jenis mime tidak valid!")

        if message.document.file_size > 5000000:
            return await m.edit("Gambar dokumen sizenya terlau besar!")
        documents.append(await message.download())

    for img_path in documents:
        img = Image.open(img_path).convert("RGB")
        img.save(img_path, "JPEG", quality=100)

    pdf = BytesIO(img2pdf.convert(documents))
    pdf.name = "Telegram.pdf"

    if len(main_message.command) >= 2:
        pdf.name = main_message.text.split(None, 1)[1]

    elapsed = round(time() - start_time, 2)

    await main_message.reply_document(
        document=pdf,
        caption=section(
            "IMG2PDF",
            body={
                "Title": pdf.name,
                "Size": f"{pdf.__sizeof__() / (10**6)}MB",
                "Pages": len(documents),
                "Took": f"{elapsed}s",
        }, 
     ),
    )

    await m.delete()
    pdf.close()
    for file in documents:
        if path.exists(file):
            remove(file)


@Bot.on_message(filters.user(ADMINS) & filters.command("pdf"))
async def img_to_pdf(_, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            "Reply ke sebuah gambar berbentuk dokumen untuk melakukan convert ke pdf."
        )

    m = await message.reply_text("Melakukan convert ke pdf..")
    start_time = time()

    if reply.media_group_id:
        messages = await Bot.get_media_group(
            message.chat.id,
            reply.message_id,
        )
        return await convert(message, messages, m, start_time)

    return await convert(message, [reply], m, start_time)
