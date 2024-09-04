#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2024 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os

from pyrogram import Client, enums, filters, idle
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Chat, ChatMember, ChatPrivileges, Message

from Akeno.utils.database import db
from Akeno.utils.handler import *
from config import CMD_HANDLER

ANTINSFW_GROUPS = 12

async def can_delete(client: Client, bot_id: int) -> bool:
    member = await client.get_member(bot_id)
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return True
    else:
        return False

def check_anti_nsfw(media) -> bool:
    url = "https://akeno.randydev.my.id/akeno/anti-nsfw"
    with open(media, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        results = response.json()
        return results["randydev"]["results"]["result"]["content"].get("isNsfw", False)
    return False

@Akeno(
    ~filters.scheduled & filters.command(["antinsfw"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def antinsfw_setting(client: Client, message: Message):
    args = message.text.lower().split()[1:]
    chat = message.chat
    if chat.type != "private":
        if args:
            if args[0] in ("yes", "on", "true"):
                await db.set_chat_setting_antinsfw(chat.id, True)
                await message.reply_text("Turned on AntiNFSW! Messages sent by any non-admin that contain anti nsfw media will be deleted.")

            elif args[0] in ("no", "off", "false"):
                await db.set_chat_setting_antinsfw(chat.id, False)
                await message.reply_text("Turned off AntiNFSW! Messages containing anti nsfw media won't be deleted.")
        else:
            reply_text = f"AntiNsfw Mode: {'On' if await db.chat_antinsfw(chat.id) else 'Off'}"
            await message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

@Akeno(
    filters.group
    & ~filters.private
    & ~filters.bot
    & ~filters.service,
    group=ANTINSFW_GROUPS
)
async def antinsfw_filter(client: Client, message: Message):
    chat = message.chat
    user = message.from_user
    if not await db.chat_antinsfw(chat.id):
        return
    if not user or user.id == 777000:
        return
    if not message.photo:
        return
    me = await client.get_me()
    if message.photo:
        file_id = message.photo.file_id
    media = await client.download_media(file_id)
    if check_anti_nsfw(media):
        if await can_delete(chat, me.id):
            return await message.delete()
            os.remove(media)

module = modules_help.add_module("antinsfw", __file__)
module.add_command("antinsfw", "to anti nsfw auto delete messages")
