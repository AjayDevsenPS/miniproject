import pytest
from PIL import Image
from io import BytesIO



def encode_message(image_path, message):
    # Open the image
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    total_pixels = width * height * 3  # Each pixel has 3 color channels (RGB)
    
    # Add a delimiter to the message to indicate the end
    message += "###"
    message_bin = ''.join([format(ord(char), "08b") for char in message])
    
    # Check if the image can hold the message
    if len(message_bin) > total_pixels:
        raise ValueError("Message is too long to encode in the provided image.")
    
    message_idx = 0
    
    # Iterate over each pixel in the image
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))
            for n in range(3):  # RGB channels
                if message_idx < len(message_bin):
                    # Modify the least significant bit (LSB)
                    pixel[n] = pixel[n] & ~1 | int(message_bin[message_idx])
                    message_idx += 1
            encoded.putpixel((col, row), tuple(pixel))
            if message_idx >= len(message_bin):
                break
        if message_idx >= len(message_bin):
            break
    
    # Return the encoded image
    return encoded


def decode_message(image_path):
    img = Image.open(image_path)
    binary_data = ""
    
    # Iterate over each pixel in the image
    for row in range(img.height):
        for col in range(img.width):
            pixel = img.getpixel((col, row))
            for n in range(3):  # RGB channels
                # Extract the least significant bit (LSB)
                binary_data += str(pixel[n] & 1)
    
    # Split binary data into 8-bit chunks
    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    
    # Convert from binary to string
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        # Break if the delimiter is found
        if decoded_data[-3:] == "###":
            return decoded_data[:-3]  # Return decoded message without delimiter

    # If no delimiter is found, return an empty string
    return ""


# Utility function to create a blank image
def create_blank_image(width, height, color=(255, 255, 255)):
    img = Image.new('RGB', (width, height), color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# Test case for encoding a short message
def test_encode_message_short():
    img_bytes = create_blank_image(100, 100)
    encoded_img = encode_message(img_bytes, "Hello")
    assert isinstance(encoded_img, Image.Image)

# Test case for decoding a short message
def test_decode_message_short():
    img_bytes = create_blank_image(100, 100)
    encoded_img = encode_message(img_bytes, "Hello")
    
    # Save encoded image to BytesIO for decoding test
    img_buffer = BytesIO()
    encoded_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    decoded_message = decode_message(img_buffer)
    assert decoded_message == "Hello"

# Test case for encoding a long message
def test_encode_message_long():
    img_bytes = create_blank_image(200, 200)
    long_message = "A" * 500  # Long message of 500 characters
    encoded_img = encode_message(img_bytes, long_message)
    assert isinstance(encoded_img, Image.Image)

# Test case for decoding a long message
def test_decode_message_long():
    img_bytes = create_blank_image(200, 200)
    long_message = "A" * 500
    encoded_img = encode_message(img_bytes, long_message)
    
    # Save encoded image to BytesIO for decoding test
    img_buffer = BytesIO()
    encoded_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    decoded_message = decode_message(img_buffer)
    assert decoded_message == long_message

# Test case for encoding an empty message
def test_encode_empty_message():
    img_bytes = create_blank_image(100, 100)
    encoded_img = encode_message(img_bytes, "")
    assert isinstance(encoded_img, Image.Image)

# Test case for decoding an empty message
def test_decode_empty_message():
    img_bytes = create_blank_image(100, 100)
    encoded_img = encode_message(img_bytes, "")
    
    # Save encoded image to BytesIO for decoding test
    img_buffer = BytesIO()
    encoded_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    decoded_message = decode_message(img_buffer)
    assert decoded_message == ""

# Test case for encoding a message in a very large image
def test_encode_message_large_image():
    img_bytes = create_blank_image(1000, 1000)
    encoded_img = encode_message(img_bytes, "Test")
    assert isinstance(encoded_img, Image.Image)

# Test case for decoding from an unmodified image
def test_decode_from_unmodified_image():
    img_bytes = create_blank_image(100, 100)  # Unmodified image
    decoded_message = decode_message(img_bytes)
    assert decoded_message == ""  # Expect no message in unmodified image

# Test case for encoding special characters
def test_encode_message_special_characters():
    img_bytes = create_blank_image(100, 100)
    special_message = "!@#$%^&*()"
    encoded_img = encode_message(img_bytes, special_message)
    assert isinstance(encoded_img, Image.Image)

# Test case for decoding special characters
def test_decode_message_special_characters():
    img_bytes = create_blank_image(100, 100)
    special_message = "!@#$%^&*()"
    encoded_img = encode_message(img_bytes, special_message)
    
    # Save encoded image to BytesIO for decoding test
    img_buffer = BytesIO()
    encoded_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    decoded_message = decode_message(img_buffer)
    assert decoded_message == special_message

# Test case for encoding a message in a transparent image (if applicable)
def test_encode_message_transparent_image():
    img = Image.new("RGBA", (100, 100), (255, 255, 255, 0))  # Transparent image
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    encoded_img = encode_message(img_bytes, "Hello")
    assert isinstance(encoded_img, Image.Image)

# Test case for decoding from a transparent image (if applicable)
def test_decode_message_transparent_image():
    img = Image.new("RGBA", (100, 100), (255, 255, 255, 0))  # Transparent image
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    encoded_img = encode_message(img_bytes, "Hello")
    
    # Save encoded image to BytesIO for decoding test
    img_buffer = BytesIO()
    encoded_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    decoded_message = decode_message(img_buffer)
    assert decoded_message == "Hello"

# Test case for encoding a message in a very small image
def test_encode_message_small_image():
    img_bytes = create_blank_image(10, 10)
    with pytest.raises(ValueError):  # Assuming your code handles this case with an exception
        encode_message(img_bytes, "This message is too long for the image!")

