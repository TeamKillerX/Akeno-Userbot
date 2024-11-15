# Copyright (C) 2020-2024 TeamKillerX <https://github.com/TeamKillerX>
#
# This file is part of TeamKillerX project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

import re

import emoji
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import *

from Akeno.utils.base_sqlite import *
from Akeno.utils.handler import *
from Akeno.utils.prefixprem import command
from config import *


@Akeno(
    ~filters.scheduled
    & command(["setprefix"])
    & filters.me
    & ~filters.forwarded
)
async def set_prefix(client: Client, message: Message):
    user_id = message.from_user.id
    if not message.text or len(message.text.split()) < 2:
        await message.reply_text("Usage: ?setprefix custom emoji or None")
        return
    new_prefix_text = message.text.split(maxsplit=1)[1]
    if client.me.is_premium:
        if message.entities:
            for entity in message.entities:
                if entity.type == MessageEntityType.CUSTOM_EMOJI and entity.offset >= len(message.text.split()[0]) + 1:
                    custom_emoji_id = entity.custom_emoji_id
                    await set_prefix_in_db(user_id, custom_emoji_id)
                    await message.reply_text(f"Custom emoji prefix set to: <emoji id={custom_emoji_id}>🗿</emoji>")
                    return
    if new_prefix_text.lower() == "none":
        await set_prefix_in_db(user_id, "None")
        await message.reply_text("Prefix removed.")
        return
    await set_prefix_in_db(user_id, new_prefix_text)
    await message.reply_text(f"Prefix set to: {new_prefix_text}")
