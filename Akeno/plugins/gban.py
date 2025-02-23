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

# Credits Developer by @xtdevs
# NO NEED DATABASE USING API REST DB

import asyncio

from pyrogram import *
from pyrogram import Client, errors, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType
from pyrogram.errors import ChannelInvalid, FloodWait
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import *
from pyrogram.types import ChatPermissions, Message

from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.tools import get_ub_chats
from config import *


async def input_user(message: Message) -> str:
    """Get the input from the user"""
    if len(message.command) < 2:
        output = ""
    else:
        try:
            output = message.text.split(" ", 1)[1].strip() or ""
        except IndexError:
            output = ""
    return output

@Akeno(
    ~filters.scheduled & filters.command(["gban"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def globalban(client: Client, message: Message):
    is_banned = False
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await message.reply_text(
                "Reply to a user or pass a username/id to gban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await message.reply_text(f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await input_user(message) or "No reason provided."
    if user.is_self:
        is_banned = False
        return await message.reply_text("I can't gban myself.")
    if user.id == client.me.id:
        is_banned = False
        return await message.reply_text("I can't gban my auth user.")
    if user.id == 1191668125:
        is_banned = False
        return await message.reply_text("I can't gban my auth user.")
    success = 0
    failed = 0
    pro = await message.reply_text(f"Gban initiated on {user.mention}...")
    is_banned = True
    if is_banned:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [
                ChatType.CHANNEL,
                ChatType.GROUP,
                ChatType.SUPERGROUP,
            ]:
                try:
                    await dialog.chat.ban_member(user.id)
                    success += 1
                except FloodWait as e:
                    await pro.edit_text(
                        f"Gban initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                    )
                    await asyncio.sleep(e.x)
                    await dialog.chat.ban_member(user.id)
                    success += 1
                    await pro.edit_text(f"Gban initiated on {user.mention}...")
                except BaseException:
                    failed += 1
        messager = ""
        messager += f"\n\nSuccess: {success}\n"
        messager += f"Failed: {failed}\n"
        await pro.edit_text(messager)

module = modules_help.add_module("gban", __file__)
module.add_command("gban", "to global banned in group all.")
