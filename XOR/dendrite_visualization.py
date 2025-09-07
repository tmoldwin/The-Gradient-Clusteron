import matplotlib.pyplot as plt
import numpy as np

# Create figure with 2x3 subplots
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# Remove all axes, ticks, and labels for minimalism
for ax in axes.flat:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

# Row 1: Close synapses
# Panel 1: Close, both red
ax1 = axes[0, 0]
ax1.plot([2, 8], [5, 5], 'k-', linewidth=2)
ax1.plot([4, 4], [5, 3], 'k-', linewidth=1.5)
ax1.plot(4, 3, 'ro', markersize=8)
ax1.plot([6, 6], [5, 7], 'k-', linewidth=1.5)
ax1.plot(6, 7, 'ro', markersize=8)

# Panel 2: Close, both blue
ax2 = axes[0, 1]
ax2.plot([2, 8], [5, 5], 'k-', linewidth=2)
ax2.plot([4, 4], [5, 3], 'k-', linewidth=1.5)
ax2.plot(4, 3, 'bo', markersize=8)
ax2.plot([6, 6], [5, 7], 'k-', linewidth=1.5)
ax2.plot(6, 7, 'bo', markersize=8)

# Panel 3: Close, red and blue
ax3 = axes[0, 2]
ax3.plot([2, 8], [5, 5], 'k-', linewidth=2)
ax3.plot([4, 4], [5, 3], 'k-', linewidth=1.5)
ax3.plot(4, 3, 'ro', markersize=8)
ax3.plot([6, 6], [5, 7], 'k-', linewidth=1.5)
ax3.plot(6, 7, 'bo', markersize=8)

# Row 2: Far synapses
# Panel 4: Far, both red
ax4 = axes[1, 0]
ax4.plot([2, 8], [5, 5], 'k-', linewidth=2)
ax4.plot([3, 3], [5, 3], 'k-', linewidth=1.5)
ax4.plot(3, 3, 'ro', markersize=8)
ax4.plot([7, 7], [5, 7], 'k-', linewidth=1.5)
ax4.plot(7, 7, 'ro', markersize=8)

# Panel 5: Far, both blue
ax5 = axes[1, 1]
ax5.plot([2, 8], [5, 5], 'k-', linewidth=2)
ax5.plot([3, 3], [5, 3], 'k-', linewidth=1.5)
ax5.plot(3, 3, 'bo', markersize=8)
ax5.plot([7, 7], [5, 7], 'k-', linewidth=1.5)
ax5.plot(7, 7, 'bo', markersize=8)

# Panel 6: Far, red and blue
ax6 = axes[1, 2]
ax6.plot([2, 8], [5, 5], 'k-', linewidth=2)
ax6.plot([3, 3], [5, 3], 'k-', linewidth=1.5)
ax6.plot(3, 3, 'ro', markersize=8)
ax6.plot([7, 7], [5, 7], 'k-', linewidth=1.5)
ax6.plot(7, 7, 'bo', markersize=8)

# Adjust layout and save
plt.tight_layout()
plt.savefig('XOR/dendrite_visualization.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.show()
