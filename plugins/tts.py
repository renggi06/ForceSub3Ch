import traceback
from asyncio import get_running_loop
from io import BytesIO

from googletrans import Translator
from gtts import gTTS
from pyrogram import filters
from pyrogram.types import Message

from bot import Bot

def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio

@Bot.on_message(filters.command("tts"))
async def text_to_speech(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Mohon reply suatu pesan...")
    if not message.reply_to_message.text:
        return await message.reply_text("Mohon reply suatu pesan...")
    m = await message.reply_text("Memproses audio..")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await message.reply_audio(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)
