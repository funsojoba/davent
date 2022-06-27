import string
import random


def random_string(length):
    values = string.digits + string.ascii_letters
    return "".join(random.choices(values, k=length))


def random_number(length):
    return "".join(ramdom.choice(string.digits, k=length))
