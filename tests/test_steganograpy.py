import unittest
from app.steganography import encode_message, decode_message
from PIL import Image

class TestSteganography(unittest.TestCase):
    def test_steganography(self):
        message = "Hidden message"
        image_path = "path/to/image.png"
        output_path = "path/to/output.png"
        encode_message(image_path, message, output_path)
        decoded_message = decode_message(output_path)
        self.assertEqual(message, decoded_message)

if __name__ == '__main__':
    unittest.main()
