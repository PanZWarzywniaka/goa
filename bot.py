import discord
from goa.generate import generate_images, save_images
from goa.extend import modify_image, add_padding
from goa.util import get_filename_from_path
import os
import glob
from dotenv import load_dotenv
import logging as log

log.basicConfig(filename='logs/bot.log',
                encoding='utf-8', 
                level=log.DEBUG,
                format='%(asctime)s:%(levelname)s:%(message)s',
                )

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

RAW_IMG_MNT = os.getenv('RAW_IMG_MNT')
SELECTED_IMG_MNT = os.getenv("SELECTED_IMG_MNT")
NO_WM_IMG_MNT = os.getenv("NO_WM_IMG_MNT")
TO_UPSCALE_MNT = os.getenv("TO_UPSCALE_MNT")
TO_EXTEND_MNT = os.getenv('TO_EXTEND_MNT')
EXTENDED_MNT = os.getenv('EXTENDED_MNT')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

HELP_MSG = """Commands:
        $hello -> prints hello message
        $g / $generate <text prompt> -> generates images and sends to google drive
        $help -> prints this message
        $ex / $extend -> tools for extending images
            $ex pad [top|bottom|left|right] -> adds alpha padding from specified side
                e.g. $ex pad bottom
            $ex modify [x] [y] -> sends request to OpenAI to modify crop of the image, (x,y) values specify top left corner of the crop
                e.g. $ex modify 0 512
        """


@client.event
async def on_ready():
    log.info("Bot ready")


@client.event
async def on_message(message):

    channel = message.channel
    content = message.content
    if message.author == client.user:
        return

    if content.startswith('$hello'):
        await channel.send("Hello, I'm ready")
        return

    if content.startswith('$help'):
        await channel.send(HELP_MSG)
        return

    if content.startswith('$generate ') or content.startswith('$g '):

        prompt = content.split(" ", 1)[-1]
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
            save_images(r, prompt, target_dir=RAW_IMG_MNT)
        except Exception as e:
            log.exception("Saving images exception")
            await channel.send(f"Saving images went wrong!")
            return

        await channel.send(f"All done, ready for the next prompt")
        return

    
    if content.startswith('$extend ') or content.startswith('$ex '):

        params = content.split(" ")[1:]
        img_path = glob.glob(f"{TO_EXTEND_MNT}/*png")[0]
        file_name = get_filename_from_path(img_path)

        if params[0] == "pad":
            pad_type = params[1]


            await channel.send(f"Padding {pad_type} of {file_name}...")
            try:
                add_padding(img_path, pad_type)
            except Exception as e:
                log.exception("Add padding exception")
                await channel.send(f"Padding images went wrong!")
                return
            
            await channel.send(f"All done, ready for the next prompt")
            return 

        if params[0] == "modify":

            
            await channel.send(f"Modifying {file_name}...")

            left = int(params[1])
            top = int(params[2])
            try:
                modify_image(img_path, left, top, EXTENDED_MNT)
            except Exception as e:
                log.exception("Add padding exception")
                await channel.send(f"Modifying images went wrong!")
                return
            await channel.send(f"All done, ready for the next prompt")
            return

    if content.startswith('$'):
        await channel.send(f"Command not recognized!")
        await channel.send(HELP_MSG)
        return


client.run(TOKEN)
