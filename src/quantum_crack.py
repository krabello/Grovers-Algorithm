# quantum_crack.py
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
    circuit = create_oracle_circuit(target_password)
    
    # Add measurement
    circuit.measure_all()
    
    # Run on simulator
    backend = Aer.get_backend('aer_simulator')
    job = backend.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    # Get most frequent measurement
    measured_bits = max(counts.items(), key=lambda x: x[1])[0]
    
    # Convert bits back to characters
    measured_chars = ''
    for i in range(0, len(measured_bits), 8):
        char_bits = measured_bits[i:i+8]
        measured_chars += chr(int(char_bits, 2))
    
    # Calculate theoretical iterations
    N = len(string.ascii_lowercase) ** len(target_password)
    iterations = int(np.pi/4 * np.sqrt(N))
    
    return measured_chars, iterations

def verify_result(original, cracked):
    """Verify if the cracked password matches original"""
    return original == cracked