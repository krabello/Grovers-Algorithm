import logging
import random
import string
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from src.classical_crack import brute_force_crack
from src.quantum_crack import grover_crack

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('password_cracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class CrackingResult:
    password: str
    classical_time: float    # in milliseconds
    quantum_time: float     # in milliseconds
    password_length: int
    classical_space: int    # in bytes
    quantum_space: int      # in bytes


class PasswordCracker:
    DEFAULT_LENGTHS = [2, 3, 4, 5]
    OUTPUT_DIR = Path('results')
    PLOT_STYLE = 'default'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.OUTPUT_DIR.mkdir(exist_ok=True)

    def plot_complexity_analysis(self, results: List[CrackingResult]) -> None:
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

            lengths = [result.password_length for result in results]
            classical_times = [result.classical_time for result in results]
            quantum_times = [result.quantum_time for result in results]

            classical_space = [26 ** length for length in lengths]
            quantum_space = [int(np.sqrt(space)) for space in classical_space]

            # Time Complexity Plot
            ax1.plot(
                lengths, classical_times, 'r-o',
                label='Classical (O(N))'
            )
            ax1.plot(
                lengths, quantum_times, 'b-o',
                label='Quantum (O(√N))'
            )
            ax1.set_xlabel('Password Length')
            ax1.set_ylabel('Time (seconds)')
            ax1.set_title('Time Complexity Analysis')
            ax1.legend()
            ax1.grid(True)

            ax2.semilogy(
                lengths, classical_space, 'r-o',
                label='Classical (26^n)'
            )
            ax2.semilogy(
                lengths, quantum_space, 'b-o',
                label='Quantum (√(26^n))'
            )
            ax2.set_xlabel('Password Length')
            ax2.set_ylabel('Search Space Size')
            ax2.set_title('Space Complexity Analysis')
            ax2.legend()
            ax2.grid(True)

            plt.tight_layout()

            plot_path = self.OUTPUT_DIR / 'complexity_analysis.png'
            plt.savefig(plot_path)
            self.logger.info(f"Saved complexity analysis plots to {plot_path}")

            plt.show()

        except Exception as error:
            self.logger.error(
                f"Error generating complexity plots: {str(error)}")

    def generate_password(self, length: int) -> str:
        if not isinstance(length, int) or length < 1:
            raise ValueError("Password length must be a positive integer")
        return ''.join(
            random.choice(string.ascii_lowercase) for _ in range(length)
        )

    def compare_cracking_methods(self) -> List[CrackingResult]:
        results = []

        for length in self.DEFAULT_LENGTHS:
            try:
                password = self.generate_password(length)
                self.logger.info(
                    f"Testing password of length {length}: {password}"
                )

                classical_space = (26 ** length) * length
                quantum_space = int(np.sqrt(classical_space))

                start = time.perf_counter()
                brute_force_crack(password)
                classical_time = (time.perf_counter() - start) * 1000

                start = time.perf_counter()
                grover_crack(password)
                quantum_time = (time.perf_counter() - start) * 1000

                results.append(CrackingResult(
                    password=password,
                    classical_time=classical_time,
                    quantum_time=quantum_time,
                    password_length=length,
                    classical_space=classical_space,
                    quantum_space=quantum_space
                ))

            except Exception as error:
                self.logger.error(
                    f"Error processing length {length}: {str(error)}")
                continue

        return results


def main():
    try:
        cracker = PasswordCracker()
        results = cracker.compare_cracking_methods()

        if not results:
            logger.warning("No results generated")
            return

        print("\nComparison Results:")
        print(
            "Length | Password | Time (ms)     | Time (ms)  | "
            "Space (bytes)  | Space (bytes)"
        )
        print(
            "       |         | Classical      | Quantum    | "
            "Classical      | Quantum     "
        )
        print("-" * 85)

        for result in results:
            print(
                f"{result.password_length:^6} | "
                f"{result.password:^8} | "
                f"{result.classical_time:^13.2f} | "
                f"{result.quantum_time:^10.2f} | "
                f"{result.classical_space:^13,d} | "
                f"{result.quantum_space:^11,d}"
            )

        cracker.plot_complexity_analysis(results)
        logger.info(f"Successfully processed {len(results)} passwords")

    except Exception as error:
        logger.error(f"Application error: {str(error)}")
        raise


if __name__ == "__main__":
    main()
