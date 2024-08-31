import os
import time

import requests
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from Akeno.utils.database import db
from Akeno.utils.driver import YoutubeDriver
from Akeno.utils.formatter import secs_to_mins
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.scripts import progress
from config import *


@Akeno(
    ~filters.scheduled
    & filters.command(["ytsa"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def youtube_search_audio(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube search to download audio."
        )
    query = await input_user(message)
    results = YoutubeSearch(query, max_results=5).to_dict()
    watch = results[0]["url_suffix"]
    url_suffix = watch.split("/")[1]
    okk = f"https://youtube.com/{url_suffix}"
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(okk)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 __Downloading audio ...__")
    try:
        with YoutubeDL(YoutubeDriver.song_options()) as ytdl:
            yt_data = ytdl.extract_info(url, False)
            yt_file = ytdl.prepare_filename(yt_data)
            ytdl.process_info(yt_data)
        upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...** \n\n**𝖳𝗂𝗍𝗅𝖾:** `{yt_data['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{yt_data['channel']}`"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_audio(
            f"{yt_file}.mp3",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            performer="[Akeno UB]",
            title=yt_data["title"],
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Audio not Downloaded:** `{e}`")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp3")
    except:
        pass

@Akeno(
    ~filters.scheduled
    & filters.command(["yta"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def youtube_audio(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube link to download audio."
        )
    query = await input_user(message)
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(query)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 __Downloading audio ...__")
    try:
        with YoutubeDL(YoutubeDriver.song_options()) as ytdl:
            yt_data = ytdl.extract_info(url, False)
            yt_file = ytdl.prepare_filename(yt_data)
            ytdl.process_info(yt_data)
        upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...** \n\n**𝖳𝗂𝗍𝗅𝖾:** `{yt_data['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{yt_data['channel']}`"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_audio(
            f"{yt_file}.mp3",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            performer="[Akeno UB]",
            title=yt_data["title"],
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Audio not Downloaded:** `{e}`")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp3")
    except:
        pass

@Akeno(
    ~filters.scheduled
    & filters.command(["ytva"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def ytvideo_search(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube search to download video."
        )
    query = await input_user(message)
    results = YoutubeSearch(query, max_results=5).to_dict()
    watch = results[0]["url_suffix"]
    url_suffix = watch.split("/")[1]
    okk = f"https://youtube.com/{url_suffix}"
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(okk)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 __Downloading video ...__")
    try:
        with YoutubeDL(YoutubeDriver.video_options()) as ytdl:
            yt_data = ytdl.extract_info(url, True)
            yt_file = yt_data["id"]

        upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...** \n\n**𝖳𝗂𝗍𝗅𝖾:** `{yt_data['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{yt_data['channel']}`"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_video(
            f"{yt_file}.mp4",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Video not Downloaded:** `{e}`")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp4")
    except:
        pass

@Akeno(
    ~filters.scheduled
    & filters.command(["ytv"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def ytvideo(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube link to download video."
        )
    query = await input_user(message)
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(query)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 __Downloading video ...__")
    try:
        with YoutubeDL(YoutubeDriver.video_options()) as ytdl:
            yt_data = ytdl.extract_info(url, True)
            yt_file = yt_data["id"]

        upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...** \n\n**𝖳𝗂𝗍𝗅𝖾:** `{yt_data['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{yt_data['channel']}`"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_video(
            f"{yt_file}.mp4",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Video not Downloaded:** `{e}`")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp4")
    except:
        pass

@Akeno(
    ~filters.scheduled
    & filters.command(["ytlink"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def ytlink(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give something to search on youtube.")
    query = await input_user(message)
    pro = await message.reply_text("Searching ...")
    try:
        results = YoutubeDriver(query, 7).to_dict()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Error:** `{e}`")
    if not results:
        return await pro.edit_text("No results found.")
    text = f"**🔎 𝖳𝗈𝗍𝖺𝗅 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 𝖥𝗈𝗎𝗇𝖽:** `{len(results)}`\n\n"
    for result in results:
        text += f"**𝖳𝗂𝗍𝗅𝖾:** `{result['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{result['channel']}`\n**𝖵𝗂𝖾𝗐𝗌:** `{result['views']}`\n**𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{result['duration']}`\n**𝖫𝗂𝗇𝗄:** `https://youtube.com{result['url_suffix']}`\n\n"
    await pro.edit_text(text, disable_web_page_preview=True)

module = modules_help.add_module("youtube", __file__)
module.add_command("yta", "Download the youtube link video in .mp3 format!.")
module.add_command("ytv", "Download the youtube link video in .mp3 format!.")
module.add_command("ytsa", "Download the youtube search video in .mp3 format!.")
module.add_command("ytva", "Download the youtube search video in .mp4 format!")
module.add_command("ytlink", "Search for a video on youtube")
