import os
import openai
import subprocess
import glob
import shutil
from multiprocessing import Pool
import time
import random

API_KEY = "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"
ORGANIZATION_ID = "org-SDlc2kVFVS1lrhTdObWKGBvd"

openai.organization = ORGANIZATION_ID
openai.api_key = API_KEY

def get_images_urls(text_prompt: str):
  try:
    response = openai.Image.create(
      prompt=text_prompt,
      n=4,
      size="1024x1024"
    )
  except openai.error.OpenAIError as e:
    print(e.http_status)
    print(e.error)
    print(e)

  return response


def download_image(image):

  start_t = time.perf_counter()

  file_name, url = image
  cmd = ["wget", '-q', f'-O {file_name}', url]
  temp = subprocess.Popen(cmd)
  output = str(temp.communicate())

  end_t = time.perf_counter()

  return file_name, end_t-start_t

def download_images(response, name):

  start_t = time.perf_counter()

  #list of [(filename, url)...]
  images = [(f'{name}-{i+1}.png', entry['url']) for i, entry in enumerate(response['data'])]

  with Pool(processes=len(images)) as pool:
      
    results = pool.imap_unordered(download_image, images)

    for file_name, duration in results:
        print(f"{file_name} completed in {duration:.2f}s")

  end_t = time.perf_counter()
  duration = end_t - start_t
  print(f"Whole process took {duration:.2f}s")


def move_file_to_gdrive(file_name):
    start_t = time.perf_counter()
    shutil.move(src=file_name, dst=f"gdrive_images/{file_name}")

    end_t = time.perf_counter()

    return file_name, end_t-start_t

def move_images_to_gdrive():


    start_t = time.perf_counter()
    file_names = glob.glob('*.png')

    with Pool(processes=len(file_names)) as pool:
        
        results = pool.imap_unordered(move_file_to_gdrive, file_names)

        for file_name, duration in results:
            print(f"{file_name} completed in {duration:.2f}s")


    end_t = time.perf_counter()
    duration = end_t - start_t
    print(f"Whole process took {duration:.2f}s")    

