from pyrogram import Client, filters
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import pathlib
from time import perf_counter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Akeno.utils.helps import ModuleHelp

group_only = [ChatType.GROUP, ChatType.SUPERGROUP]
Akeno = Client.on_message
Akeno_chat_member_updated = Client.on_chat_member_updated()
script_path = pathlib.Path(__file__).parent.parent
modules_help = ModuleHelp()
scheduler_jobs = []
scheduler = AsyncIOScheduler()
bot_uptime = perf_counter()
