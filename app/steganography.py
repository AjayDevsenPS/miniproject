from PIL import Image

def encode_message(image_path, message):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += "###"  # Add delimiter to indicate end of message
    message_bin = ''.join([format(ord(i), "08b") for i in message])
    message_idx = 0

    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))
            for n in range(3):  # RGB
                if message_idx < len(message_bin):
                    pixel[n] = int(bin(pixel[n])[2:-1] + message_bin[message_idx], 2)
                    message_idx += 1
            encoded.putpixel((col, row), tuple(pixel))

    encoded.save("encoded_image.png")

def decode_message(image_path):
    img = Image.open(image_path)
    binary_data = ""
    for row in range(img.height):
        for col in range(img.width):
            pixel = img.getpixel((col, row))
            for n in range(3):  # RGB
                binary_data += bin(pixel[n])[-1]

    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-3:] == "###":
            break

    return decoded_data[:-3]  # Remove the delimiter
