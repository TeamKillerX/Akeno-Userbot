#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2023 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import importlib
import logging
import sys
from contextlib import closing, suppress
from importlib import import_module

from pyrogram import idle
from pyrogram.errors import *
from uvloop import install

from Akeno import clients
from Akeno.plugins import ALL_MODULES
from Akeno.utils.database import db
from Akeno.utils.logger import LOGS

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
loop = asyncio.get_event_loop()

async def main():
    try:
        await db.connect()
        for module_name in ALL_MODULES:
            imported_module = import_module(f"Akeno.plugins.{module_name}")
        for cli in clients:
            try:
                await cli.start()
            except (
                SessionExpired,
                ApiIdInvalid,
                UserDeactivated,
                AuthKeyDuplicated
            ) as e:
                LOGS.info(f"Error {e}")
                continue
            except Exception as e:
                LOGS.info(f"Error {e}")
                continue
            ex = await cli.get_me()
            LOGS.info(f"Started {ex.first_name}")
            await cli.send_message("me", "Starting Akeno Userbot")
            try:
                await cli.join_chat("RendyProjects")
            except UserIsBlocked:
                LOGS.info("You have been blocked. Please support @xtdevs")
                sys.exit(1)
        await idle()
    except Exception as e:
        LOGS.info(f"Error in main: {e}")
    finally:
        for task in asyncio.all_tasks():
            task.cancel()
        LOGS.info("All tasks completed successfully!")

if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(3.0))
