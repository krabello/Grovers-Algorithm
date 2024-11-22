import random
import matplotlib.pyplot as plt
from classical_search import linear_search
from quantum_search import grover_search_simulation

def compare_algorithms(sizes):
    """Compare classical and quantum search performance."""
    classical_steps = []
    quantum_steps = []
    
    for size in sizes:
        # Create a random array of given size
        arr = list(range(size))
        random.shuffle(arr)
        target = random.choice(arr)
        
        # Run classical search
        _, c_steps = linear_search(arr, target)
        classical_steps.append(c_steps)
        
        # Run quantum search simulation
        _, q_steps = grover_search_simulation(arr, target)
        quantum_steps.append(q_steps)
    
    return classical_steps, quantum_steps

def plot_results(sizes, classical_steps, quantum_steps):
    """Plot the comparison results."""
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, classical_steps, 'r-', label='Classical Search (O(n))')
    plt.plot(sizes, quantum_steps, 'b-', label='Quantum Search (O(√n))')
    plt.xlabel('Input Size')
    plt.ylabel('Number of Steps')
    plt.title('Classical vs Quantum Search Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Test with different array sizes
    sizes = [10, 100, 1000, 10000, 100000]
    classical_steps, quantum_steps = compare_algorithms(sizes)
    
    # Print results
    print("\nComparison Results:")
    print("------------------")
    print("Array Size | Classical Steps | Quantum Steps")
    print("-" * 45)
    for i in range(len(sizes)):
        print(f"{sizes[i]:^10} | {classical_steps[i]:^15} | {quantum_steps[i]:^12}")
    
    # Plot results
    plot_results(sizes, classical_steps, quantum_steps)

if __name__ == "__main__":
    main()