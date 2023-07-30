# Avatar Emoji Bot

## About

Avatar Emoji Bot uses the new [custom emoji feature.](https://t.me/CustomEmojiPacks) It generates an emoji pack of group members’ rounded avatars.

https://t.me/AvatarEmojiBot

![-2147483648_-212950](https://github.com/tm-a-t/AvatarEmojiBot/assets/38432588/eea27db8-b526-4cbe-8d64-7e1aad6c1c5e)

![-2147483648_-212956](https://github.com/tm-a-t/AvatarEmojiBot/assets/38432588/6aae2107-8f45-4d58-b8ae-1bd32a2e1d44)


## Features

- When added to group, generates a pack.
- When `/update` command is used in the group, regenerates the pack.
- Replies to private messages with an 'Add me to group' button

## Run yourself

You need Python 3.11 and [Poetry](https://python-poetry.org/docs/) installed.

1. Create a bot with [BotFather](https://t.me/BotFather) and get the bot token.

2. Create `.env` file. Put your bot token and [Telegram API key](my.telegram.org) there as in [`.env.example`](/tm-a-t/AvatarEmojiBot/blob/main/.env.example).

3.
    ```shell
    poetry install
    python -m app
    ```
