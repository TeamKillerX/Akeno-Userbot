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
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime as dt

from g4f.client import Client as Clients_g4f

from Akeno.utils.logger import LOGS

owner_base = f"""
Your name is Randy Dev. A kind and friendly AI assistant that answers in
a short and concise answer. Give short step-by-step reasoning if required.

- Powered by @xtdevs on telegram
Today is {dt.now():%A %d %B %Y %H:%M}
"""

async def chat_message(question):
    clients_x = Clients_g4f()
    response = clients_x.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": owner_base},
            {"role": "user", "content": question}
        ],
    )
    messager = response.choices[0].message.content
    return messager
