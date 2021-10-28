import random

chars = '_@?abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def generate_password(length=6) -> str:
    password = [random.choice(chars) for _ in range(length)]
    return "".join(password)
