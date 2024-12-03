import logging
import random
import string
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from src.classical_crack import brute_force_crack
from src.quantum_crack import GroverCrack
from src.timing_utils import TimingUtils
from dataclasses import dataclass
import csv
import time


@dataclass
class CrackingResult:
    password: str
    classical_time: float
    quantum_time: float
    password_length: int
    classical_space: int
    quantum_space: int


class PasswordCracker:
    DEFAULT_LENGTHS = [2, 3, 4, 5]
    OUTPUT_DIR = Path('results')

    def __init__(self):
        self.OUTPUT_DIR.mkdir(exist_ok=True)

    def plot_complexity_analysis(self, results: List[CrackingResult]) -> None:
        """Generate time and space complexity plots."""
        lengths = [r.password_length for r in results]
        classical_times = [r.classical_time for r in results]
        quantum_times = [r.quantum_time for r in results]
        classical_space = [r.classical_space for r in results]
        quantum_space = [r.quantum_space for r in results]

        # Time Complexity Plot
        plt.figure(figsize=(10, 5))
        plt.plot(lengths, classical_times, 'r-o', label='Classical Time (ms)')
        plt.plot(lengths, quantum_times, 'b-o', label='Quantum Time (ms)')
        plt.xlabel('Password Length')
        plt.ylabel('Time (ms)')
        plt.title('Time Complexity Analysis')
        plt.legend()
        plt.grid(True)
        plt.savefig(self.OUTPUT_DIR / 'time_complexity.png')
        plt.show()

        # Space Complexity Plot
        plt.figure(figsize=(10, 5))
        plt.plot(lengths, classical_space, 'r-o',
                 label='Classical Space (bytes)')
        plt.plot(lengths, quantum_space, 'b-o', label='Quantum Space (bytes)')
        plt.xlabel('Password Length')
        plt.ylabel('Space (bytes)')
        plt.title('Space Complexity Analysis')
        plt.legend()
        plt.grid(True)
        plt.savefig(self.OUTPUT_DIR / 'space_complexity.png')
        plt.show()

    def generate_password(self, length: int) -> str:
        """Generate a random password of the length given."""
        charset = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(charset) for _ in range(length))

    def compare_cracking_methods(self) -> List[CrackingResult]:
        """Compare classical and quantum cracking."""
        results = []
        for length in self.DEFAULT_LENGTHS:
            try:
                password = self.generate_password(length)

                # Space Complexity
                classical_space = (
                    len(string.ascii_letters + string.digits + string.punctuation) ** length) * length
                quantum_space = int(np.sqrt(classical_space))

                # Classical Cracking
                _, classical_time = brute_force_crack(password)

                # Quantum Cracking
                grover_instance = GroverCrack()
                start_time = time.perf_counter()  # Start timer
                quantum_result = grover_instance.crack_password(password)
                quantum_time = (time.perf_counter() -
                                start_time) * 1000  # Convert to ms

                # Log measured time
                logging.info(
                    f"Quantum time for length {length}: {quantum_time:.2f} ms")

                # Append results
                results.append(CrackingResult(
                    password=password,
                    classical_time=classical_time,
                    quantum_time=quantum_time,
                    password_length=length,
                    classical_space=classical_space,
                    quantum_space=quantum_space
                ))

            except Exception as error:
                logging.error(
                    f"Error processing length {length}: {str(error)}")
                continue

        return results

    def save_results_to_csv(self, results: List[CrackingResult], file_path: Path) -> None:
        """Save results to a CSV."""
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Password Length', 'Password', 'Classical Time (ms)',
                          'Quantum Time (ms)', 'Classical Space (bytes)', 'Quantum Space (bytes)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow({
                    'Password Length': result.password_length,
                    'Password': result.password,
                    'Classical Time (ms)': f"{result.classical_time:.2f}",
                    'Quantum Time (ms)': f"{result.quantum_time:.2f}",
                    'Classical Space (bytes)': result.classical_space,
                    'Quantum Space (bytes)': result.quantum_space,
                })
        logging.info(f"Results saved to {file_path}")


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        cracker = PasswordCracker()
        results = cracker.compare_cracking_methods()
        if not results:
            logging.warning("No results generated")
            return

        # Generate plots and save results
        cracker.plot_complexity_analysis(results)
        output_file = cracker.OUTPUT_DIR / 'cracking_results.csv'
        cracker.save_results_to_csv(results, output_file)
        logging.info(f"Successfully processed {len(results)} passwords")
    except Exception as error:
        logging.error(f"Application error: {str(error)}")
        raise


if __name__ == "__main__":
    main()
