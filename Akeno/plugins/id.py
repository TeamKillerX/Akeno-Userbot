import asyncio
import os
import random
import time

from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import Message

from Akeno.utils.handler import *
from config import *


@Akeno(
    ~filters.scheduled
    & filters.command(["id"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None
    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`"
            file_id += "**File Type**: `audio`"
        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`"
            file_id += f"**File Type**: `{rep.document.mime_type}`"
        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`"
            file_id += "**File Type**: `photo`"
        elif rep.sticker:
            file_id = f"**Sicker ID**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set**: `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji**: `{rep.sticker.emoji}`\n"
                file_id += f"**Animated Sticker**: `{rep.sticker.is_animated if rep.sticker else False}`\n"
                file_id += f"**Video Sticker**: `{rep.sticker.is_video if rep.sticker else False}`\n"
                file_id += f"**Premium Sticker**: `{rep.sticker.is_premium if rep.sticker else False}`\n"
            else:
                file_id += "**Sticker Set**: __None__\n"
                file_id += "**Sticker Emoji**: __None__"
        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n"
            file_id += "**File Type**: `video`"
        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `GIF`"
        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n"
            file_id += "**File Type**: `Voice Note`"
        elif rep.video_note:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `Video Note`"
        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.location.latitude}`"
        elif rep.venue:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.venue.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address**:\n"
            file_id += f"**title**: `{rep.venue.title}`\n"
            file_id += f"**detailed**: `{rep.venue.address}`\n\n"
        elif rep.from_user:
            user_id = rep.from_user.id
    if user_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        elif rep.forward_from_chat:
            user_detail = (
                f"**Forwarded Channel ID**: `{message.reply_to_message.forward_from_chat.id}`\n"
                f"**Forwarded Channel Title**: `{message.reply_to_message.forward_from_chat.title}`\n"
                f"**Forwarded Channel Username**: `@{message.reply_to_message.forward_from_chat.username if message.reply_to_message.forward_from_chat else None}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`"
        await message.reply_text(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        elif rep.sender_chat:
            user_detail = (
                f"**Sender Chat ID**: `{message.reply_to_message.sender_chat.id if message.reply_to_message.sender_chat else None}`\n"
                f"**Sender Chat Title**: `{message.reply_to_message.sender_chat.title if message.reply_to_message.sender_chat else None}`\n"
                f"**Sender Chat Username**: `@{message.reply_to_message.sender_chat.username if message.reply_to_message.sender_chat else None}`\n"
            )
        else:
            user_detail = (
                f"**User ID**: `{message.reply_to_message.from_user.id if message.reply_to_message.from_user else None}`\n"
            )
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        try:
            await message.reply_text(user_detail)
        except ChannelInvalid:
            await message.reply_text("Channel Invalid")
        except Exception as e:
            await message.reply_text(f"Error: {e}")
    else:
        await message.reply_text(f"**Chat ID**: `{message.chat.id}`")
