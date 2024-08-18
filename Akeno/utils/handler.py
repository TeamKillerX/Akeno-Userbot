import pathlib
from time import perf_counter

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from Akeno.utils.helps import ModuleHelp

group_only = [ChatType.GROUP, ChatType.SUPERGROUP]
Akeno = Client.on_message
Akeno_chat_member_updated = Client.on_chat_member_updated()
script_path = pathlib.Path(__file__).parent.parent
modules_help = ModuleHelp()
scheduler_jobs = []
scheduler = AsyncIOScheduler()
bot_uptime = perf_counter()

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
