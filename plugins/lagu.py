from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import asyncio
import youtube_dl
from bot import Bot
from aiohttp import ClientSession as aiohttpsession

from youtube_search import YoutubeSearch
from helper_func import subscribed, subscriber, subscribe
import requests

import os




## Extra Fns -------------------------------
def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


# Convert hh:mm:ss to seconds
async def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Bot.on_message(filters.command('lagu') & subscribed & subscriber & subscribe)
async def lagu(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = await message.reply('🔎 Mencari lagu yang diminta...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            await m.edit('Lagu tidak ditemukan mohon cari yang lain. .')
            return
    except Exception as e:
        await m.edit(
            "✖️ Tidak ada yang ditemukan.Maaf.\n\nSilahkan cari kata kunci lain."
        )
        print(str(e))
        return
    await m.edit("⏬ Mendownload lagu...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 **Judul**: [{title[:35]}]({link})\n⏳ **Durasi**: `{duration}`\n👁‍🗨 **Views**: `{views}`\n\n𝙱𝚘𝚝 𝙼𝚞𝚕𝚝𝚒𝚏𝚞𝚗𝚐𝚜𝚒 [𝙼.𝚁](t.me/Hyoneechan)'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        await m.delete()
    except Exception as e:
        await m.edit('❌ Error')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

@Bot.on_message(filters.command('lirik') & subscribed & subscriber & subscribe)
async def lirik(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("<b>Mohon berikan nama lirik lagu</b>")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔎 <b>Sedang Mencari lirik lagu</b>")
        resp = requests.get(f"https://api-tede.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("<b>Maaf lirik lagu tidak ditemukan. Mohon berikan judul yang benar")



@Bot.on_message(filters.command('asupan') & subscribed & subscriber & subscribe)
async def asupan(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/asupan/ptl").json()
        results = f"{resp['url']}"
        rep = await message.reply('🔎 Mencari asupan yang mantap...')
        await rep.delete() 
        return await client.send_video(message.chat.id, video=results)
    except Exception:
        await message.reply_text("Telah terjadi kesalahan...")



@Bot.on_message(filters.command('chika') & subscribed & subscriber & subscribe)
async def chika(client, message):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/chika").json()
        results = f"{resp['url']}"
        rep = await message.reply('🔎 Mencari asupan yang mantap...')
        await rep.delete() 
        return await client.send_video(message.chat.id, video=results)
    except Exception:
        await message.reply_text("Telah terjadi kesalahan...")



@Bot.on_message(filters.command('gagal') & subscribed & subscriber & subscribe)
async def gagal(client, message):
    try:
        resp = requests.get("https://api-otakudesux.herokuapp.com/api/asupan?apikey=Alphabot").json()
        results = f"{resp['result']}"
        rep = await message.reply('🔎 Mencari asupan yang mantap...')
        await rep.delete() 
        return await client.send_video(message.chat.id, video=results)
    except Exception:
        await message.reply_text("Telah terjadi kesalahan...")

