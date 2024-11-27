import logging
import random
import string
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from src.classical_crack import brute_force_crack
from src.quantum_crack import grover_crack
from src.timing_utils import TimingUtils
from dataclasses import dataclass
import csv


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
        # Same as before
        pass

    def generate_password(self, length: int) -> str:
        # Same as before
        pass

    def compare_cracking_methods(self) -> List[CrackingResult]:
        results = []
        for length in self.DEFAULT_LENGTHS:
            try:
                password = self.generate_password(length)

                classical_space = (26 ** length) * length
                quantum_space = int(np.sqrt(classical_space))

                _, classical_time = brute_force_crack(password)
                _, quantum_time = grover_crack(password)

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
    try:
        cracker = PasswordCracker()
        results = cracker.compare_cracking_methods()
        if not results:
            logging.warning("No results generated")
            return

        cracker.plot_complexity_analysis(results)
        output_file = cracker.OUTPUT_DIR / 'cracking_results.csv'
        cracker.save_results_to_csv(results, output_file)
        logging.info(f"Successfully processed {len(results)} passwords")
    except Exception as error:
        logging.error(f"Application error: {str(error)}")
        raise


if __name__ == "__main__":
    main()
