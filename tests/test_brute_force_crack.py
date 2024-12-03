from src.timing_utils import TimingUtils
import unittest
import sys
import os
from src.classical_crack import brute_force_crack

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'src')))


class TestBruteForceCrack(unittest.TestCase):
    def assert_password_cracked(self, password: str, msg: str = None):
        """Helper method to verify password cracking."""
        cracked_password, _ = brute_force_crack(
            password)  # Extract the cracked password from the result tuple
        if isinstance(cracked_password, tuple):
            # Extract actual password if it's a tuple
            cracked_password = cracked_password[0]
        self.assertEqual(cracked_password, password,
                         msg or f"Failed to crack password '{password}'. Got '{cracked_password}'")

    def test_short_passwords(self):
        """Test short passwords for successful cracking."""
        passwords = [
            "a",
            "ab",
            "abc"
        ]
        for password in passwords:
            with self.subTest(password=password):
                cracked_password, _ = brute_force_crack(password)
                if isinstance(cracked_password, tuple):
                    # Extract actual password if it's a tuple
                    cracked_password = cracked_password[0]
                self.assertEqual(cracked_password, password,
                                 f"Failed to crack password '{password}'. Got '{cracked_password}'")

    def test_special_characters(self):
        """Test passwords containing special characters."""
        passwords = [
            "@",
            "#$",
            "&*()",
            "!%^",
            "~<>|"
        ]
        for password in passwords:
            with self.subTest(password=password):
                cracked_password, _ = brute_force_crack(password)
                if isinstance(cracked_password, tuple):
                    # Extract actual password if it's a tuple
                    cracked_password = cracked_password[0]
                self.assertEqual(cracked_password, password,
                                 f"Failed to crack password '{password}'. Got '{cracked_password}'")

    def test_numeric_passwords(self):
        """Test numeric passwords."""
        passwords = [
            "1",
            "12",
            "1234"
        ]
        for password in passwords:
            with self.subTest(password=password):
                cracked_password, _ = brute_force_crack(password)
                if isinstance(cracked_password, tuple):
                    # Extract actual password if it's a tuple
                    cracked_password = cracked_password[0]
                self.assertEqual(cracked_password, password,
                                 f"Failed to crack password '{password}'. Got '{cracked_password}'")

    def test_alphanumeric_passwords(self):
        """Test passwords with a mix of letters and numbers."""
        passwords = [
            "a1",
            "A1b2",
            "abc123",
            "XYZ789"
        ]
        for password in passwords:
            with self.subTest(password=password):
                cracked_password, _ = brute_force_crack(password)
                if isinstance(cracked_password, tuple):
                    # Extract actual password if it's a tuple
                    cracked_password = cracked_password[0]
                self.assertEqual(cracked_password, password,
                                 f"Failed to crack password '{password}'. Got '{cracked_password}'")

    def test_value_error_on_invalid_input(self):
        """Test that invalid inputs raise ValueError."""
        invalid_inputs = [
            None,
            ""
        ]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    brute_force_crack(invalid_input)


if __name__ == "__main__":
    unittest.main(verbosity=2)
