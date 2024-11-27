# classical_crack.py

"""
The brute_force_crack function demonstrates a brute-force approach at password cracking.
It systematically generates and tests every possible combination of characters in the specified
character set until it finds a match. While effective for short passwords, this method becomes
computationally infeasible for longer passwords due to its exponential time complexity.
"""

import string
import itertools


def brute_force_crack(target_password):
    charset = string.ascii_lowercase
    password_length = len(target_password)
    attempts = 0

    for guess in itertools.product(charset, repeat=password_length):
        attempts += 1
        current_guess = ''.join(guess)
        if current_guess == target_password:
            return current_guess, attempts

    return None, attempts
