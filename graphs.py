import matplotlib.pyplot as plt
import numpy as np


def create_visualizations():
    # Data (converting times from ms to ns)
    lengths = [2, 3, 4, 5, 6, 7, 8]
    classical_times = [
        0.45 * 1e6,           # 450,000 ns
        42.30 * 1e6,         # 42,300,000 ns
        3976.20 * 1e6,       # 3,976,200,000 ns
        373762.80 * 1e6,     # 373,762,800,000 ns
        35133703.20 * 1e6,   # 35,133,703,200,000 ns
        3302568100.80 * 1e6,  # 3,302,568,100,800,000 ns
        310441401475.20 * 1e6  # 310,441,401,475,200,000 ns
    ]
    quantum_times = [
        69.84 * 1e6,         # 69,840,000 ns
        513.22 * 1e6,        # 513,220,000 ns
        4724.96 * 1e6,       # 4,724,960,000 ns
        45472.37 * 1e6,      # 45,472,370,000 ns
        440446.24 * 1e6,     # 440,446,240,000 ns
        4269773.01 * 1e6,    # 4,269,773,010,000 ns
        41396386.56 * 1e6    # 41,396,386,560,000 ns
    ]

    speedup_ratios = [c/q for c, q in zip(classical_times, quantum_times)]

    classical_space = [17672, 2491752, 312299584, 36695201120,
                       3449148905280, 324219697095680, 30476551526993900]
    quantum_space = [132, 1578, 17672, 191559, 2097152, 22020096, 231211008]

    transitions = ["2→3", "3→4", "4→5", "5→6", "6→7", "7→8"]
    classical_growth = [94] * 6
    quantum_growth = [7.35, 9.21, 9.62, 9.69, 9.69, 9.70]

    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
    fig.suptitle('Password Cracking Complexity Analysis', fontsize=16, y=0.95)

    # 1. Time Complexity
    ax1.plot(lengths, classical_times, 'b-o',
             label='Classical', linewidth=2, markersize=8)
    ax1.plot(lengths, quantum_times, 'g-o',
             label='Quantum', linewidth=2, markersize=8)
    ax1.set_yscale('log')
    ax1.set_xlabel('Password Length')
    ax1.set_ylabel('Time (ns)')
    ax1.set_title('Time Complexity Comparison')
    ax1.grid(True, which="both", ls="-", alpha=0.2)
    ax1.legend()
    # Format y-axis labels in scientific notation
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    # 2. Speedup Ratio
    ax2.plot(lengths, speedup_ratios, 'g-o', linewidth=2, markersize=8)
    ax2.set_yscale('log')
    ax2.set_xlabel('Password Length')
    ax2.set_ylabel('Speedup Ratio (Classical/Quantum)')
    ax2.set_title('Speedup Ratio')
    ax2.grid(True, which="both", ls="-", alpha=0.2)

    # 3. Space Complexity
    ax3.plot(lengths, classical_space, 'b-o',
             label='Classical', linewidth=2, markersize=8)
    ax3.plot(lengths, quantum_space, 'g-o',
             label='Quantum', linewidth=2, markersize=8)
    ax3.set_yscale('log')
    ax3.set_xlabel('Password Length')
    ax3.set_ylabel('Space (bytes)')
    ax3.set_title('Space Complexity Comparison')
    ax3.grid(True, which="both", ls="-", alpha=0.2)
    ax3.legend()

    # 4. Growth Rate
    x = np.arange(len(transitions))
    width = 0.35
    ax4.bar(x - width/2, classical_growth, width,
            label='Classical', color='blue', alpha=0.7)
    ax4.bar(x + width/2, quantum_growth, width,
            label='Quantum', color='green', alpha=0.7)
    ax4.set_ylabel('Growth Factor')
    ax4.set_title('Growth Rate Comparison')
    ax4.set_xticks(x)
    ax4.set_xticklabels(transitions)
    ax4.legend()
    ax4.grid(True, alpha=0.2)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('complexity_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    create_visualizations()
