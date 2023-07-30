from telethon import events, Button
from telethon.events.common import EventBuilder
from telethon.tl import types as tl_types
from telethon.tl.custom import Message

from app.bot import Bot
from app.utils import get_full_set_link, get_set_title


class HandlerGroup(list):
    def __init__(self):
        super().__init__()
        self.group_commands = HandlerGenerator(
            lambda command: self.on(events.NewMessage(func=lambda message: is_group_command(message, command)))
        )
        self.added_to_group = self.on(events.ChatAction(func=added_to_group))
        self.private_messages = self.on(events.NewMessage(func=lambda event: event.is_private))

    def on(self, event: EventBuilder):
        def decorator(func):
            self.append((event, func))
            return func

        return decorator

    def apply(self, bot: Bot):
        for event, func in self:
            bot.add_event_handler(func, event)


class HandlerGenerator:
    def __init__(self, func):
        self.func = func

    def __getattr__(self, item):
        return self.func(item)


def is_group(obj) -> bool:
    return isinstance(obj, tl_types.Channel) or isinstance(obj, tl_types.Chat)


def is_command(message: Message, command: str) -> bool:
    return f'/{command}' == message.text.removesuffix(f'@{message.client.me.username}')


def is_group_command(message: Message, command: str) -> bool:
    return is_command(message, command) and is_group(message.chat)


def added_to_group(event: events.ChatAction.Event):
    return (
            is_group(event.chat)
            and event.user_added
            and event.user.is_self
            and hasattr(event.original_update, 'new_participant')
    )


def get_chat_set_link(event: events.ChatAction.Event | Message) -> str:
    link = get_full_set_link(event.chat.id, event.client.me.username)
    title = get_set_title(event.chat.title)
    return f'<a href="{link}">{title}</a>'
