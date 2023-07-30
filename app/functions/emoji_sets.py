import hashlib
from io import BytesIO
from random import randint

from PIL import Image
from telethon.errors import PackShortNameOccupiedError, BadRequestError, StickersetInvalidError
from telethon.functions import stickers, messages
from telethon.tl import types as tl_types
from telethon.tl.functions.messages import UploadMediaRequest
from telethon.types import Chat, Channel
from telethon.utils import get_input_document

from app.bot import Bot
from app.functions._emoji import Emoji
from app.utils import get_set_title, get_set_link

mask_image = Image.open('mask.png').convert('L')


async def create_set(bot: Bot, chat: Chat | Channel, user_id: int, *, existing: bool) -> bool:
    title = get_set_title(chat.title)
    link = get_set_link(chat.id, bot.me.username)

    emojis = await create_emoji_items(bot, chat)

    if not existing:
        request = stickers.CreateStickerSetRequest(254210206, title, link, emojis, emojis=True)
        try:
            await bot(request)
        except PackShortNameOccupiedError:
            pass
        else:
            return True

    get_set_request = messages.GetStickerSetRequest(tl_types.InputStickerSetShortName(link), hash=randint(1, 10 ** 9))
    try:
        emoji_set: tl_types.messages.StickerSet = await bot(get_set_request)
    except StickersetInvalidError:
        return await create_set(bot, chat, user_id, existing=False)

    input_emoji_set = tl_types.InputStickerSetShortName(link)

    if emoji_set.set.title != title:
        update_title_request = stickers.RenameStickerSetRequest(input_emoji_set, title)
        await bot(update_title_request)

    for emoji in emojis:
        add_request = stickers.AddStickerToSetRequest(input_emoji_set, emoji)
        await bot(add_request)

    for document in emoji_set.documents:
        remove_request = stickers.RemoveStickerFromSetRequest(get_input_document(document))
        try:
            await bot(remove_request)
        except BadRequestError:
            pass


async def create_emoji_items(bot: Bot, chat: Chat | Channel) -> list[Emoji]:
    items = []

    if chat.photo:
        photo: bytes = await bot.download_profile_photo(chat, bytes)
        items.append(await create_emoji(bot, photo))

    async for user in bot.iter_participants(chat):
        if user.is_self:
            continue
        if user.photo is None or isinstance(user.photo, tl_types.UserProfilePhotoEmpty):
            continue

        photo: bytes = await bot.download_profile_photo(user, bytes)
        items.append(await create_emoji(bot, photo, keywords=user.username or None))

        if len(items) == 120:
            # reached max number of emoji
            break

    return items


async def create_emoji(bot: Bot, original_photo_bytes: bytes, *, keywords: str = None) -> Emoji:
    new_photo_bytes_io = BytesIO()
    image = Image.open(BytesIO(original_photo_bytes))
    image_resized = image.resize((90, 90))
    image_resized.putalpha(mask_image)
    container_image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    container_image.paste(image_resized, (5, 5))
    container_image.save(new_photo_bytes_io, format='webp')
    new_photo_bytes = new_photo_bytes_io.getvalue()

    file = await bot.upload_file(new_photo_bytes_io.getvalue())
    mime = 'image/webp'
    uploaded_document = tl_types.InputMediaUploadedDocument(file, mime, [])
    media = await bot(UploadMediaRequest(tl_types.InputPeerSelf(), uploaded_document))
    input_document = get_input_document(media)

    return Emoji(input_document, '🟣', new_photo_bytes, keywords=keywords)


async def get_emoji_set_hash_set(bot: Bot, emoji_set: tl_types.messages.StickerSet):
    hash_set = set()
    for document in emoji_set.documents:
        emoji_bytes = await bot.download_file(document, bytes)
        emoji_hash = hashlib.sha256(emoji_bytes).hexdigest()
        hash_set.add(emoji_hash)
    return hash_set
