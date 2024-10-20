import unittest
from PIL import Image
import os
from io import BytesIO
from app.steganography import encode_message, decode_message

class TestSteganography(unittest.TestCase):

    def setUp(self):
        # Create a temporary image for testing
        self.image_path = "test_image.png"
        self.message = "Hidden message"
        self.create_test_image(self.image_path)

    def create_test_image(self, path):
        # Create a simple white image for testing
        img = Image.new('RGB', (10, 10), color='white')
        img.save(path)

    def test_encode_message(self):
        """Test that the message is correctly encoded into the image."""
        encoded_image = encode_message(self.image_path, self.message)
        self.assertIsNotNone(encoded_image, "Encoded image should not be None")
        
        # Save the encoded image to a BytesIO stream to avoid writing to disk
        with BytesIO() as output:
            encoded_image.save(output, format="PNG")
            output.seek(0)
            self.assertGreater(output.getbuffer().nbytes, 0, "Encoded image should have content")

    def test_decode_message(self):
        """Test that the message is correctly decoded from the image."""
        encoded_image = encode_message(self.image_path, self.message)
        
        # Save the encoded image to a temporary file for decoding
        encoded_image.save(self.image_path)

        decoded_message = decode_message(self.image_path)
        self.assertEqual(self.message, decoded_message, "Decoded message should match the original message")

    def tearDown(self):
        # Clean up the temporary image file
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

if __name__ == '__main__':
    unittest.main()
