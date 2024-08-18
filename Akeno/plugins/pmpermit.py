import random

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from Akeno.utils.database import db
from Akeno.utils.handler import *
from config import CMD_HANDLER, ENV_TEMPLATE

blocked_messages = [
    "🤐 User has entered the silent zone.",
    "👻 Message blocked. Ghost mode activated.",
    "🏖️ Sorry, the user is on vacation in Blockland.",
    "🚫 Message blocked. Time for a digital forcefield.",
    "🚷 User temporarily ejected from my DM.",
    "🌑 Blocking vibes only. Silence in progress.",
    "🔇 Shhh... message blocked for tranquility.",
    "🚷 Access denied. User in the digital timeout corner.",
    "⛔ User temporarily MIA from the conversation.",
    "🔒 Message blocked. Secret mission engaged.",
]
unblocked_messages = [
    "🎉 Welcome back! Digital barrier lifted.",
    "🌊 Unblocked! Get ready for a flood of messages.",
    "🗝️ User released from message jail. Freedom at last!",
    "🔓 Breaking the silence!.",
    "📬 User back on the radar. Messages unlocked!",
    "🚀 Soaring back into the conversation!",
    "🌐 Reconnecting user to the chat matrix.",
    "📈 Unblocking for an influx of communication!",
    "🚀 Launching user back into the message cosmos!",
    "🎙️ Unblocked and ready for the conversation spotlight!",
]

WARNS = {}
PREV_MESSAGE = {}

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

