import unittest
from app.encryption import encrypt_message, decrypt_message

class TestEncryption(unittest.TestCase):
    def test_encryption_decryption(self):
        message = "Hello, World!"
        password = "secret"
        encrypted_message = encrypt_message(message, password)
        decrypted_message = decrypt_message(encrypted_message, password)
        self.assertEqual(message, decrypted_message)

if __name__ == '__main__':
    unittest.main()
