import asyncio

from telethon import events, Button
from telethon.tl.custom import Message

from app.functions import emoji_sets
from app.handlers.utils import HandlerGroup, get_chat_set_link

handlers = HandlerGroup()
lock = asyncio.Lock()


@handlers.added_to_group
async def _(event: events.ChatAction.Event):
    await event.respond('Creating an emoji pack...')

    user_id = event.original_update.new_participant.inviter_id
    async with lock:
        is_created = await emoji_sets.create_set(event.client, event.chat, user_id, existing=False)

    if is_created:
        await event.respond(f'Created!\n{get_chat_set_link(event)}', parse_mode='html')
    else:
        await event.respond(f'Pack updated!\n{get_chat_set_link(event)}', parse_mode='html')


@handlers.group_commands.update
async def _(message: Message):
    info_message = await message.respond('Updating the emoji pack...')

    async with lock:
        await emoji_sets.create_set(message.client, message.chat, message.sender_id, existing=True)

    await info_message.reply(f'Emoji pack updated!\n{get_chat_set_link(message)}', parse_mode='html')


@handlers.private_messages
async def _(message: Message):
    button = Button.url('Choose group', f't.me/{message.client.me.username}?startgroup')
    await message.respond('Hello! Add me to group to start.', buttons=button)
