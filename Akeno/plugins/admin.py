# Copyright (C) 2020-2023 TeamKillerX <https://github.com/TeamKillerX>
#
# This file is part of TeamKillerX project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

import asyncio
import time
from time import time as waktu

from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *

from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.prefixprem import command
from config import CMD_HANDLER

admins_in_chat = {}

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": waktu(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


@Akeno(
    ~filters.scheduled & command(["ban", "dban", "hban"]) & filters.me & ~filters.forwarded
)
async def member_ban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit_text("I don't have enough permissions")
    if not user_id:
        return await rd.edit_text("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit_text("I can't ban myself.")
    if user_id == 1191668125:
        return await rd.edit_text("I can't ban my developer!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit_text("I can't ban an admin, You know the rules, so do i.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    elif message.command[0][0] == "h":
        await client.delete_user_history(message.chat.id, user_id)
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await rd.edit_text(msg)


@Akeno(
    ~filters.scheduled & command(["unban"]) & filters.me & ~filters.forwarded
)
async def member_unban_user(client: Client, message: Message):
    reply = message.reply_to_message
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit_text("I don't have enough permissions")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await rd.edit_text("You cannot unban a channel")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await rd.edit_text(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await rd.edit_text(f"Unbanned! {umention}")


@Akeno(
    ~filters.scheduled & command(["pin", "unpin"]) & filters.me & ~filters.forwarded
)
async def pin_message(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to a message to pin/unpin it.")
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await rd.edit_text("I don't have enough permissions")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await rd.edit_text(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await rd.edit_text(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )

@Akeno(
    ~filters.scheduled & command(["mute", "dmute", "hmute"]) & filters.me & ~filters.forwarded
)
async def mute_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit_text("I don't have enough permissions")
    if not user_id:
        return await rd.edit_text("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit_text("I can't mute myself.")
    if user_id == 1191668125:
        return await rd.edit("I can't mute my developer!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit_text("I can't mute an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    elif message.command[0][0] == "h":
        await client.delete_user_history(message.chat.id, user_id)
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await rd.edit_text(msg)

@Akeno(
    ~filters.scheduled & command(["unmute"]) & filters.me & ~filters.forwarded
)
async def unmute_user(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit_text("I don't have enough permissions")
    if not user_id:
        return await rd.edit_text("I can't find that user.")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await rd.edit_text(f"Unmuted! {umention}")

@Akeno(
    ~filters.scheduled & command(["kick", "dkick", "hkick"]) & filters.me & ~filters.forwarded
)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit_text("I don't have enough permissions")
    if not user_id:
        return await rd.edit_text("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit_text("I can't kick myself.")
    if user_id == 1191668125:
        return await rd.edit_text("I can't kick my developer.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit_text("I can't kick an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    elif message.command[0][0] == "h":
        await client.delete_user_history(message.chat.id, user_id)
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await rd.edit_text(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await rd.edit_text("**Maaf Anda Bukan admin**")

@Akeno(
    ~filters.scheduled & command(["promote", "fullpromote"]) & filters.me & ~filters.forwarded
)
async def promotte_user(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit_text("I can't find that user.")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await rd.edit_text("I don't have enough permissions")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await rd.edit_text(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await rd.edit_text(f"Promoted! {umention}")

@Akeno(
    ~filters.scheduled & command(["demote"]) & filters.me & ~filters.forwarded
)
async def demote_user(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit_text("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit_text("I can't demote myself.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await rd.edit_text(f"Demoted! {umention}")

module = modules_help.add_module("admin", __file__)
module.add_command("ban", "Ban someone.")
module.add_command("dban", "dban a user deleting the replied to message")
module.add_command("hban", "hban a user deleting all the replied to message")
module.add_command("kick", "kick out someone from your group")
module.add_command("dkick", "dkick a user deleting the replied to message")
module.add_command("hkick", "hkick a user deleting all the replied to message")
module.add_command("promote", "Promote someonen")
module.add_command("demote", "Demote someone")
module.add_command("mute", "Mute someone")
module.add_command("dmute", "dmute a user deleting the replied to message")
module.add_command("hmute", "hmute a user deleting all the replied to message")
module.add_command("pin", "to pin any message.")
module.add_command("unpin", "To unpin any message")
module.add_command("setgpic", "To set an group profile pic.")
