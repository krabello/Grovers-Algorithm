# Classical calculation for length 15
base_classical = 310441401475.20  # ms at length 8
classical_growth = 94 ** 7        # growth for 7 more characters
classical_15 = base_classical * classical_growth

# Quantum calculation for length 15
base_quantum = 41396386.56       # ms at length 8
quantum_growth = 9.7 ** 7        # growth for 7 more characters
quantum_15 = base_quantum * quantum_growth

# Convert to more readable units
classical_years = classical_15 / (1000 * 60 * 60 * 24 * 365)
quantum_days = quantum_15 / (1000 * 60 * 60 * 24)

print(f"Classical time for 15 characters: {classical_years:.2e} years")
print(f"Quantum time for 15 characters: {quantum_days:.2f} days")
