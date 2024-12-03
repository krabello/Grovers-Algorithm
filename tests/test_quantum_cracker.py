from src.quantum_crack import CompletePasswordCracker
from typing import List, Tuple
import unittest
import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Assuming previous code is in quantum_crack.py


class TestQuantumPasswordCracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the cracker once for all tests."""
        cls.cracker = CompletePasswordCracker()

    def assert_password_cracked(self, password: str, msg: str = None):
        """Helper method to verify password cracking."""
        result = self.cracker.crack_password(password)
        self.assertEqual(result, password,
                         msg or f"Failed to crack password '{password}'. Got '{result}'")

    def test_basic_alphanumeric(self):
        """Test basic alphanumeric passwords."""
        passwords = [
            "abc123",
            "def456",
            "xyz789"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_case_sensitivity(self):
        """Test passwords with mixed case."""
        passwords = [
            "AbC123",
            "DEF456",
            "PaSsWoRd"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_special_characters(self):
        """Test passwords with special characters."""
        passwords = [
            "!@#$%^",
            "***###",
            "(){}[]"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_mixed_characters(self):
        """Test passwords with mix of all character types."""
        passwords = [
            "Pass@123",
            "Test#456",
            "Secure!99"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_length_variations(self):
        """Test passwords of different lengths."""
        passwords = [
            "a",        # Single character
            "ab",       # Two characters
            "abc123!@",  # Eight characters
            "LongPass123#"  # Longer password
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_repeated_characters(self):
        """Test passwords with repeated characters."""
        passwords = [
            "aaa",
            "111",
            "abc111abc"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_common_patterns(self):
        """Test common password patterns."""
        passwords = [
            "Password123",
            "Admin!123",
            "Test@1234"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_special_sequences(self):
        """Test passwords with special sequences."""
        passwords = [
            "Hello,World!",
            "User.Name@1",
            "Test-Case_1"
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assert_password_cracked(password)

    def test_invalid_input(self):
        """Test handling of invalid inputs."""
        invalid_passwords = [
            "",             # Empty string
            " ",            # Space
            "£€¥"           # Unsupported characters
        ]
        for password in invalid_passwords:
            with self.subTest(password=password):
                result = self.cracker.crack_password(password)
                print(f"Testing invalid input '{password}': got '{result}'")
                self.assertEqual(result, "Invalid password",
                                 f"Expected 'Invalid password' for '{password}', got '{result}'")

    def test_performance_consistency(self):
        """Test consistency of cracking the same password multiple times."""
        test_password = "Test@123"
        results = []
        for _ in range(5):
            result = self.cracker.crack_password(test_password)
            results.append(result)

        # All results should be identical
        self.assertTrue(all(r == test_password for r in results),
                        f"Inconsistent results for repeated attempts: {results}")


if __name__ == '__main__':
    # Run with detailed output
    unittest.main(verbosity=2)
