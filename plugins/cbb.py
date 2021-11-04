#(©)Codexbotz

from pyrogram import Client, filters, __version__
from bot import Bot
from config import OWNER_ID, URL_GROUP, URL_VIRAL
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("fun"))
async def fun(_, query: CallbackQuery):
    await query.edit_message_text(
  """<b>Berikut bantuan untuk Modul Fun :</b>

 •/lagu - mendownload lagu
 •/lirik - mencari lirik lagu
 •/tts - convert teks ke audio
 •/info - cek info akun telegram""", 
reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Kembali", callback_data="cbback"
                    )
]
]
) 
)

@Client.on_callback_query(filters.regex("files"))
async def files(_, query: CallbackQuery):
    await query.edit_message_text(
  """<b>Berikut bantuan untuk Modul Files :</b>

Hanya Untuk Admin
 •/batch - buat tautan untuk lebih dari satu postingan
 •/genlink - buat tautan untuk satu postingan """, 
reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Kembali", callback_data="cbback"
                    )
]
]
) 
)

@Client.on_callback_query(filters.regex("spesial"))
async def spesial(_, query: CallbackQuery):
    await query.edit_message_text(
  """<b>Berikut bantuan untuk Modul Spesial :</b>

Hanya Untuk Admin bot
 •/broadcast - melakukan pesan siaran 
 •/users - melihat statistik bot
 •/ping - melihat speed bot
 •/pdf - convert beberapa gambar ke file pdf

Untuk Pengguna Telegram
 •/get_sticker - convert sticker ke gambar
 •/asupan - mencari konten asupan 
 •/chika - mencari konten asupan chika tiktok
 •/sticker_id - cek info id suatu sticker
 •𝗨𝗥𝗟 𝗦𝗵𝗼𝗿𝘁𝗻𝗲𝗿: Perpendek suatu url/tautan, untuk menggunakan ini kirimkan saja link ke sini otomatis tautan akan diproses.""", 
reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Kembali", callback_data="cbback"
                    )
]
]
) 
) 


@Client.on_callback_query(filters.regex("author"))
async def author(_, query: CallbackQuery):
    await query.edit_message_text(
  """<b>Berikut bantuan untuk Modul Author Bot :</b>

Hanya Untuk Authot bot
 •/logs - melihat catatan masalah bot yang sedang terjadi
 •/broadcast - melakukan pesan siaran 
 •/users - melihat statistik bot
 •/ping - melihat speed bot """, 
reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Kembali", callback_data="cbback"
                    )
]
]
) 
)




@Client.on_callback_query(filters.regex("cbback"))
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text("""<b>Perintah utama :</b>
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
