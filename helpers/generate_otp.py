import string
import random

def get_otp():
    return "".join(random.choices(string.digits, k=6))