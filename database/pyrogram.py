import asyncio
import math
import shlex
import sys
import time
import traceback
from functools import wraps
from typing import Callable, Coroutine, Dict, List, Tuple, Union

from PIL import Image
from pyrogram import Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Chat, Message, User
from config import OWNER_ID, CHANNEL_ID
from bot import Bot

def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None



admins: Dict[str, List[User]] = {}


def set(chat_id: Union[str, int], admins_: List[User]):
    if isinstance(chat_id, int):
        chat_id = str(chat_id)

    admins[chat_id] = admins_


def get(chat_id: Union[str, int]) -> Union[List[User], bool]:
    if isinstance(chat_id, int):
        chat_id = str(chat_id)

    if chat_id in admins:
        return admins[chat_id]

    return False

async def get_administrators(chat: Chat) -> List[User]:
    _get = get(chat.id)

    if _get:
        return _get
    else:
        set(
            chat.id,
            [member.user for member in await chat.get_members(filter="administrators")],
        )
        return await get_administrators(chat)


def admins_only(func: Callable) -> Coroutine:
    async def wrapper(client: Client, message: Message):
        if message.from_user.id == OWNER_ID:
            return await func(client, message)
        admins = await get_administrators(message.chat)
        for admin in admins:
            if admin.id == message.from_user.id:
                return await func(client, message)

    return wrapper

