# Ported From DarkCobra Originally By UNIBORG
# Ultroid - UserBot
# converter telethon to pyrogram by @xtdevs

from datetime import datetime as dt

import speedtest
from pyrogram import Client as ren
from pyrogram import *
from pyrogram.types import *
from speedtest import Speedtest

from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.prefixprem import command
from config import CMD_HANDLER

temxt = (
    "**Akeno Ubot Speedtest completed in {0} seconds.**\n\n" \
    "**Download:**  `{1}` \n" \
    "**Upload:**  `{2}` \n" \
    "**Ping:**  `{3} ms` \n" \
    "**Internet Provider:**  `{4} ({5})` \n"
)

def humanbytes(size: float) -> str:
    """ humanize size """
    if not size:
        return "0 B"
    power = 1024
    t_n = 0
    power_dict = {
        0: '',
        1: 'Ki',
        2: 'Mi',
        3: 'Gi',
        4: 'Ti',
        5: 'Pi',
        6: 'Ei',
        7: 'Zi',
        8: 'Yi'}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])  # pylint: disable=consider-using-f-string


def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "Kilobytes/s", 2: "Megabytes/s", 3: "Gigabytes/s", 4: "Terabytes/s"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

@Akeno(
    ~filters.scheduled
    & command(["speedtest"])
    & filters.me
    & ~filters.forwarded
)
async def speedtest_test(client: Client, message: Message):
    args = message.text.split()
    xx = await message.reply_text("`Calculating your Akeno's Server Speed ...`")
    start = dt.now()
    s = Speedtest()
    s.get_best_server()
    s.download()
    s.upload()  # dchehe
    end = dt.now()
    ms = (end - start).seconds
    response = s.results.dict()

    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")

    if args and args == "text":
        await xx.edit_text(temxt.format(
            ms,
            convert_from_bytes(download_speed),
            convert_from_bytes(upload_speed),
            ping_time,
            i_s_p,
            i_s_p_rating,
        ))
    else:
        try:
            speedtest_image = s.results.share()
            await client.send_photo(
                message.chat.id,
                photo=speedtest_image,  # heeehe
                caption="**SpeedTest** completed in {} seconds".format(ms),
                reply_to_message_id=message.id
            )
            await xx.delete()
        except Exception as exc:  # dc
            xx2 = temxt.format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                i_s_p,
                i_s_p_rating,
            )
            return await xx.edit_text(
                f"{xx2} \n**Exception:** `{exc}`"
            )

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.

@Akeno(
    ~filters.scheduled
    & command(["speedtest2"])
    & filters.me
    & ~filters.forwarded
)
async def speedtst_2(client: Client, message: Message):
    pro = await message.reply_text("`Running speed test . . .`")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        await pro.edit_text("`Performing download test . . .`")
        test.download()
        await pro.edit_text("`Performing upload test . . . .`")
        test.upload()
        try:
            test.results.share()
        except speedtest.ShareResultsConnectFailure:
            pass
        result = test.results.dict()
    except Exception as e:
        await pro.edit_text(str(e))
        return
    output = f"""**--Started at {result['timestamp']}--

Client:

ISP: `{result['client']['isp']}`
Country: `{result['client']['country']}`

Server:

Name: `{result['server']['name']}`
Country: `{result['server']['country']}, {result['server']['cc']}`
Sponsor: `{result['server']['sponsor']}`
Latency: `{result['server']['latency']}`

Ping: `{result['ping']}`
Sent: `{humanbytes(result['bytes_sent'])}`
Received: `{humanbytes(result['bytes_received'])}`
Download: `{humanbytes(result['download'] / 8)}/s`
Upload: `{humanbytes(result['upload'] / 8)}/s`**"""
    if result['share']:
        await client.send_photo(
            message.chat.id,
            photo=result['share'],
            caption=output
        )
    else:
        await client.send_message(
            message.chat.id,
            text=output
        )
    await pro.delete()
