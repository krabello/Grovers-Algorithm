import logging
import random
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from src.classical_crack import brute_force_crack
from src.quantum_crack import GroverCrack
from src.timing_utils import TimingUtils
from shared_constants import CHARSET
from dataclasses import dataclass
import csv
import time

ENABLE_CLASSICAL = True


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
        lengths = [r.password_length for r in results]
        classical_times = [r.classical_time for r in results]
        quantum_times = [r.quantum_time for r in results]
        classical_space = [r.classical_space for r in results]
        quantum_space = [r.quantum_space for r in results]

        plt.figure(figsize=(10, 5))
        if ENABLE_CLASSICAL:
            plt.plot(lengths, classical_times, 'r-o',
                     label='Classical Time (ms)')
        plt.plot(lengths, quantum_times, 'b-o', label='Quantum Time (ms)')
        plt.xlabel('Password Length')
        plt.ylabel('Time (ms)')
        plt.title('Time Complexity Analysis')
        plt.legend()
        plt.grid(True)
        plt.savefig(self.OUTPUT_DIR / 'time_complexity.png')
        plt.show()

        plt.figure(figsize=(10, 5))
        if ENABLE_CLASSICAL:
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
        return ''.join(random.choice(CHARSET) for _ in range(length))

    def compare_cracking_methods(self) -> List[CrackingResult]:
        results = []
        for length in self.DEFAULT_LENGTHS:
            try:
                logging.info(
                    f"Starting processing for password length: {length}")
                password = self.generate_password(length)

                try:
                    if length <= 6:  # We set a practical limit for computation
                        classical_space = len(CHARSET) ** length * length
                        quantum_space = int(np.sqrt(classical_space))
                    else:
                        classical_space = "Overflow"
                        quantum_space = "Overflow"
                except OverflowError as e:
                    logging.error(f"Overflow error for length {length}: {e}")
                    classical_space = "Overflow"
                    quantum_space = "Overflow"
                except Exception as e:
                    logging.error(f"Unexpected error for length {length}: {e}")
                    classical_space = "Error"
                    quantum_space = "Error"

                if ENABLE_CLASSICAL:
                    _, classical_time = brute_force_crack(password)
                else:
                    classical_time = 0

                grover_instance = GroverCrack()
                start_time = time.perf_counter()
                grover_instance.crack_password(password)
                quantum_time = (time.perf_counter() -
                                start_time) * 1000

                results.append(CrackingResult(
                    password=password,
                    classical_time=classical_time,
                    quantum_time=quantum_time,
                    password_length=length,
                    classical_space=classical_space if ENABLE_CLASSICAL else 0,
                    quantum_space=quantum_space
                ))
            except Exception as error:
                logging.error(
                    f"Error processing length {length}: {str(error)}")
                continue

        return results

    def save_results_to_csv(self, results: List[CrackingResult], file_path: Path) -> None:
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Password Length', 'Password', 'Classical Time (ms)',
                          'Quantum Time (ms)', 'Classical Space (bytes)', 'Quantum Space (bytes)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow({
                    'Password Length': result.password_length,
                    'Password': result.password,
                    'Classical Time (ms)': f"{result.classical_time:.2f}" if isinstance(result.classical_time, (float, int)) else result.classical_time,
                    'Quantum Time (ms)': f"{result.quantum_time:.2f}" if isinstance(result.quantum_time, (float, int)) else result.quantum_time,
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