@Akeno(
    ~filters.scheduled & filters.command(["allow", "approve", "a"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def allow_pm(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
            user_mention = user.mention
        except Exception as e:
            return await message.reply_text(str(e))
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
        user_mention = message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    else:
        return await message.reply_text(
            "`Reply to a user or give their id/username`"
        )
    if user_id == client.me.id:
        return await message.reply_text("`I can't allow myself`")
    if await db.is_pmpermit(client.me.id, user_id):
        return await message.reply_text("`User is already allowed to pm!`")
    await db.add_pmpermit(client.me.id, user_id)
    await message.reply_text(f"**Allowed:** {user_mention}")

@Akeno(
    ~filters.scheduled & filters.command(["disallow", "disapprove", "d"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def disallow_pm(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
            user_mention = user.mention
        except Exception as e:
            return await message.reply_text(f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
        user_mention = message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    else:
        return await message.reply_text(
            "`Reply to a user or give their id/username`"
        )

    if user_id == client.me.id:
        return await message.reply_text("`I can't disallow myself`")

    if not await db.is_pmpermit(client.me.id, user_id):
        return await message.reply_text("`User is not allowed to pm!`")
    await db.rm_pmpermit(client.me.id, user_id)
    await message.reply_text(
        f"** Disallowed:** {user_mention}"
    )

@Akeno(
    ~filters.scheduled & filters.command(["allowlist", "approvelist"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def allowlist(client: Client, message: Message):
    x = await message.reply_text("`Fetching allowlist...`")
    users = await db.get_all_pmpermits(client.me.id)
    if not users:
        return await x.edit("`No users allowed to pm!`")

    text = "**🍀 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽 𝖴𝗌𝖾𝗋'𝗌 𝖫𝗂𝗌𝗍:**\n\n"
    for user in users:
        try:
            name = (await client.get_users(user["user"])).first_name
            text += f"{name} (`{user['user']}`) | {user['date']}\n"
        except:
            text += f"Unkown Peer (`{user['user']}`) | {user['date']}\n"

    await x.edit(text)

@Akeno(
    ~filters.scheduled & filters.command(["pmpermit"], CMD_HANDLER) & filters.me & ~filters.forwarded
)
async def set_pmpermit(_, message: Message):
    if len(message.command) < 2:
        status = await db.get_env(ENV_TEMPLATE.pmpermit)
        text = "Enabled" if status else "Disabled"
        return await message.reply_text(
            f"**Current PM Permit Setting:** `{text}`\n\nTo change the setting give either `on` or `off` as argument.",
        )
    cmd = message.command[1].lower().strip()
    if cmd == "on":
        await db.set_env(ENV_TEMPLATE.pmpermit, True)
        await message.reply_text("**PM Permit Enabled!**")
    elif cmd == "off":
        await db.set_env(ENV_TEMPLATE.pmpermit, False)
        await message.reply_text("**PM Permit Disabled!**")
    else:
        await message.reply_text("**Invalid Argument!**")

@Akeno(filters.outgoing & filters.private & ~filters.bot)
async def handler_outgoing_pm(client: Client, message: Message):
    if message.chat.id == 777000:
        return

    if not await db.get_env(ENV_TEMPLATE.pmpermit):
        return

    if not await db.is_pmpermit(client.me.id, message.chat.id):
        await db.add_pmpermit(client.me.id, message.chat.id)
        x = await message.reply_text("Approving ...")
        await x.edit_text(
            f"**Auto-Approved Outgoing PM:** {message.chat.first_name}",
        )


@Akeno(filters.incoming & filters.private & ~filters.bot & ~filters.service)
async def handle_incoming_pm(client: Client, message: Message):
    if message.from_user.id == 1191668125:
        return
    if message.from_user.id == 777000:
        return
    if not await db.get_env(ENV_TEMPLATE.pmpermit):
        return
    if await db.is_pmpermit(client.me.id, message.from_user.id):
        return
    if message.from_user.id == 1191668125:
        return
    max_spam = await db.get_env(ENV_TEMPLATE.pm_max_spam)
    max_spam = int(max_spam) if max_spam else 3
    warns = WARNS.get(client.me.id, {}).get(message.from_user.id, max_spam)
    if warns <= 0:
        await client.block_user(message.from_user.id)
        WARNS[client.me.id] = {message.from_user.id: max_spam}
        return await client.send_message(
            message.from_user.id,
            f"**𝖤𝗇𝗈𝗎𝗀𝗁 𝗈𝖿 𝗒𝗈𝗎𝗋 𝗌𝗉𝖺𝗆𝗆𝗂𝗇𝗀 𝗁𝖾𝗋𝖾! 𝖡𝗅𝗈𝖼𝗄𝗂𝗇𝗀 𝗒𝗈𝗎 𝖿𝗋𝗈𝗆 𝖯𝖬 𝗎𝗇𝗍𝗂𝗅 𝖿𝗎𝗋𝗍𝗁𝖾𝗋 𝗇𝗈𝗍𝗂𝖼𝖾.**",
        )
    pm_msg = f"Tiktok 𝐏𝐌 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲!\n\n"
    custom_pmmsg = await db.get_env(ENV_TEMPLATE.custom_pmpermit)
    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n**𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!**"
    else:
        pm_msg += f"**𝖧𝖾𝗅𝗅𝗈 {message.from_user.mention}!**\n𝖳𝗁𝗂𝗌 𝗂𝗌 𝖺𝗇 𝖺𝗎𝗍𝗈𝗆𝖺𝗍𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖺𝗇𝖽 𝗒𝗈𝗎 𝖺𝗋𝖾 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝗇𝗈𝗍 𝗍𝗈 𝗌𝗉𝖺𝗆 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗁𝖾𝗋𝖾! \n**𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!**"
    try:
        pm_pic = await db.get_env(ENV_TEMPLATE.pmpermit_pic)
        if pm_pic and pm_pic.endswith(".mp4"):
            msg = await client.send_video(
                message.from_user.id,
                pm_pic,
                pm_msg,
            )
        elif pm_pic:
            msg = await client.send_photo(
                message.from_user.id,
                pm_pic,
                pm_msg,
            )
        else:
            msg = await client.send_message(
                message.from_user.id,
                pm_msg,
                disable_web_page_preview=True,
            )
    except:
        msg = await client.send_message(
            message.from_user.id,
            pm_msg,
            disable_web_page_preview=True,
        )

    prev_msg = PREV_MESSAGE.get(client.me.id, {}).get(message.from_user.id, None)
    if prev_msg:
        await prev_msg.delete()

    PREV_MESSAGE[client.me.id] = {message.from_user.id: msg}
    WARNS[client.me.id] = {message.from_user.id: warns - 1}

module = modules_help.add_module("pmpermit", __file__)
module.add_command("allow", "Allow a user to pm you.")
module.add_command("disallow", "Disallow a user to pm you.")
module.add_command("allowlist", "List all users allowed to pm you.")
