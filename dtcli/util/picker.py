"""Responsible for displaying the pick interface to the user for model and image size"""
import math
import pick as pick_module
from dtcli.util.getmodels import get_available_models
from dtcli.constants import IMAGE_DIMENSION_LIST

def pick_model(url, models):
    available_models = get_available_models(url)

    if available_models:
        models = available_models
    return pick_module.pick(
        models,
        "Please choose the model you wish to generate with:",
        indicator="=>",
        multiselect=False
    )[0]

# def pick_model(url, models):
#     available_models = get_available_models(url)

#     if available_models:
#         models = available_models
#     selected_option, _ = pick_module.pick(
#         models,
#         "Please choose the model you wish to generate with:",
#         indicator="=>",
#         multiselect=False
#     )
#     return selected_option
   

def calculate_aspect_ratio(width, height):
    """Calculates the aspect ratio of an image dimension"""
    gcd = math.gcd(width, height)
    aspect_width = width // gcd
    aspect_height = height // gcd
    return f"{aspect_width}:{aspect_height}"

def display_image_size_options(options):
    """Displays image size options to the user and returns the chosen option"""

    title = "Please choose an image dimension: "
    image_options = pick_module.pick(options, title, indicator="=>", default_index=0)
    return image_options

def image_size_picker():
    """Allows the user to pick an image dimension from a list of options"""
    image_dimensions_with_aspect_ratios = []

    chosen_img_size_log =""

    # Calculate aspect ratios and store them alongside the dimensions
    for width, height in IMAGE_DIMENSION_LIST:
        aspect_ratio = width / height
        aspect_ratio_str = calculate_aspect_ratio(width, height)
        image_dimensions_with_aspect_ratios.append((width, height, aspect_ratio, aspect_ratio_str))

    # Display the options to the user
    options = [
        f"{width}x{height} ({aspect_ratio_str})"  # Format string with width, height, and aspect ratio  pylint: disable=line-too-long
        for width, height, aspect_ratio, aspect_ratio_str in image_dimensions_with_aspect_ratios
    ]

    chosen_image_option = display_image_size_options(options)  # Call the function once

    chosen_tuple = next(item for item in image_dimensions_with_aspect_ratios if f"{item[0]}x{item[1]}" in chosen_image_option[0]) # pylint: disable=line-too-long
    width, height = chosen_tuple[0], chosen_tuple[1]

    chosen_img_size_log = chosen_image_option[0]  # Store the chosen option
    return width, height, chosen_img_size_log
