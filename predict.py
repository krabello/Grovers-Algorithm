import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ComplexityPrediction:
    password_length: int
    classical_time: float  # milliseconds
    quantum_time: float   # milliseconds
    classical_space: int  # bytes
    quantum_space: int    # bytes


class ComplexityPredictor:
    # default for ASCII letters, digits, punctuation
    def __init__(self, charset_size: int = 94):
        self.charset_size = charset_size
        # Constants from experimental data for length 2
        self.classical_base_time = 0.45  # ms for length 2
        self.quantum_base_time = 69.84   # ms for length 2
        self.quantum_overhead = 10       # ms overhead per character

    def predict_classical_time(self, length: int) -> float:
        """
        Predict classical brute force time based on O(N) complexity
        where N is charset_size^length
        """
        # Calculate scaling factor from base case (length 2)
        scaling_factor = self.classical_base_time / (self.charset_size ** 2)
        predicted_time = scaling_factor * (self.charset_size ** length)
        return predicted_time

    def predict_quantum_time(self, length: int) -> float:
        """
        Predict quantum time based on O(√N) complexity plus overhead
        """
        # Calculate base quantum scaling factor from length 2 case
        base_search_space = self.charset_size ** length
        grover_iterations = int(np.sqrt(base_search_space))

        # Scale based on experimental data, adding per-character overhead
        scaling_factor = (self.quantum_base_time -
                          self.quantum_overhead * 2) / np.sqrt(self.charset_size ** 2)
        predicted_time = (scaling_factor * np.sqrt(base_search_space)
                          ) + (self.quantum_overhead * length)

        return predicted_time

    def predict_classical_space(self, length: int) -> int:
        """
        Predict classical space requirements based on search space size
        """
        return length * self.charset_size ** length

    def predict_quantum_space(self, length: int) -> int:
        """
        Predict quantum space requirements based on quantum register size
        7 qubits per character plus classical overhead
        """
        qubits_per_char = 7
        quantum_register_size = length * qubits_per_char
        # Space grows with quantum register size
        # Additional space for classical control
        return int(2 ** quantum_register_size + length * 32)

    def predict_complexity(self, length: int) -> ComplexityPrediction:
        """Generate complete complexity prediction for a given password length"""
        return ComplexityPrediction(
            password_length=length,
            classical_time=self.predict_classical_time(length),
            quantum_time=self.predict_quantum_time(length),
            classical_space=self.predict_classical_space(length),
            quantum_space=self.predict_quantum_space(length)
        )

    def predict_range(self, min_length: int, max_length: int) -> List[ComplexityPrediction]:
        """Generate predictions for a range of password lengths"""
        return [self.predict_complexity(length)
                for length in range(min_length, max_length + 1)]

    def find_crossover_point(self) -> Tuple[int, float]:
        """Find the password length where quantum becomes faster than classical"""
        length = 1
        while length <= 20:  # Safety limit
            pred = self.predict_complexity(length)
            if pred.quantum_time < pred.classical_time:
                return length, pred.quantum_time
            length += 1
        return -1, -1


def main():
    predictor = ComplexityPredictor()

    # Generate predictions for lengths 2-8
    predictions = predictor.predict_range(2, 8)

    print("\nComplexity Predictions:")
    print("-" * 80)
    print(f"{'Length':^8} | {'Classical Time (ms)':^20} | {'Quantum Time (ms)':^20} | {'Space Ratio':^15}")
    print("-" * 80)

    for pred in predictions:
        space_ratio = pred.quantum_space / pred.classical_space
        print(f"{pred.password_length:^8} | {pred.classical_time:^20.2f} | "
              f"{pred.quantum_time:^20.2f} | {space_ratio:^15.2e}")

    # Find crossover point
    crossover_length, crossover_time = predictor.find_crossover_point()
    if crossover_length > 0:
        print(f"\nQuantum advantage begins at length {crossover_length} "
              f"(Time: {crossover_time:.2f}ms)")


if __name__ == "__main__":
    main()
