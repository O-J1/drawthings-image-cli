"""Holds any img metadata functions"""
from PIL import PngImagePlugin

# Convert the dictionary to a PngInfo object
def extract_metadata(image):
    """Extracts the metadata from the decoded base64 bytestream and allows us to save it"""
    info = PngImagePlugin.PngInfo()
    for key, value in image.info.items():
        # Convert metadata values to strings
        str_value = str(value)
        info.add_text(key, str_value)
    return info
