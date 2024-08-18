from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram import *
from Akeno.utils.handler import *
from Akeno.utils.database import db
from Akeno.utils.logger import LOGS
from config import *

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

@Akeno(
    ~filters.scheduled & filters.command(["setvar"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def setvar(_, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            "**𝖦𝗂𝗏𝖾 𝗏𝖺𝗋𝗇𝖺𝗆𝖾 𝖺𝗇𝖽 𝗏𝖺𝗋-𝗏𝖺𝗅𝗎𝖾 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽!**"
        )
    input_str = (await input_user.input(message)).split(" ", 1)
    varname = input_str[0]
    varvalue = input_str[1]
    oldValue = await db.get_env(varname.upper())
    await db.set_env(varname.upper(), varvalue)
    await message.reply_text(
        f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾:** `{varname.upper()}` \n\n"
        f"**𝖮𝗅𝖽 𝖵𝖺𝗅𝗎𝖾:** `{oldValue}` \n\n"
        f"**𝖭𝖾𝗐 𝖵𝖺𝗅𝗎𝖾:** `{varvalue}`",
    )
