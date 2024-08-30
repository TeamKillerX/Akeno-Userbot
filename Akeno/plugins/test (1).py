import re
from pyrogram import Client, filters
from pyrogram.types import Message

TARGET_CHAT_ID = -1002068064532
TARGET_CHANNEL_ID = -1002195132204

# Optimized list of target patterns with non-capturing groups
TARGET_PATTERNS = [
    r"Drop your TON wallet address",
    r"giving away \d+(?:\.\d+)?(?: TON)?",
    r"\d+(?:\.\d+)?(?: first comments| first \d+(?:\.\d+)? comments)",
    r"TON",
    r"ton"
]

@Client.on_message(filters.chat(TARGET_CHAT_ID) & ~filters.service & ~filters.bot, -1)
async def reply_to_message(client: Client, message: Message):
    try:
        # Check if the message contains text or a caption
        content = message.text or message.caption
        if not content:
            return  # Ignore if there's no content to process

        # Check if the content matches any of the target patterns with case-insensitive search
        if any(re.search(pattern, content, re.IGNORECASE) for pattern in TARGET_PATTERNS):
            if message.sender_chat and message.sender_chat.id == TARGET_CHANNEL_ID:
                await message.reply_text("UQAcpGyz8ciRwYMBQIwT7cHrrmaPgAKNMF95PG-qaPc-hpEA")
                print("Replied to the message with 'ton address'.")
    except Exception as e:
        # Handle and log the exception
        print(f"An error occurred: {e}")
