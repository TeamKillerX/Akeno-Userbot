import asyncio
from json import tool
from Akeno.utils.handler import *
from Akeno.utils.database import db

from pyrogram import Client, filters, enums
from pyrogram.types import Message
import cohere
from config import cohere_key

co = cohere.Client(cohere_key)

@Akeno(filters.command("cohere", CMD_HANDLER) & filters.me)
async def cohere(c: Client, message: Message):
    try:
        user_id = message.from_user.id
        chat_history = db._get_cohere_chat_from_db(user_id)
        if len(message.command) > 1:
            prompt = message.text.split(maxsplit=1)[1]
        elif message.reply_to_message:
            prompt = message.reply_to_message.text
        else:
            await message.edit_text(
                f"<b>Usage: </b><code>{prefix}cohere [prompt/reply to message]</code>"
            )
            return
        chat_history.append({"role": "USER", "message": prompt})
        await message.edit_text("<code>Umm, lemme think...</code>")
        response = co.chat_stream(
            chat_history=chat_history,
            model="command-r-plus",
            message=prompt,
            temperature=0.3,
            tools=[{"name": "internet_search"}],
            connectors=[],
            prompt_truncation="OFF",
        )
        output = ""
        tool_message = ""
        data = []
        for event in response:
            if event.event_type == "tool-calls-chunk":
                if event.tool_call_delta and event.tool_call_delta.text is None:
                    tool_message += ""
                else:
                    tool_message += event.text
            if event.event_type == "search-results":
                data.append(event.documents)
            if event.event_type == "text-generation":
                output += event.text
        if output == "":
            output = "I can't seem to find an answer to that"
        chat_history.append({"role": "CHATBOT", "message": output})
        await db._update_cohere_chat_in_db(user_id, chat_history)
        await message.edit_text(f"<code>{tool_message}</code>")
        await asyncio.sleep(5)
        try:
            data = data[0]
            references = ""
            reference_dict = {}
            for item in data:
                title = item["title"]
                url = item["url"]
                if title not in reference_dict:
                    reference_dict[title] = url

            i = 1
            for title, url in reference_dict.items():
                references += f"**{i}.** [{title}]({url})\n"
                i += 1

            await message.edit_text(
                f"**Question:**`{prompt}`\n**Answer:** {output}\n\n**References:**\n{references}",
                disable_web_page_preview=True
            )

        except IndexError:
            references = ""
            await message.edit_text(
                f"**Question:**`{prompt}`\n**Answer:** {output}\n",
                disable_web_page_preview=True
            )

    except Exception as e:
        await message.edit_text(f"An error occurred: {e}")
