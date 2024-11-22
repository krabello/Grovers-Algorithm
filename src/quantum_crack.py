# quantum_crack.py

"""
This script simulates a quantum approach to password cracking using Grover's algorithm principles. 
It creates a quantum circuit with an oracle for password matching and uses Qiskit's Aer simulator 
to estimate the quantum search process.
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.primitives import Sampler
import string

def create_oracle_circuit(target_password):
    """Create simple oracle circuit for password matching"""
    n_qubits = len(target_password) * 8
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    circuit = QuantumCircuit(qr, cr)
    
    # Initialize superposition
    circuit.h(qr)
    
    # Convert password to binary
    target_binary = ''.join([format(ord(c), '08b') for c in target_password])
    
    # Add oracle gates
    for i, bit in enumerate(target_binary):
        if bit == '1':
            circuit.x(qr[i])
    
    return circuit

def grover_crack(target_password):
    """Simplified quantum password cracking simulation"""
    # Create circuit with oracle
    # Calls the `create_oracle_circuit` function to generate a quantum circuit
    # containing the oracle for the target password
    circuit = create_oracle_circuit(target_password)
    
    # Add measurement
    # Adds measurement gates to all qubits in the circuit to observe their states after execution
    circuit.measure_all()
    
    # Sets up a quantum simulator backend from Qiskit's Aer provider
    backend = Aer.get_backend('aer_simulator')
    # Submits the circuit to the simulator with 1000 shots (repeated executions)
    job = backend.run(circuit, shots=1000)
    # Retrieves the results of the simulation
    result = job.result()
    # Extracts the measurement results, which are counts of observed bitstrings
    counts = result.get_counts()
    
    # Get most frequent measurement
    # Identifies the most frequently observed bitstring from the measurement results
    # `max` selects the bitstring with the highest count
    measured_bits = max(counts.items(), key=lambda x: x[1])[0]
    
    # Convert bits back to characters
    # Initializes an empty string to store the decoded characters
    measured_chars = ''
    # Loops through the measured bitstring 8 bits at a time (1 byte = 1 character)
    for i in range(0, len(measured_bits), 8):
        # Extracts an 8-bit segment from the measured bitstring
        char_bits = measured_bits[i:i+8]
        # Converts the binary string to an integer, then to a character using `chr`
        measured_chars += chr(int(char_bits, 2))
    
    # Calculate theoretical iterations
    # Calculates the size of the search space: number of possible passwords
    # (N = Character Set^Password Length)
    N = len(string.ascii_lowercase) ** len(target_password)
    # Calculates the theoretical number of iterations Grover's algorithm would require
    # (iterations = pi / 4 times sqrt{N})
    iterations = int(np.pi/4 * np.sqrt(N))
    
    # Return the cracked password and the theoretical number of iterations
    return measured_chars, iterations


def verify_result(original, cracked):
    """Verify if the cracked password matches original"""
    return original == cracked
