import logging

import discord
from discord.channel import TextChannel


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    async def on_ready(self):
        self.logger.info("bot is ready")

    async def on_message(self, message):
        if not self._validate(message):
            return

        try:
            await self._command(message)
            self.logger.info(f"[ OK ] {message.guild.name} | {message.channel.name}")
        except:
            self.logger.error(f"[FAIL] {message.guild.name} | {message.channel.name}")

    def _validate(self, message):
        channel = message.channel

        if not isinstance(channel, TextChannel):
            return False

        if message.author == self.user:
            return False

        if message.content != "nuke":
            return False

        return True

    async def _command(self, message):
        channel = message.channel
        guild = message.guild

        await channel.delete()
        await guild.create_text_channel(
            channel.name,
            category=channel.category,
            position=channel.position,
            topic=channel.topic,
            slowmode_delay=channel.slowmode_delay,
            nsfw=channel.nsfw,
            overwrites=channel.overwrites,
            default_auto_archive_duration=channel.default_auto_archive_duration,
        )


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run("")
