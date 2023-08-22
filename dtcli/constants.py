from pathlib import Path


FOLDER_NAME = "DrawThings Output"
CONFIG_FILENAME = "dt_config.toml"
CONFIG_TEMPLATE = { "options":{
            "url": "http://127.0.0.1:7860", 
            "timeout": 120,
            "prompt": "(limited palette blue black:1.1), creative (command line interface CLI:1.3) connected to a (blue magical tesseract glowing cube:1.2), no humans",
            "negative_prompt": "human, man, woman, child, simple background, (low quality, worst quality, normal quality), hand",
            "seed": -1,
            "steps": 30,
            "sampler": "Euler a",
            "batch_size": 1,
            "batch_count": 1,
            "guidance_scale": 7,
            "hires_fix": False,
            "default_model_list": ['Generic (Stable Diffusion v1.5)', 'SDXL Base (v1.0)'],
            "manual_model_list": [],
            "avail_models_api": []
}}

CWD = Path.cwd()

CONFIG_PATH = CWD / CONFIG_FILENAME
FOLDER_PATH = CWD / FOLDER_NAME

# Storing multiple image dimensions with aspect ratios using a list of tuples
IMAGE_DIMENSION_LIST = [
    (512, 512),  # Width x Height
    (512, 768),
    (768, 512),
    (768, 384),
    (384, 768),
    (640, 640),
    (640, 960),
    (960, 640),
    (768, 768),
    (1024,512),
    (512,1024),
    (1024,576),
    (576,1024),
    (960, 960),
    (768, 1152),
    (1280, 640),
    (640, 1280),
    (1024,1024)
]
