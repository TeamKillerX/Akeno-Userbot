from pyrogram import Client, filters, idle, enums
from pyrogram.types import Chat, Message, InlineKeyboardButton, InlineKeyboardMarkup, ChatPrivileges, ChatMember
from pyrogram.enums.parse_mode import ParseMode
import logging
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
    ~filters.scheduled & filters.command(["antiarabic"], CMD_HANDLER) & filters.me & ~filters.forwarded
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
            await client.send_message(LOGS_CHANNEL, get_user_check)
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

randydev.run()
