import random
import time
import asyncio
from Akeno.utils.images import generate_alive_image
from Akeno.utils.handler import *
from config import *

@Akeno(filters.command("alive", CMD_HANDLER), & filters.me)
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
                message.from_user.first_name, user_pfp, del_path, Config.FONT_PATH
            )
        ]
    else:
        img = img.split(" ")
    img = random.choice(img)
    uptime = readable_time(time.time() - START_TIME)
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
