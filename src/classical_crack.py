# classical_crack.py

"""
The `brute_force_crack` function demonstrates a brute-force approach to password cracking. 
It systematically generates and tests every possible combination of characters in the specified 
character set until it finds a match. While effective for short passwords, this method becomes 
computationally infeasible for longer passwords due to its exponential time complexity.
"""

import string
import itertools

def brute_force_crack(target_password):
    """Classical brute-force password cracking"""
    # Define the character set to use for guessing (lowercase English letters)
    charset = string.ascii_lowercase
    # Determine the length of the target password
    password_length = len(target_password)
    # Initialize a counter to track the number of guessing attempts
    attempts = 0
    
    # Generate all possible combinations of characters from the charset
    # with a length equal to the target password
    for guess in itertools.product(charset, repeat=password_length):
        # Increment the attempts counter for each guess
        attempts += 1
        # Convert the tuple of characters from itertools.product into a string
        current_guess = ''.join(guess)
        # Check if the current guess matches the target password
        if current_guess == target_password:
            # If a match is found, return the guessed password and the number of attempts
            return current_guess, attempts
            
    # If no match is found (unlikely), return None and the total number of attempts
    return None, attempts
