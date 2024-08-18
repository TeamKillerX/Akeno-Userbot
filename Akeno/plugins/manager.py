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
    input_str = (await input_user(message)).split(" ", 1)
    varname = input_str[0]
    varvalue = input_str[1]
    oldValue = await db.get_env(varname.upper())
    await db.set_env(varname.upper(), varvalue)
    await message.reply_text(
        f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾:** `{varname.upper()}` \n\n"
        f"**𝖮𝗅𝖽 𝖵𝖺𝗅𝗎𝖾:** `{oldValue}` \n\n"
        f"**𝖭𝖾𝗐 𝖵𝖺𝗅𝗎𝖾:** `{varvalue}`",
    )

@Akeno(
    ~filters.scheduled & filters.command(["delvar"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def delvar(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**𝖦𝗂𝗏𝖾 𝗏𝖺𝗋𝗇𝖺𝗆𝖾 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽!**")
    varname = message.command[1]
    if varname.upper() in os_configs:
        return await message.reply_text(
            "You can't delete this var for security reasons."
        )
    if await db.is_env(varname.upper()):
        await db.rm_env(varname.upper())
        await message.reply_text(
            f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾** `{varname.upper()}` **𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**"
        )
        return
    await message.reply_text("**𝖭𝗈 𝗌𝗎𝖼𝗁 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾!**")

@Akeno(
    ~filters.scheduled & filters.command(["getvar"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def getvar(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give a varname to fetch value.")
    varname = message.command[1]
    if varname.upper() in os_configs:
        value = await db.get_env(varname.upper())
    if isinstance(value, str):
        await message.reply_text(
            f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖭𝖺𝗆𝖾:** `{varname.upper()}`\n**𝖵𝖺𝗅𝗎𝖾:** `{value}`",
        )
    elif value is None:
        await message.reply_text(f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾 {varname} 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌!**")

@Akeno(
    ~filters.scheduled & filters.command(["getallvar", "getallvars"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def getallvar(_, message: Message):
    text = "**📃 𝖫𝗂𝗌𝗍 𝗈𝖿 𝖺𝗅𝗅 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖺𝗋𝖾:**\n\n"
    for env in all_env:
        text += f"`{env}`\n"
    for config in os_configs:
        text += f"`{config}`\n"
    await message.reply_text(text)
