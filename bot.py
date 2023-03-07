import discord
from discord.ext import commands
from goa.generate import generate_images, save_images
from goa.extend import modify_image, add_padding
from goa.util import get_filename_from_path
import os
import glob
from dotenv import load_dotenv
import logging as log
import time
import subprocess

log.basicConfig(filename='logs/bot.log',
                encoding='utf-8', 
                level=log.DEBUG,
                format='%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(message)s',
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

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

@bot.event
async def on_ready():
    log.info("Bot ready")

async def remount_gdrive(ctx):
    
    log.info("Remounting gdrive.")
    await ctx.send("Resyncing with Google drive...")
    
    CMD_STR = "umount mnt && rclone mount --daemon goa_drive: mnt"
    result = subprocess.run(CMD_STR, shell=True)

    assert result.returncode == 0, "Remounting gdrive was not successfull."

    while not os.path.exists("mnt/images"):
        time.sleep(0.1)

    log.info("Remounting done.")

async def send_help_msg(ctx):
    HELP_MSG = """Commands:
        $hello -> prints hello message
        $g / $generate <text prompt> -> generates images and sends to google drive
        $help -> prints this message
        $pad [top|bottom|left|right] -> adds alpha padding from specified side
            e.g. $pad bottom
        $modify [x] [y] -> sends request to OpenAI to modify crop of the image, (x,y) values specify top left corner of the crop
                e.g. $modify 0 512
        """

    await ctx.send(HELP_MSG)


@bot.command(pass_context=True)
async def hello(ctx, *args):
    await ctx.send("Hello, I'm ready")

@bot.command()
async def help(ctx, *args):
    await send_help_msg(ctx)

### IMAGE GENERATION

async def generate_and_save_images(ctx, prompt):
    await remount_gdrive(ctx)

    await ctx.send(f"Starting image generation with prompt: {prompt}")
    r = await generate_images(prompt, n=10)

    await ctx.send("Now trying to save images.")

    save_images(r, prompt, target_dir=RAW_IMG_MNT)
    await ctx.send(f"Generating images done, ready for the next prompt")


@bot.command(pass_context=True)
async def g(ctx, *, prompt):
    await generate_and_save_images(ctx, prompt)

@bot.command(pass_context=True)
async def generate(ctx, *, prompt):
    await generate_and_save_images(ctx, prompt)

### PADDING

@bot.command(pass_context=True)
async def pad(ctx, pad_type):

    await remount_gdrive(ctx)

    img_path = glob.glob(f"{TO_EXTEND_MNT}/*png")[0]
    file_name = get_filename_from_path(img_path)
    await ctx.send(f"Padding {pad_type} of {file_name}...")

    add_padding(img_path, pad_type)
    await ctx.send(f"Padding done, ready for the next prompt")

### MODIFYING IMAGES

@bot.command(pass_context=True)
async def modify(ctx, left: int, top: int):

    await remount_gdrive(ctx)
    images = glob.glob(f"{TO_EXTEND_MNT}/*png")
    img_path = images[0] #take the first one
    file_name = get_filename_from_path(img_path)
    await ctx.send(f"Modifying {file_name} from coords ({left},{top})...")

    
    await modify_image(img_path, left, top, EXTENDED_MNT)
    await ctx.send(f"Modifying done, ready for the next prompt")

### ERROR HANDLING

@bot.event
async def on_command_error(context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.
    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    e_string = str(error).capitalize()
    embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=e_string,
            color=0xE02B2B,
        )
    log.error(e_string)
    await context.send(embed=embed)


bot.run(TOKEN)