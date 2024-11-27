# Password Cracker: Classical vs. Quantum

This project provides a comparative analysis of password cracking techniques using classical brute-force methods and quantum-inspired Grover's algorithm principles. It includes tools to simulate both approaches, analyze time and space complexity, and generate visualizations for enterprise-level applications.

---

## Features

- **Classical Brute-Force Simulation**:
  - Systematically generates all possible password combinations.
  - Demonstrates exponential time complexity for longer passwords.

- **Quantum Grover's Algorithm Simulation**:
  - Uses Qiskit's Aer simulator to estimate quantum search processes.
  - Provides theoretical quadratic speedup for password searches.

- **Time and Space Complexity Analysis**:
  - Measures time and space usage for both methods.
  - Generates visualizations comparing classical and quantum approaches.

- **Enterprise Logging**:
  - Logs results and errors to both a console and a file (`password_cracker.log`).

---

## File Structure

- `main.py`: Main script to simulate password cracking and compare methods.
- `classical_crack.py`: Implements the classical brute-force cracking approach.
- `quantum_crack.py`: Simulates quantum cracking using Grover's algorithm principles.

---

## Dependencies

To run the project, install the following dependencies:

- cd into project directory

```bash
    python3.10 -m venv venv
```

```bash
    source venv/bin/activate
```

```bash
    pip install -r requirements.txt
```

```bash
    python main.py
```
