from telethon import TelegramClient
from telethon.tl import types as tl_types


class Bot(TelegramClient):
    me: tl_types.User | None

    async def _run(self, token: str):
        await self.connect()
        self.me = await self.sign_in(bot_token=token)
        await self.run_until_disconnected()

    def run(self, token: str):
        self.loop.run_until_complete(self._run(token))
