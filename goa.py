import openai
from multiprocessing import Pool
import time
import os
from dotenv import load_dotenv
import base64
import logging as log

load_dotenv()

openai.organization = os.getenv('OPENAI_ORGANIZATION_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')
TARGET_DIR = os.getenv('RAW_IMG_MNT')


def generate_images(text_prompt, n=4, format="b64_json"):

    log.info("Generating images...")
    start_t = time.perf_counter()

    try:
        response = openai.Image.create(
            prompt=text_prompt,
            n=n,
            size="1024x1024",
            response_format=format,
        )
    except openai.error.OpenAIError as e:
        log.info(e.http_status)
        log.info(e.error)
        log.info(e)

    duration = time.perf_counter() - start_t
    log.info(f"Generating images took {duration:.2f}s")
    return response


def _save_image(image_data):

    start = time.perf_counter()
    bytes_obj, img_name = image_data

    b64_bytes = bytes_obj['b64_json']
    with open(f"{TARGET_DIR}/{img_name}", "wb") as f:
        f.write(base64.b64decode(b64_bytes))

    duration = time.perf_counter()-start
    return img_name, duration


def save_images(response, prompt):

    log.info("Saving images")
    start_t = time.perf_counter()

    image_bytes_list = response["data"]
    images_names = [f'{prompt}-{i+1}.png' for i,  # create a list of image names e.g. "van gogh-1","van gogh-2" ...
                    _ in enumerate(image_bytes_list)]

    image_data = list(zip(image_bytes_list, images_names))

    with Pool(processes=len(image_data)) as pool:

        results = pool.imap_unordered(_save_image, image_data)

        for file_name, duration in results:
            log.info(f"{file_name} completed in {duration:.2f}s")

    duration = time.perf_counter() - start_t
    log.info(f"Saving images took {duration:.2f}s")


if __name__ == "__main__":
    import sys
    log.basicConfig(stream=sys.stdout, level=log.DEBUG)

    prompt = "soviet propaganda poster space mission"
    x = generate_images(prompt)
    save_images(x, prompt)
