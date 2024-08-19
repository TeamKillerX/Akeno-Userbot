import asyncio
from asyncio import *
from random import *

from pyrogram import *
from pyrogram.types import *

from Akeno.utils.database import db
from Akeno.utils.handler import *
from config import *


@Akeno(
    ~filters.scheduled
    & filters.command(["asupan"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def asupan_channel(client: Client, message: Message):
    pro = await message.reply_text("`Processing....`")
    user_id = message.from_user.id
    get_username = await db.get_env(ENV_TEMPLATE.asupan_username)
    if not get_username:
        return await pro.edit_text("required `.setvar ASUPAN_USERNAME`")
    if not get_username.startswith("@"):
        return await pro.edit_text("Invalid username")
    custom_emoji = "<emoji id=5328317370647715629>✅</emoji>"
    prem = await client.get_users("me")
    if prem.is_premium:
        caption = f"{custom_emoji}**Uploaded by** {client.me.mention}"
    else:
        caption = f"**Uploaded by** {client.me.mention}"
    await asyncio.gather(
        pro.delete(),
        client.send_video(
            message.chat.id,
            choice(
                [
                    asupan.video.file_id
                    async for asupan in client.search_messages(
                        get_username,
                        filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            caption=caption,
            reply_to_message_id=message.id
        ),
    )

module = modules_help.add_module("asupan", __file__)
module.add_command("asupan", "to asupan random video")
