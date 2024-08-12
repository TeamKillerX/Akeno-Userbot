from pyrogram import Client, filters
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

group_only = [ChatType.GROUP, ChatType.SUPERGROUP]
Akeno = Client.on_message
Akeno_chat_member_updated = Client.on_chat_member_updated()
