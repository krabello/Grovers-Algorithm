"""
The brute_force_crack function demonstrates a brute-force approach to password cracking.
It systematically generates and tests every possible combination of characters in the specified
character set until it finds a match. While effective for short passwords, this method becomes
computationally infeasible for longer passwords due to its exponential time complexity.
"""
from timing_utils import TimingUtils
import string
import itertools


@TimingUtils.timing_decorator
def brute_force_crack(target_password):
    """
    Attempts to brute-force crack the given target password.

    Args:
        target_password (str): The password to be cracked.

    Returns:
        tuple: The cracked password and the number of attempts.

    Raises:
        ValueError: If the target password is None or empty.
    """
    if not target_password:
        raise ValueError("Target password cannot be None or empty.")

    charset = string.ascii_letters + string.digits + string.punctuation
    password_length = len(target_password)
    attempts = 0

    for guess in itertools.product(charset, repeat=password_length):
        attempts += 1
        current_guess = ''.join(guess)
        if current_guess == target_password:
            return current_guess, attempts

    return None, attempts

# test code
# if __name__ == "__main__":
#     # Example usage
#     password = "abcdef"
#     result, elapsed_time = brute_force_crack(password)
#     print(
#         f"Cracked Password: {result[0]}, Attempts: {result[1]}, Time: {elapsed_time:.2f} ms"
#     )
