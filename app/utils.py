from random import choice

letters = "abcdefghijklmnopqrstuvwxyz"


def create_link() -> str:
    return "".join([choice(letters) for i in range(7)])