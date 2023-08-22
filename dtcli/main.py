""" DT txt2img and img2img over API in python - DT Version 1.20230818.0"""
# Original edits by Bob Kao - 19/08/2023
# Completely rewritten and turned into CLI tools + packaged by Extra
# Special thanks to L3viathan who without their help I couldnt have patched the arg parser for click + Scyren and Tachyondecay for some tidbits
# Original API script from https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API
from datetime import datetime
import io
import base64
import json
import requests

from PIL import Image
from dtcli.constants import CONFIG_TEMPLATE
from dtcli.util.imgmetadata import extract_metadata
from dtcli.util import log

# Seperates CLI from processing payload, handles response and request.
def process_payload(**kwargs):
    """Responsible for running the actual 'main' function that calls DT"""
    payload = {
        "prompt": kwargs["prompt"],
        "negative_prompt": kwargs["negative_prompt"], 
        "sampler": kwargs["sampler"],
        "seed": kwargs["seed"],
        "steps": kwargs["steps"],
        "model": kwargs["model"],
        "batch_count": kwargs["batch_count"],
        "batch_size": kwargs["batch_size"],
        "guidance_scale": kwargs["guidance_scale"],
        "width": kwargs["wh"][0],
        "height": kwargs["wh"][1]
    }

    try:
        response = requests.post(url=f'{kwargs["url"]}/sdapi/v1/txt2img', json=payload, timeout=CONFIG_TEMPLATE["options"]["timeout"]) # pylint: disable=line-too-long
        response_data = response.json()
        
        for image_data in response_data['images']:

            image_binary = base64.b64decode(image_data.split(",", 1)[0])
            image = Image.open(io.BytesIO(image_binary))

            # Get the current timestamp in a readable format
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Get the image dimensions
            image_width, image_height = image.size

            # Construct the file name with timestamp and image dimensions
            file_name = f'output_{timestamp}_{image_width}x{image_height}.png'

            # Extract metadata
            image_metadata = extract_metadata(image)

            # Save image with metadata using the constructed file name
            image.save(file_name, pnginfo=image_metadata, optimize=True)
            log.success(f"Image saved as {file_name}")
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exception:
        log.error(f"Connection has timed out, {exception}")
    except requests.exceptions.ContentDecodingError as exception:
        log.error(f"Failed to decode: {exception}")
