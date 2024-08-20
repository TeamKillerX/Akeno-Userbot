import asyncio
import os

from pyrogram.types import Message

from Akeno.utils.driver import Driver
from Akeno.utils.handler import *
from config import *


@Akeno(
    ~filters.scheduled
    & filters.command(["carbon"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def carbon(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give me some code to make carbon.")
    code = await input_user(message)
    pro = await message.reply_text("**[ 50% ]** __Making carbon...__")
    driver, resp = Driver.get()
    if not driver:
        return await pro.edit_text(resp)
    await pro.edit_text("**[ 75% ]** __Making carbon...__")
    image = await Driver.generate_carbon(driver, code)
    await asyncio.sleep(4)
    await pro.edit_text("**[ 100% ]** __Uploading carbon...__")
    Driver.close(driver)
    await message.reply_photo(image, caption=f"**𝖢𝖺𝗋𝖻𝗈𝗇𝖾𝖽:**\n`{code}`")
    await pro.delete()
    os.remove(image)

@Akeno(
    ~filters.scheduled
    & filters.command(["karbon"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def karbon(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give me some code to make karbon.")
    code = await input_user(message)
    pro = await message.reply_text("**[ 50% ]** __Making karbon...__")
    driver, resp = Driver.get()
    if not driver:
        return await pro.edit_text(resp)
    await pro.edit_text("**[ 75% ]** __Making karbon...__")
    image = await Driver.generate_carbon(driver, code, True)
    await asyncio.sleep(4)
    await pro.edit_text("**[ 100% ]** __Uploading karbon...__")
    Driver.close(driver)
    await message.reply_photo(image, caption=f"**𝖢𝖺𝗋𝖻𝗈𝗇𝖾𝖽:**\n`{code}`")
    await pro.delete()
    os.remove(image)

module = modules_help.add_module("carbon", __file__)
module.add_command("carbon", "Makes carbon of given code snippet.")
module.add_command("karbon", "Makes carbon of given code snippet.")
