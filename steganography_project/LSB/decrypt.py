from base64 import urlsafe_b64encode
from hashlib import md5

from cryptography.fernet import Fernet

from LSB.utils import str2bin, bin2str

class Decryptor:
    """Responsible for decrypting steganography of many images using a given key"""
    def __init__(self, password: str):
        _hash = md5(password.encode()).hexdigest()
        cipher_key = urlsafe_b64encode(_hash.encode())
        self.__encryptor = Fernet(cipher_key)


    @staticmethod
    def __extract_data_length_from_image(im):
        bits = ""
        height, width, _ = im.shape

        count = 0
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    bits += str(im[i, j][k] & 1)
                    count += 1
                    if count == 32:
                        return int(bits, 2)

    @staticmethod
    def __extract_data_from_image(im, data_length):
        bits = ""
        height, width, _ = im.shape

        count = 0
        skip = 32

        for i in range(height):
            for j in range(width):
                for k in range(3):

                    if skip:
                        skip -= 1
                        continue

                    bits += str(im[i, j][k] & 1)
                    count += 1

                    if count == data_length:
                        return bin2str(bits)

    def decrypt(self, im) -> str:
        """Decrypts the hidden message in `im`."""
        data_length = self.__extract_data_length_from_image(im)
        data = self.__extract_data_from_image(im, data_length)
        message = self.__encryptor.decrypt(data.encode()).decode()
        return message
