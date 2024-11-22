# classical_crack.py
import string
import itertools

def brute_force_crack(target_password):
    """Classical brute-force password cracking"""
    charset = string.ascii_lowercase
    password_length = len(target_password)
    attempts = 0
    
    for guess in itertools.product(charset, repeat=password_length):
        attempts += 1
        current_guess = ''.join(guess)
        if current_guess == target_password:
            return current_guess, attempts
            
    return None, attempts