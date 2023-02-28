import openai
from multiprocessing import Pool
import time
import os
from dotenv import load_dotenv
import base64
import logging as log
from io import BytesIO
from PIL import Image
import base64
from .util import get_prompt_from_path

load_dotenv()

openai.organization = os.getenv('OPENAI_ORGANIZATION_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')

MAX_RES = 1024 #maximal resolution allowed by openai

def create_alpha_padding_for_image(image, type):
    w, h = image.size

    if type == "top" or type == "bottom": #horizontal padding
        size = (w, MAX_RES//2)

    if type == "left" or type == "right": #vertical padding
        size = (MAX_RES//2, h)
    
    padding = Image.new(mode="RGBA", size=size, color=(0, 0, 0, 0))
    return padding

def merge_images(image1, image2, type="bottom"):

    w1, h1 = image1.size
    w2, h2 = image2.size

    #determine size of merged image
    if type == "top" or type == "bottom":
        new_size = (max(w1, w2) , h1 + h2)

    if type == "left" or type == "right":
        new_size = (w1 + w2 , max(h1, h2))

    merged = Image.new("RGBA", new_size)

    #merge images
    if type == "top":
        merged.paste(image2)
        merged.paste(image1, (0, h2))
    if type == "bottom":
        merged.paste(image1)
        merged.paste(image2, (0, h1))
    if type == "right":
        merged.paste(image1)
        merged.paste(image2, (w1, 0))
    if type == "left":
        merged.paste(image2)
        merged.paste(image1, (w2, 0))
    
    return merged

def add_padding(img_path, type="top"):

    img = Image.open(img_path)

    padding = create_alpha_padding_for_image(img, type)
    merged = merge_images(img, padding, type)
    merged.save(img_path)

def get_box_selection(image, left, top):
    
    box = [left, top, left+MAX_RES, top+MAX_RES]

    #check if box is not out of image bounds
    w, h = image.size

    if box[2] > w:
        box[2] = w

    if box[3] > h:
        box[3] = h

    return tuple(box)

def parse_image(image_data):
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    return image

def image_to_byte_array(image):
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    return byte_array

def openai_edit_image(image, text_prompt, n=4, format="b64_json"):

    try:
        log.info("Generating images...")
        start_t = time.perf_counter()

        response = openai.Image.create_edit(
            image=image,
            prompt=text_prompt,
            n=n,
            size="1024x1024",
            response_format=format,
        )

        duration = time.perf_counter() - start_t
        log.info(f"Generating images took {duration:.2f}s")

        return response, "Images generated successfully!"

    except openai.error.OpenAIError as e:
        log.info(e.http_status)
        log.info(e.error)
        log.info(e)
        return None, str(e)

def modify_image(img_path, left, top, target_dir):
    prompt = get_prompt_from_path(img_path)
    img = Image.open(img_path)
    box = get_box_selection(img, left, top)
    crop = img.crop(box)
    crop_bytes = image_to_byte_array(crop)
    r, msg = openai_edit_image(crop_bytes, prompt, n=5)

    log.info(msg)

    for i, data in enumerate(r['data']):
        variant = parse_image(data["b64_json"])
        img.paste(variant, box)
        save_path = f"{target_dir}/{prompt}-{i+1}.png"
        img.save(save_path)    

if __name__ == "__main__":
    import sys
    import glob
    log.basicConfig(stream=sys.stdout, level=log.DEBUG)
    img_path = glob.glob(f"{os.getenv('TO_EXTEND_MNT')}/*png")[0]
    # add_padding(img_path, "bottom")
    # modify_image(img_path, 0, 512, os.getenv('EXTENDED_MNT'))
    img = Image.open(img_path)
    log.info(get_box_selection(img, 1000, 1000))
