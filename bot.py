import discord
from discord.ext import commands
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

bot = commands.Bot(command_prefix='$', intents=intents)



@bot.event
async def on_ready():
    log.info("Bot ready")


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

### IMAGE GENERATION

async def generate_and_save_images(ctx, prompt):
    await ctx.send(f"Starting image generation of prompt: {prompt}")
    r, msg = generate_images(prompt, n=10)
    await ctx.send(msg)
    await ctx.send("Now trying to save images")

    if r is None:
        await ctx.send(f"Quiting.")
        return
    try:
        save_images(r, prompt, target_dir=RAW_IMG_MNT)
    except IOError:
        log.exception("Saving images, IOError exception")
        await ctx.send(f"Saving images went wrong! (IOError exception)")
    except Exception:
        log.exception("Saving generated images exception")
        await ctx.send(f"Saving generated images went wrong!")
    else: #print success
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
    img_path = glob.glob(f"{TO_EXTEND_MNT}/*png")[0]
    file_name = get_filename_from_path(img_path)
    await ctx.send(f"Padding {pad_type} of {file_name}...")

    try:
        add_padding(img_path, pad_type)
    except Exception:
        log.exception("Add padding exception")
        await ctx.send(f"Padding images went wrong!")
    else: #print success
        await ctx.send(f"Padding done, ready for the next prompt")

### MODIFYING IMAGES

@bot.command(pass_context=True)
async def modify(ctx, left: int, top: int):
    img_path = glob.glob(f"{TO_EXTEND_MNT}/*png")[0]
    file_name = get_filename_from_path(img_path)
    await ctx.send(f"Modifying {file_name} from coords ({left},{top})...")

    try:
        modify_image(img_path, left, top, EXTENDED_MNT)
    except IOError:
        log.exception("Saving images, IOError exception")
        await ctx.send(f"Saving images went wrong! (IOError exception)")
    except Exception:
        log.exception("Saving images exception")
        await ctx.send(f"Saving images went wrong!")
    else: #print success
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