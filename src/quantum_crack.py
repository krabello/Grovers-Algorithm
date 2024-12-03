import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
import string
from shared_constants import CHARSET


class GroverCrack:
    def __init__(self):
        # Use 7 bits to represent ~94 characters (2^7 = 128)
        self.bits_per_char = 7
        print(f"Initialized GroverCrack with {len(CHARSET)} characters.")
        print(f"Charset: {CHARSET}")

    def _validate_password(self, password: str) -> bool:
        """Validate that all characters in password are in charset."""
        invalid_chars = set(password) - set(CHARSET)
        if invalid_chars:
            print(
                f"Error: Invalid characters in password: {sorted(invalid_chars)}")
            print(f"Supported characters: {CHARSET}")
            return False
        return True

    def _precompensate_bits(self, binary: str) -> str:
        """Pre-compensate binary encoding for quantum circuit transformations."""
        bits = list(binary)
        for i, j in [(0, 6), (1, 5), (2, 4)]:  # Swap bits for 7-bit encoding
            if bits[i] != bits[j]:
                bits[i], bits[j] = bits[j], bits[i]
        return ''.join(bits)

    def _encode_char(self, char: str) -> str:
        """Encode character to binary with pre-compensation."""
        if char not in CHARSET:
            raise ValueError(f"Character '{char}' not in supported charset")
        index = CHARSET.index(char)
        binary = format(index, f'0{self.bits_per_char}b')
        compensated = self._precompensate_bits(binary)
        return compensated

    def _create_circuit(self, target_char: str) -> QuantumCircuit:
        """Create quantum circuit for single character."""
        qreg = QuantumRegister(self.bits_per_char, 'q')
        creg = ClassicalRegister(self.bits_per_char, 'c')
        circuit = QuantumCircuit(qreg, creg)

        binary = self._encode_char(target_char)

        # Create superposition
        circuit.h(qreg)

        # Apply oracle
        for i, bit in enumerate(binary):
            if bit == '0':
                circuit.x(qreg[i])

        # Phase kickback
        circuit.h(qreg[-1])
        circuit.mcx(list(range(self.bits_per_char - 1)), qreg[-1])
        circuit.h(qreg[-1])

        # Uncompute oracle
        for i, bit in enumerate(binary):
            if bit == '0':
                circuit.x(qreg[i])

        # Apply diffusion
        circuit.h(qreg)
        circuit.x(qreg)
        circuit.h(qreg[-1])
        circuit.mcx(list(range(self.bits_per_char - 1)), qreg[-1])
        circuit.h(qreg[-1])
        circuit.x(qreg)
        circuit.h(qreg)

        # Measure
        circuit.measure(qreg, creg)
        return circuit

    def _decode_measurement(self, bits: str) -> str:
        """Decode measured bits back to character."""
        try:
            index = int(bits, 2)
            return CHARSET[index] if index < len(CHARSET) else '?'
        except ValueError:
            return '?'

    def crack_password(self, target_password: str) -> str:
        """Crack the target password using quantum simulation."""
        if not target_password.strip():
            print(
                f"Invalid password input: '{target_password}' (Reason: Empty or space-only)")
            return "Invalid password"

        if not self._validate_password(target_password):
            return "Invalid password"

        print(f"\nAttempting to crack password: {target_password}")
        result = ""

        for pos, target_char in enumerate(target_password):
            print(f"\nPosition {pos}: {target_char}")

            # Create and simulate circuit
            circuit = self._create_circuit(target_char)
            backend = Aer.get_backend('qasm_simulator')
            circuit = transpile(circuit, backend=backend, optimization_level=3)
            counts = backend.run(circuit, shots=10000).result().get_counts()

            # Analyze results
            sorted_counts = sorted(
                counts.items(), key=lambda x: x[1], reverse=True)
            best_bits = sorted_counts[0][0]
            best_char = self._decode_measurement(best_bits)
            result += best_char

            if best_char != target_char:
                print(f"Warning: Got {best_char}, expected {target_char}")

        print(f"\nFinal cracked password: {result}")
        return result


# def main():
#     """Main function to test the GroverCrack class."""
#     cracker = GroverCrack()

#     passwords = [
#         "abc123",             # Alphanumeric
#         "Password!@#",        # Mixed with special chars
#         "!@#$%^",             # All special chars
#         "aB1#$x",             # Mixed types
#         "123!@#456",          # Numbers and special chars
#         "Hello,World!",       # With punctuation
#     ]

#     for password in passwords:
#         print("\n" + "=" * 50)
#         print(f"Testing password: {password}")
#         result = cracker.crack_password(password)
#         if result != "Invalid password":
#             print(f"Result: {result}")
#             print(f"Match: {result == password}")


# if __name__ == "__main__":
#     main()
