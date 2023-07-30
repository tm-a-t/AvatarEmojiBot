from telethon.tl import types as tl_types


class Emoji(tl_types.InputStickerSetItem):
    def __init__(self, document: tl_types.TypeInputDocument, emoji: str, bytes_: bytes, keywords: str | None = None):
        self.bytes = bytes_
        super().__init__(document, emoji, keywords=keywords)
