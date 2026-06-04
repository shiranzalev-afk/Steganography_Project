from cryptography.fernet import Fernet

KEY = b'6M6mM8n4L8QyL5l6u0Hq8GxX7m6mP9gD1nH6mJ2xK3Q='

cipher = Fernet(KEY)


def encrypt_data(data):
    return cipher.encrypt(data)


def decrypt_data(data):
    return cipher.decrypt(data)