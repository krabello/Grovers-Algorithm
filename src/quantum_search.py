import math

def grover_search_simulation(arr, target):
    """
    Simulates Grover's quantum search algorithm.
    In reality, this would run on a quantum computer.
    Here we just simulate the number of steps it would take.
    """
    n = len(arr)
    # Grover's algorithm takes approximately π/4 * √n iterations
    steps = int(math.pi/4 * math.sqrt(n))
    
    # Find the actual index for demonstration purposes
    target_index = arr.index(target) if target in arr else -1
    
    return target_index, steps