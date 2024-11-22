# password_cracker.py

import random
import string
import time
import logging
from typing import List
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from classical_crack import brute_force_crack
from quantum_crack import grover_crack

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
    """Data class for password cracking results"""
    password: str
    classical_time: float    # in milliseconds
    quantum_time: float     # in milliseconds
    password_length: int
    classical_space: int    # in bytes
    quantum_space: int      # in bytes

class PasswordCracker:
    """Enterprise password cracking comparison tool"""
    DEFAULT_LENGTHS = [2, 3, 4, 5, 6, 7]
    OUTPUT_DIR = Path('results')
    PLOT_STYLE = 'default'
    
    def __init__(self):
        """Initialize password cracker"""
        self.logger = logging.getLogger(__name__)
        self.OUTPUT_DIR.mkdir(exist_ok=True)

    def plot_complexity_analysis(self, results: List[CrackingResult]) -> None:
        """Generate time and space complexity plots"""
        try:
            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Extract data
            lengths = [r.password_length for r in results]
            classical_times = [r.classical_time for r in results]
            quantum_times = [r.quantum_time for r in results]
            
            # Calculate space complexities
            classical_space = [26 ** length for length in lengths]
            quantum_space = [int(np.sqrt(space)) for space in classical_space]
            
            # Time Complexity Plot
            ax1.plot(lengths, classical_times, 'r-o', label='Classical (O(N))')
            ax1.plot(lengths, quantum_times, 'b-o', label='Quantum (O(√N))')
            ax1.set_xlabel('Password Length')
            ax1.set_ylabel('Time (seconds)')
            ax1.set_title('Time Complexity Analysis')
            ax1.legend()
            ax1.grid(True)
            
            # Space Complexity Plot
            ax2.semilogy(lengths, classical_space, 'r-o', label='Classical (26^n)')
            ax2.semilogy(lengths, quantum_space, 'b-o', label='Quantum (√(26^n))')
            ax2.set_xlabel('Password Length')
            ax2.set_ylabel('Search Space Size')
            ax2.set_title('Space Complexity Analysis')
            ax2.legend()
            ax2.grid(True)
            
            plt.tight_layout()
            
            # Save plot
            plot_path = self.OUTPUT_DIR / 'complexity_analysis.png'
            plt.savefig(plot_path)
            logger.info(f"Saved complexity analysis plots to {plot_path}")
            
            plt.show()
            
        except Exception as e:
            logger.error(f"Error generating complexity plots: {str(e)}")

    def generate_password(self, length: int) -> str:
        """Generate a random password of given length"""
        if not isinstance(length, int) or length < 1:
            raise ValueError("Password length must be positive integer")
        return ''.join(random.choice(string.ascii_lowercase) 
                      for _ in range(length))

    def compare_cracking_methods(self) -> List[CrackingResult]:
        results = []
        
        for length in self.DEFAULT_LENGTHS:
            try:
                password = self.generate_password(length)
                logger.info(f"Testing password of length {length}: {password}")
                
                # Calculate space complexities (1 byte per character)
                classical_space = (26 ** length) * length  # each guess is length bytes
                quantum_space = int(np.sqrt(classical_space))
                
                # Measure classical approach (convert to ms)
                start = time.perf_counter()
                brute_force_crack(password)
                classical_time = (time.perf_counter() - start) * 1000
                
                # Measure quantum simulation (convert to ms)
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
                
            except Exception as e:
                logger.error(f"Error processing length {length}: {str(e)}")
                continue
                
        return results

def main():
    try:
        cracker = PasswordCracker()
        results = cracker.compare_cracking_methods()
        
        if not results:
            logger.warning("No results generated from password cracking")
            return
            
        # Print results
        print("\nComparison Results:")
        print("Length | Password | Time (ms)     | Time (ms)  | Space (bytes)  | Space (bytes)")
        print("       |         | Classical      | Quantum    | Classical      | Quantum     ")
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
        
        # Generate complexity plots
        cracker.plot_complexity_analysis(results)
            
        # Log actual count of processed passwords
        logger.info(f"Successfully processed {len(results)} passwords")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()