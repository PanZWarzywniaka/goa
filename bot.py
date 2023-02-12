import discord
from goa import move_images_to_gdrive, download_images, generate_images
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

HELP_MSG = """Commands:
        $greet -> prints hello message
        $generate <text prompt> -> generates images and sends to google drive
        """


@client.event
async def on_ready():
    print("Bot ready")


@client.event
async def on_message(message):

    channel = message.channel
    if message.author == client.user:
        return

    if message.content.startswith('$greet'):
        await channel.send('Siema siema kurwa witam!')
        return

    if message.content.startswith('$help'):
        await channel.send(HELP_MSG)
        return

    if message.content.startswith('$generate'):

        prompt = message.content.split(" ", 1)[-1]
        await channel.send(f"Starting to generate images with prompt: {prompt}")
        await channel.send(f"Please wait...")
        r = generate_images(prompt)

        await channel.send(f"Images generated successfully!")
        await channel.send(f"Starting download")
        await channel.send(f"Please wait...")

        download_images(r, prompt)

        await channel.send(f"Images downloaded successfully!")
        await channel.send(f"Starting upload to Google drive")
        await channel.send(f"Please wait...")

        move_images_to_gdrive()

        await channel.send(f"All done, ready for the next prompt")
        return

    if message.content.startswith('$'):
        await channel.send(f"Command not recognized!")
        await channel.send(HELP_MSG)
        return


client.run(TOKEN)
