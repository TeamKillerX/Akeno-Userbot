# Copyright (C) 2020-2024 TeamKillerX <https://github.com/TeamKillerX>
#
# This file is part of TeamKillerX project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

import re
from typing import List, Union

from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.filters import Filter, create
from pyrogram.types import Message

from Akeno.utils.base_sqlite import get_prefix

def command(commands: Union[str, List[str]], case_sensitive: bool = False):
    command_re = re.compile(
        r"([\"'])(.*?)(?<!\\)\1|(\S+)",
        flags=re.UNICODE,
    )

    async def func(flt, client: Client, message: Message):
        username = client.me.username or ""
        user_id = client.me.id if client.me else 0
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        stored_prefix = await get_prefix(user_id)
        if stored_prefix is None:
            stored_prefix = "."

        if stored_prefix == "None":
            without_prefix = text.strip()
            return await process_command(flt, client, message, without_prefix, command_re, username)

        if message.entities:
            for entity in message.entities:
                if entity.type == MessageEntityType.CUSTOM_EMOJI and str(entity.custom_emoji_id) == stored_prefix:
                    without_prefix = text[entity.length:].strip()
                    return await process_command(flt, client, message, without_prefix, command_re, username)

        if text.startswith(stored_prefix):
            without_prefix = text[len(stored_prefix.encode("utf-16-le")) // 2:].strip()
            return await process_command(flt, client, message, without_prefix, command_re, username)
    
        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    return create(func, "CommandFilter", commands=commands, case_sensitive=case_sensitive)

async def process_command(flt, client: Client, message: Message, without_prefix: str, command_re, username: str):
    """Helper function to process command after prefix (if any) is removed."""
    for cmd in flt.commands:
        if re.match(
            f"^(?:{cmd}(?:@?{username})?)(?:\s|$)",
            without_prefix,
            flags=0 if flt.case_sensitive else re.IGNORECASE,
        ):
            without_command = re.sub(
                f"{cmd}(?:@?{username})?\s?",
                "",
                without_prefix,
                count=1,
                flags=0 if flt.case_sensitive else re.IGNORECASE,
            )
            message.command = [cmd] + [
                re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                for m in command_re.finditer(without_command)
            ]
            return True
    return False
