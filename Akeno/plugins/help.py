from pyrogram import *
from pyrogram.types import *

from Akeno.utils.handler import *
from Akeno.utils.helps import *
from config import *


@Akeno(~filters.scheduled & filters.command(["help", "h"], CMD_HANDLER) & filters.me & ~filters.forwarded)
async def help_cmd(_, message: Message):
    args, _ = get_args(message)
    try:
        if not args:
            msg_edited = False

            for text in modules_help.help():
                if msg_edited:
                    await message.reply(text, disable_web_page_preview=True)
                else:
                    await message.edit(text, disable_web_page_preview=True)
                    msg_edited = True
        elif args[0] in modules_help.modules:
            await message.edit(modules_help.module_help(args[0]), disable_web_page_preview=True)
        else:
            await message.edit(modules_help.command_help(args[0]), disable_web_page_preview=True)
    except ValueError as e:
        await message.edit(e)

module = modules_help.add_module("help", __file__)
module.add_command("help", "Get common/module/command help.")
