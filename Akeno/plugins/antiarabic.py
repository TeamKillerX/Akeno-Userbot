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

from pyrogram import Client, enums, filters, idle
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Chat, ChatMember, ChatPrivileges, Message

from Akeno.utils.database import db
from Akeno.utils.handler import *
from config import CMD_HANDLER

ANTIARABIC_GROUPS = 12

async def can_delete(client: Client, bot_id: int) -> bool:
    member = await client.get_member(bot_id)
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return True
    else:
        return False

def extract_text(message: Message) -> str:
    return (
        message.text
        or message.caption
        or (message.sticker.emoji if message.sticker else None)
    )

@Akeno(
    ~filters.scheduled & filters.command(["antiarab"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def antiarabic_setting(client: Client, message: Message):
    args = message.text.lower().split()[1:]
    chat = message.chat
    if chat.type != "private":
        if args:
            if args[0] in ("yes", "on", "true"):
                await db.set_chat_setting(chat.id, True)
                await message.reply_text("Turned on AntiArabic! Messages sent by any non-admin that contain Arabic text will be deleted.")

            elif args[0] in ("no", "off", "false"):
                await db.set_chat_setting(chat.id, False)
                await message.reply_text("Turned off AntiArabic! Messages containing Arabic text won't be deleted.")
        else:
            reply_text = f"AntiArabic Mode: {'On' if await db.chat_antiarabic(chat.id) else 'Off'}"
            await message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

@Akeno(
    filters.group
    & ~filters.private
    & ~filters.bot
    & ~filters.service,
    group=ANTIARABIC_GROUPS
)
async def antiarabic_filter(client: Client, message: Message):
    chat = message.chat
    to_match = extract_text(message)
    user = message.from_user
    if not await db.chat_antiarabic(chat.id):
        return
    if not user or user.id == 777000:
        return
    if not to_match:
        return
    me = await client.get_me()
    for c in to_match:
        if ('\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F'
                or '\u08A0' <= c <= '\u08FF' or '\uFB50' <= c <= '\uFDFF'
                or '\uFE70' <= c <= '\uFEFF'
                or '\U00010E60' <= c <= '\U00010E7F'
                or '\U0001EE00' <= c <= '\U0001EEFF'):
            if await can_delete(chat, me.id):
                return await message.delete()

module = modules_help.add_module("antiarabic", __file__)
module.add_command("antiarab", "to antarabic auto delete messages")
