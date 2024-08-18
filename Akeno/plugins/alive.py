import asyncio
import os
import random
import time

from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *

from Akeno import StartTime, __version__
from Akeno.plugins.ping import get_readable_time
from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.images import generate_alive_image
from config import *

FONT_PATH = "resources/fonts/Montserrat.ttf"

ALIVE_TEMPLATES = [
    (
        "•────────────────•\n"
        "•       Aᴋᴇɴᴏ ɪs ᴀʟɪᴠᴇ        •\n"
        "╭────────────────•\n"
        "╰➢ ᴏᴡɴᴇʀ » {owner}\n"
        "╰➢ ᴘʏʀᴏɢʀᴀᴍ » {pyrogram}\n"
        "╰➢ ᴘʏᴛʜᴏɴ » {python}\n"
        "╰➢ ᴜᴘᴛɪᴍᴇ » {uptime}\n"
        "╰────────────────•\n"
        "𝖡𝗒 © @xtdevs\n"
        "•────────────────•\n"
    ),
]

async def alive_template(owner: str, uptime: str) -> str:
    template = await db.get_env(ENV_TEMPLATE.alive_template)
    if template:
        message = template
    else:
        message = random.choice(ALIVE_TEMPLATES)
    return message.format(
        owner=owner,
        pyrogram=__version__["pyrogram"],
        python=__version__["python"],
        uptime=uptime,
    )

@Akeno(
    ~filters.scheduled
    & filters.command(["alive"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def alive(client: Client, message: Message):
    pro = await message.reply_text("Processing ...")
    img = await db.get_env(ENV_TEMPLATE.alive_pic)
    if not img:
        img = "https://telegra.ph/file/316e8e52a723e06d59bbf.jpg"
    uptime = get_readable_time(time.time() - StartTime)
    caption = await alive_template(client.me.first_name, uptime)
    if img.endswith(".mp4"):
        await message.reply_video(img, caption=caption)
    else:
        await message.reply_photo(img, caption=caption)
    await pro.delete()
    if os.path.exists(img):
        try:
            os.remove(img)
        except:
            pass

module = modules_help.add_module("alive", __file__)
module.add_command("alive", "Get the alive message of the bot.")
