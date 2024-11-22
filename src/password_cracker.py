# password_cracker.py
import random
import string
import time
import matplotlib.pyplot as plt
from classical_crack import brute_force_crack
from quantum_crack import grover_crack

def generate_password(length):
    """Generate a random password of given length"""
    return ''.join(random.choice(string.ascii_lowercase) 
                  for _ in range(length))

def compare_cracking_methods(password_lengths):
    classical_times = []
    quantum_times = []
    passwords = []  # Track generated passwords
    
    for length in password_lengths:
        password = generate_password(length)
        passwords.append(password)  # Store password
        
        # Measure classical approach
        start = time.time()
        brute_force_crack(password)
        classical_time = time.time() - start
        classical_times.append(classical_time)
        
        # Measure quantum simulation
        start = time.time()
        grover_crack(password)
        quantum_time = time.time() - start
        quantum_times.append(quantum_time)
        
    return classical_times, quantum_times, passwords  # Return passwords

def main():
    password_lengths = [2, 3, 4, 5, 6]
    classical_times, quantum_times, passwords = compare_cracking_methods(
        password_lengths)
    
    # Print results with passwords
    print("\nComparison Results:")
    print("Password Length | Password | Classical Time | Quantum Time")
    print("-" * 65)
    for i, length in enumerate(password_lengths):
        print(f"{length:^14} | {passwords[i]:^8} | {classical_times[i]:^13.4f} | "
              f"{quantum_times[i]:^11.4f}")
    
    # Plot results
    plot_results(password_lengths, classical_times, quantum_times)

# In password_cracker.py
def plot_results(lengths, classical_times, quantum_times):
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, classical_times, 'r-', 
             label='Classical Brute-Force (O(N))')
    plt.plot(lengths, quantum_times, 'b-', 
             label='Quantum Grover (O(√N))')
    plt.xlabel('Password Length')
    plt.ylabel('Time (seconds)')
    plt.title('Password Cracking: Classical vs Quantum Approaches')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    password_lengths = [2, 3, 4, 5, 6]
    # Update unpacking to include passwords
    classical_times, quantum_times, passwords = compare_cracking_methods(
        password_lengths)
    
    # Print results with passwords
    print("\nComparison Results:")
    print("Password Length | Password | Classical Time | Quantum Time")
    print("-" * 65)
    for i, length in enumerate(password_lengths):
        print(f"{length:^14} | {passwords[i]:^8} | {classical_times[i]:^13.4f} | "
              f"{quantum_times[i]:^11.4f}")
    
    # Plot results
    plot_results(password_lengths, classical_times, quantum_times)

if __name__ == "__main__":
    main()