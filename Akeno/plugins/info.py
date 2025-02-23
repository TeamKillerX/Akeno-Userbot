from asyncio import gather
from os import remove

from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram import filters
from pyrogram.types import *
from pyrogram.types import Message

from Akeno.plugins.admin import extract_user
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.prefixprem import command
from config import CMD_HANDLER


@Akeno(
    ~filters.scheduled
    & command(["info"])
    & filters.me
    & ~filters.forwarded
)
async def who_is(client: Client, message: Message):
    user_id = await extract_user(message)
    ex = await message.edit_text("`Processing . . .`")
    if not user_id:
        return await ex.edit(
            "**Provide userid/username/reply to get that user's info.**"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = user.first_name or "-"
        last_name = user.last_name or "-"
        fullname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        user_details = (await client.get_chat(user.id)).bio or "-"
        status = user.status.name
        dc_id = user.dc_id or "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>USER INFORMATION:</b>

🆔 <b>User ID:</b> <code>{user.id}</code>
👤 <b>First Name:</b> {first_name}
🗣️ <b>Last Name:</b> {last_name}
🌐 <b>Username:</b> {username}
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🤖 <b>Is Bot:</b> <code>{user.is_bot}</code>
🚷 <b>Is Scam:</b> <code>{user.is_scam}</code>
🚫 <b>Restricted:</b> <code>{user.is_restricted}</code>
✅ <b>Verified:</b> <code>{user.is_verified}</code>
⭐ <b>Premium:</b> <code>{user.is_premium}</code>
📝 <b>User Bio:</b> {bio}

👀 <b>Same groups seen:</b> {len(common)}
👁️ <b>Last Seen:</b> <code>{status}</code>
🔗 <b>User permanent link:</b> <a href='tg://user?id={user.id}'>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                ex.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await ex.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        LOGS.error(str(e))
        return await ex.edit(f"**INFO:** `{e}`")

module = modules_help.add_module("info", __file__)
module.add_command("info", "to info view users.")
