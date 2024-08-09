#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2023 (c) Randy W @xtdevs, @xtsea
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

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import errors, filters
from pyrogram import *
from pyrogram.types import *
from pyrogram.enums import ChatType, ChatMemberStatus as CMS
from pyrogram.errors import FloodWait
from pyrogram.errors import ChannelInvalid
from pyrogram.types import ChatPermissions, Message
from pyrogram.raw.functions.messages import DeleteHistory
from Akeno.utils.tools import get_ub_chats
from Akeno.utils.help import add_command_help
from Akeno.utils.spamwatch import auto_post_gban, auto_check_gban
from Akeno.utils.handler import Akeno, Akeno_chat_member_updated
from Akeno.utils.admin import extract_user_and_reason
from config import FEDBAN_API_KEY

api_key = FEDBAN_API_KEY

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
    ~filters.scheduled & command(["gban"]) & filters.me & ~filters.forwarded
)
async def globalban(client: Client, message: Message):
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
        return await message.reply_text("I can't gban myself.")
    if user.id == client.me.id:
        return await message.reply_text("I can't gban my auth user.")
    success = 0
    failed = 0
    pro = await message.reply_text(f"Gban initiated on {user.mention}...")
    response = await auto_post_gban(user.id, reason)
    if response == True:
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
        messager += response["randydev"].get("message")
        messager += f"\n\nSuccess: {success}\n"
        messager += f"Failed: {failed}\n"
        await pro.edit_text(messager)

@Akeno_chat_member_updated
async def globalbanwatcher(_, u: ChatMemberUpdated):
    if not (member.new_chat_member and member.new_chat_member.status not in {CMS.BANNED, CMS.LEFT, CMS.RESTRICTED} and not member.old_chat_member):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    response = await auto_check_gban(user.id)
    if response[0] == True:
        watchertext = f"**𝖦𝖻𝖺𝗇𝗇𝖾𝖽 𝖴𝗌𝖾𝗋 𝗃𝗈𝗂𝗇𝖾𝖽 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍! \n\n𝖦𝖻𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** __{response[1]}__\n\n"
        try:
            await _.ban_chat_member(u.chat.id, user.id)
            watchertext += f"**𝖲𝗈𝗋𝗋𝗒 𝖨 𝖼𝖺𝗇'𝗍 𝗌𝖾𝖾 𝗒𝗈𝗎 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍!**"
        except BaseException:
            watchertext += f"Reported to @admins"
        await _.send_message(u.chat.id, watchertext)
    return

@Akeno(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def global_spammer(client: Client, message: Message):
    if not message or not message.from_user:
        return
    user_id = message.from_user.id
    response = await auto_check_gban(user_id)
    if response[0] == True:
        if message.photo:
            await message.delete()
        elif message.video:
            await message.delete()
        else:
            await client.block_user(user_id)
    message.continue_propagation()
