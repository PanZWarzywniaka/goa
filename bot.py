import discord
from goa import move_images_to_gdrive, download_images, get_images_urls

TOKEN = "MTA3MDc2NjcwMDQ5ODI3NjQxMw.G-ZwjP.0agN6BkL6kv94MiNKwG0tU2QHxc3gzVaNmkzJk"
URL = "https://discord.com/api/oauth2/authorize?client_id=1070766700498276413&permissions=534723950656&scope=bot"

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot ready")

@client.event
async def on_message(message):

    channel = message.channel
    if message.author == client.user:
        return

    if message.content=='$greet':
        await channel.send('Siema siema kurwa witam!')

    if message.content.startswith('$help'):
        msg = """Commands:
        $greet -> prints hello message
        $generate <text prompt> -> generates images and sends to google drive
        """
        await channel.send(msg)

    if message.content.startswith('$generate'):

        prompt = message.content.split(" ", 1)[-1]
        await channel.send(f"Starting to generate images with prompt: {prompt}")
        await channel.send(f"Please wait...")
        r = get_images_urls(prompt)

        await channel.send(f"Images generated successfully!")
        await channel.send(f"Starting download")
        await channel.send(f"Please wait...")

        download_images(r, prompt)


        await channel.send(f"Images downloaded successfully!")
        await channel.send(f"Starting upload to Google drive")
        await channel.send(f"Please wait...")

        move_images_to_gdrive()

        await channel.send(f"All done, ready for the next prompt")


client.run(TOKEN)