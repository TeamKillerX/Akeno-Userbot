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
        if message.from_user.photo:
            user_pfp = await client.download_media(message.from_user.photo.big_file_id)
            del_path = True
        else:
            user_pfp = "resources/images/logo.png"
            del_path = False
        img = [
            generate_alive_image(
                message.from_user.first_name,
                user_pfp,
                del_path,
                FONT_PATH
            )
        ]
    else:
        img = img.split(" ")
    img = random.choice(img)
    uptime = get_readable_time(time.time() - StartTime)
    caption = await alive_template(client.me.first_name, uptime)
    if img.endswith(".mp4"):
        await message.reply_video(img, caption=caption)
    else:
        await message.reply_photo(img, caption=caption)
    await pro.delete()
    try:
        os.remove(img)
    except:
        pass
