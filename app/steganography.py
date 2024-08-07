from PIL import Image
from stegano import lsb

def encode_message(input_image_path, message, output_image_path):
    image = Image.open(input_image_path)
    encoded_image = lsb.hide(input_image_path, message)
    encoded_image.save(output_image_path)

def decode_message(input_image_path):
    message = lsb.reveal(input_image_path)
    return message
