"""
Simulates a quantum password cracker using Grover's algorithm principles.
The circuit creates a quantum oracle for matching the target password
and uses Qiskit's Aer simulator to estimate the quantum search process.
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from timing_utils import TimingUtils
import numpy as np
import string


from qiskit.circuit import Gate


def create_oracle(target_binary, qubits_per_char):
    """
    Creates a quantum oracle for marking the target binary state.

    Args:
        target_binary (str): Binary representation of the target password.
        qubits_per_char (int): Number of qubits per character.

    Returns:
        Gate: The oracle gate.
    """
    n_qubits = len(target_binary)
    quantum_register = QuantumRegister(n_qubits, 'q')
    oracle_circuit = QuantumCircuit(quantum_register, name="oracle")

    # Apply X gates to flip the target bits
    for i, bit in enumerate(target_binary):
        if bit == '0':
            oracle_circuit.x(quantum_register[i])

    # Add a multi-controlled Z gate to mark the state
    # Put the last qubit into the |+> state
    oracle_circuit.h(quantum_register[-1])
    oracle_circuit.mcx(list(range(n_qubits - 1)),
                       quantum_register[-1])  # Multi-controlled X
    # Return the last qubit to the |0> state
    oracle_circuit.h(quantum_register[-1])

    # Revert the X gates applied earlier
    for i, bit in enumerate(target_binary):
        if bit == '0':
            oracle_circuit.x(quantum_register[i])

    # Convert the circuit to a gate
    oracle_gate = oracle_circuit.to_gate()
    oracle_gate.name = "Oracle"  # Name the gate for visualization

    return oracle_gate


def apply_grover_iteration(circuit, quantum_register, oracle):
    """Applies a single iteration of Grover's algorithm."""
    circuit.append(oracle, quantum_register)  # Apply oracle
    circuit.h(quantum_register)
    circuit.x(quantum_register)
    circuit.h(quantum_register)


@TimingUtils.timing_decorator
def grover_crack(target_password, charset=string.ascii_lowercase[:16]):
    """
    Simulates Grover's algorithm to crack a password.

    Args:
        target_password (str): The password to be cracked.
        charset (str): The character set to use (default: lowercase letters).

    Returns:
        tuple: The cracked password and the theoretical number of Grover iterations.
    """
    if not all(c in charset for c in target_password):
        raise ValueError(
            "All characters in the target password must be in the charset.")

    # Calculate the number of qubits required
    qubits_per_char = len(bin(len(charset) - 1)) - 2
    n_qubits = len(target_password) * qubits_per_char
    quantum_register = QuantumRegister(n_qubits, 'q')
    classical_register = ClassicalRegister(n_qubits, 'c')
    circuit = QuantumCircuit(quantum_register, classical_register)

    # Apply Hadamard gates to create superposition
    circuit.h(quantum_register)

    # Convert target password to binary
    target_binary = ''.join([
        format(charset.index(c), f'0{qubits_per_char}b') for c in target_password
    ])
    print(f"Target binary: {target_binary}")

    # Create the oracle circuit
    oracle_circuit = create_oracle(target_binary, qubits_per_char)

    # Add Grover iterations
    iterations = int(np.pi / 4 * np.sqrt(len(charset) ** len(target_password)))
    for _ in range(iterations):
        apply_grover_iteration(circuit, quantum_register, oracle_circuit)

    # Add measurement gates
    circuit.measure_all()

    # Simulate the circuit
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(circuit, shots=10_000)  # Increase shots for accuracy
    result = job.result()
    counts = result.get_counts()

    # Visualize measurement results
    plot_histogram(counts).show()

    # Decode the most frequent measurement result
    try:
        measured_bits = max(counts.items(), key=lambda x: x[1])[0]
        print(f"Measured bits: {measured_bits}")
        print(f"Length of measured bits: {len(measured_bits)}")

        # Adjust measured_bits length
        expected_length = len(target_password) * qubits_per_char
        measured_bits = measured_bits[:expected_length].ljust(
            expected_length, '0')
        print(f"Truncated measured bits: {measured_bits}")
        print(f"Adjusted length: {len(measured_bits)}")

        # Decode measured bits into characters
        measured_chars = ''
        for i in range(0, expected_length, qubits_per_char):
            binary_chunk = measured_bits[i:i + qubits_per_char]
            decimal_value = int(binary_chunk, 2)
            print(f"Chunk: {binary_chunk}, Decimal: {decimal_value}")

            if decimal_value < len(charset):
                measured_chars += charset[decimal_value]
            else:
                measured_chars += '?'  # Placeholder for invalid indices

    except (ValueError, IndexError) as e:
        print(f"Error decoding measured bits: {e}")
        measured_chars = "Error"

    # Calculate theoretical Grover iterations
    N = len(charset) ** len(target_password)
    iterations = int(np.pi / 4 * np.sqrt(N))

    return measured_chars, iterations


def verify_result(original, cracked):
    """
    Verifies if the cracked password matches the original password.
    """
    return original == cracked


if __name__ == "__main__":
    password = "abc"
    result, elapsed_time = grover_crack(
        password, charset=string.ascii_lowercase)
    print(
        f"Cracked Password: {result}, Theoretical Iterations: {elapsed_time:.2f} ms")
