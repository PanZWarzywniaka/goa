import discord
from goa import generate_images, save_images
import os
from dotenv import load_dotenv
import logging as log

log.basicConfig(filename='logs/bot.log',
                encoding='utf-8', 
                level=log.DEBUG,
                format='%(asctime)s:%(levelname)s:%(message)s',
                )

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

HELP_MSG = """Commands:
        $greet -> prints hello message
        $generate <text prompt> -> generates images and sends to google drive
        $help -> prints this message
        """


@client.event
async def on_ready():
    log.info("Bot ready")


@client.event
async def on_message(message):

    channel = message.channel
    if message.author == client.user:
        return

    if message.content.startswith('$greet'):
        await channel.send("Hello, I'm ready")
        return

    if message.content.startswith('$help'):
        await channel.send(HELP_MSG)
        return

    if message.content.startswith('$generate'):

        prompt = message.content.split(" ", 1)[-1]
        await channel.send(f"Starting to generate images with prompt: {prompt}")
        await channel.send(f"Please wait...")

        r, msg = generate_images(prompt, n=10)
        await channel.send(msg)

        if r is None:
            await channel.send(f"Quiting.")
            return

        await channel.send(f"Now saving to gdrive.")
        await channel.send(f"Please wait...")

        try:
            save_images(r, prompt)
        except Exception:
            log.exception("Saving images exception")
            await channel.send(f"Saving images went wrong!")
            return

        await channel.send(f"All done, ready for the next prompt")
        return

    if message.content.startswith('$'):
        await channel.send(f"Command not recognized!")
        await channel.send(HELP_MSG)
        return


client.run(TOKEN)
