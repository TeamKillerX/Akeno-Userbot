import os

from pyrogram import Client
from pyrogram.errors import PeerIdInvalid, UserIsBlocked
from pyrogram.raw.types import InputDocument, InputStickerSetItem
from pyrogram.types import Message

from Akeno.utils.convert import image_to_sticker, video_to_sticker
from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.sticker import *
from config import *


@Akeno(
    ~filters.scheduled
    & filters.command(["kang"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def kangSticker(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a sticker to kang it.")

    pro = await message.reply_text("__Kanging sticker...__")
    pack_id, pack_emoji = get_emoji_and_id(message)
    pack_type, is_animated, is_video, is_static, pack_limit = check_sticker_data(
        message.reply_to_message
    )
    if pack_type is None:
        return await pro.edit_text("Unsupported media type.")
    nickname = f"@{client.me.username}" if client.me.username else client.me.first_name
    pack_name = (
        await db.get_env(ENV_TEMPLATE.sticker_packname)
        or f"{nickname}'s Vol.{pack_id} ({pack_type.title()})"
    )
    pack_url_suffix = (
        f"Akeno{client.me.id}_vol{pack_id}_{pack_type}_by_{client.me.username}"
    )
    if message.reply_to_message.sticker:
        if is_static:
            file = await message.reply_to_message.download()
            status, path = await image_to_sticker(file)
            if not status:
                return await pro.edit_text(path)
        else:
            path = await message.reply_to_message.download()
    else:
        if is_video:
            await pro.edit_text("Converting to video sticker...")
            path, status = await video_to_sticker(message.reply_to_message)
            if not status:
                return await pro.edit_text(path)
        elif is_animated:
            await pro.edit_text("Converting to animated sticker...")
            path = await message.reply_to_message.download()
        else:
            await pro.edit_text("Converting to sticker...")
            file = await message.reply_to_message.download()
            status, path = await image_to_sticker(file)
            if not status:
                return await pro.edit_text(path)
    LOGGER_ID = await db.get_env(ENV_TEMPLATE.log_id)
    if not LOGGER_ID:
        LOGGER_ID = "me"
    sticker = await create_sticker(client, LOGGER_ID, path, pack_emoji)
    os.remove(path)
    try:
        while True:
            stickerset = await get_sticker_set(client, pack_url_suffix)
            if stickerset:
                if stickerset.set.count == pack_limit:
                    pack_id += 1
                    pack_name = (
                        await db.get_env(ENV_TEMPLATE.sticker_packname)
                        or f"{nickname}'s Vol.{pack_id} ({pack_type.title()})"
                    )
                    pack_url_suffix = f"Akeno{client.me.id}_vol{pack_id}_{pack_type}_by_{client.me.username}"
                    continue
                else:
                    await add_sticker(client, stickerset, sticker)
            else:
                await new_sticker_set(
                    client,
                    client.me.id,
                    pack_name,
                    pack_url_suffix,
                    [sticker],
                    is_animated,
                    is_video,
                )
            break
        return await pro.edit_text(
            f"**{pack_emoji} 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝗄𝖺𝗇𝗀𝖾𝖽 𝗍𝗈 [this pack](t.me/addstickers/{pack_url_suffix})**",
            disable_web_page_preview=True,
        )
    except Exception as e:
        return await message.reply_text(str(e))

@Akeno(
    ~filters.scheduled
    & filters.command(["packkang"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def packKang(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a sticker to kang whole pack!")
    pro = await message.reply_text("__Kanging sticker pack...__")
    pack_id = 1
    nickname = f"@{client.me.username}" if client.me.username else client.me.first_name
    packname = await input_user(message) or f"{nickname}'s Pack (Vol.{pack_id})"
    pack_url_suffix = f"Akeno{client.me.id}_pkvol{pack_id}_by_{client.me.username}"
    if not message.reply_to_message.sticker:
        return await pro.edit_text("Reply to a sticker to kang whole pack!")
    is_animated = message.reply_to_message.sticker.is_animated
    is_video = message.reply_to_message.sticker.is_video
    stickers = []
    replied_setname = message.reply_to_message.sticker.set_name
    replied_set = await get_sticker_set(client, replied_setname)
    if not replied_set:
        return await pro.edit_text("Reply to a sticker to kang whole pack!")
    for sticker in replied_set.documents:
        document = InputDocument(
            id=sticker.id,
            access_hash=sticker.access_hash,
            file_reference=sticker.file_reference,
        )
        stickers.append(InputStickerSetItem(document=document, emoji="🍀"))
    try:
        while True:
            stickerset = await get_sticker_set(client, pack_url_suffix)
            if stickerset:
                pack_id += 1
                pack_url_suffix = (
                    f"Akeno{client.me.id}_pkvol{pack_id}_by_{client.me.username}"
                )
                packname = (
                    await input_user(message) or f"{nickname}'s Pack (Vol.{pack_id})"
                )
                continue
            else:
                await new_sticker_set(
                    client,
                    client.me.id,
                    packname,
                    pack_url_suffix,
                    stickers,
                    is_animated,
                    is_video,
                )
                break
        return await pro.edit_text(
            f"**🍀 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖯𝖺𝖼𝗄 𝗄𝖺𝗇𝗀𝖾𝖽 𝗍𝗈 [this pack](t.me/addstickers/{pack_url_suffix})**",
            disable_web_page_preview=True,
        )
    except Exception as e:
        return await message.reply_text(str(e))

@Akeno(
    ~filters.scheduled
    & filters.command(["stickerinfo"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def stickerInfo(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("Reply to a sticker to get their info.")
    pro = await message.reply_text("__Fetching sticker info ...__")
    sticker = message.reply_to_message.sticker
    sticker_set = await get_sticker_set(client, sticker.set_name)
    if not sticker_set:
        return await pro.edit_text("This sticker is not part of a pack.")
    pack_emoji = []
    for emojis in sticker_set.packs:
        if emojis.emoticon not in pack_emoji:
            pack_emoji.append(emojis.emoticon)
    outStr = (
        f"**🍀 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖯𝖺𝖼𝗄 𝖨𝗇𝖿𝗈:**\n\n"
        f"**𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖨𝖣:** `{sticker.file_id}`\n"
        f"**Pack Name:** `{sticker_set.set.title}`\n"
        f"**Pack Short Name:** `{sticker_set.set.short_name}`\n"
        f"**𝖮𝖿𝖿𝗂𝖼𝗂𝖺𝗅:** {sticker_set.set.official}\n"
        f"**𝖤𝗆𝗈𝗃𝗂:** `{', '.join(pack_emoji)}`\n"
        f"**𝖣𝖺𝗍𝖾:** `{sticker_set.set.installed_date}`\n"
        f"**𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖲𝗂𝗓𝖾:** `{sticker_set.set.count}`\n"
    )
    await pro.edit_text(outStr, disable_web_page_preview=True)

@Akeno(
    ~filters.scheduled
    & filters.command(["rmsticker"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def removeSticker(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text(
            "Reply to a sticker to remove it from the pack."
        )
    await message.reply_text("__Removing sticker from pack...__")
    sticker = message.reply_to_message.sticker
    sticker_set = await get_sticker_set(client, sticker.set_name)
    if not sticker_set:
        return await message.reply_text("This sticker is not part of a pack.")
    try:
        await remove_sticker(client, sticker.file_id)
        await message.reply_text(
            f"**𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝗍𝗁𝖾 𝗌𝗍𝗂𝖼𝗄𝖾𝗋 𝖿𝗋𝗈𝗆 𝗉𝖺𝖼𝗄:** {sticker_set.set.title}",
        )
    except Exception as e:
        await message.reply_text(str(e))

module = modules_help.add_module("sticker", __file__)
module.add_command("kang", "Add the replied image/gif/video/sticker into your own sticker pack kang.")
module.add_command("packkang", "Add all the stickers in the replied pack into your own sticker pack.")
module.add_command("stickerinfo", "Get info about the replied sticker.")
module.add_command("rmsticker", "Remove the replied sticker from the pack.")
