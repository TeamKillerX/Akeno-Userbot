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
import bs4
import requests
from pyrogram import Client
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message

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

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@Akeno(
    ~filters.scheduled
    & filters.command(["eval", "ev"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def runeval(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("No python code provided!")

    reply_to = message.reply_to_message or message

    code = await input_user(message)
    pro = await message.reply_texf("`running...`")

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(code, client, message)
    except Exception:
        exc = traceback.format_exc()

    evaluation = ""
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    heading = f"**𝖤𝗏𝖺𝗅:**\n```python\n{code}```\n\n"
    output = f"**𝖮𝗎𝗍𝗉𝗎𝗍:**\n`{evaluation.strip()}`"
    final_output = heading + output
    try:
        await reply_to.reply_text(final_output, disable_web_page_preview=True)
    except MessageTooLong:
        with io.BytesIO(str.encode(output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to.reply_document(out_file, caption=heading)
    await pro.delete()
