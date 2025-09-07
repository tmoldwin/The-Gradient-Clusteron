import matplotlib.pyplot as plt
import numpy as np

# Create figure with 2x3 subplots
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# Set up axes with proper facecolor support
for ax in axes.flat:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    # Turn axes on but hide lines, ticks, and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Row 1: Close synapses
# Panel 1: Close, both red - WHITE ON BLACK
ax1 = axes[0, 0]
ax1.set_facecolor('black')  # Set black background
ax1.plot([2, 8], [5, 5], 'w-', linewidth=2)  # White dendrite
ax1.plot([4, 4], [5, 3], 'w-', linewidth=1.5)  # White branch
ax1.plot(4, 3, 'ro', markersize=8)  # Red synapse
ax1.plot([6, 6], [5, 7], 'w-', linewidth=1.5)  # White branch
ax1.plot(6, 7, 'ro', markersize=8)  # Red synapse

# Panel 2: Close, both blue - BLACK ON WHITE
ax2 = axes[0, 1]
ax2.set_facecolor('white')  # Set white background
ax2.plot([2, 8], [5, 5], 'k-', linewidth=2)  # Black dendrite
ax2.plot([4, 4], [5, 3], 'k-', linewidth=1.5)  # Black branch
ax2.plot(4, 3, 'bo', markersize=8)  # Blue synapse
ax2.plot([6, 6], [5, 7], 'k-', linewidth=1.5)  # Black branch
ax2.plot(6, 7, 'bo', markersize=8)  # Blue synapse

# Panel 3: Close, red and blue - WHITE ON BLACK
ax3 = axes[0, 2]
ax3.set_facecolor('black')  # Set black background
ax3.plot([2, 8], [5, 5], 'w-', linewidth=2)  # White dendrite
ax3.plot([4, 4], [5, 3], 'w-', linewidth=1.5)  # White branch
ax3.plot(4, 3, 'ro', markersize=8)  # Red synapse
ax3.plot([6, 6], [5, 7], 'w-', linewidth=1.5)  # White branch
ax3.plot(6, 7, 'bo', markersize=8)  # Blue synapse

# Row 2: Far synapses
# Panel 4: Far, both red - BLACK ON WHITE
ax4 = axes[1, 0]
ax4.set_facecolor('white')  # Set white background
ax4.plot([2, 8], [5, 5], 'k-', linewidth=2)  # Black dendrite
ax4.plot([3, 3], [5, 3], 'k-', linewidth=1.5)  # Black branch
ax4.plot(3, 3, 'ro', markersize=8)  # Red synapse
ax4.plot([7, 7], [5, 7], 'k-', linewidth=1.5)  # Black branch
ax4.plot(7, 7, 'ro', markersize=8)  # Red synapse

# Panel 5: Far, both blue - WHITE ON BLACK
ax5 = axes[1, 1]
ax5.set_facecolor('black')  # Set black background
ax5.plot([2, 8], [5, 5], 'w-', linewidth=2)  # White dendrite
ax5.plot([3, 3], [5, 3], 'w-', linewidth=1.5)  # White branch
ax5.plot(3, 3, 'bo', markersize=8)  # Blue synapse
ax5.plot([7, 7], [5, 7], 'w-', linewidth=1.5)  # White branch
ax5.plot(7, 7, 'bo', markersize=8)  # Blue synapse

# Panel 6: Far, red and blue - BLACK ON WHITE
ax6 = axes[1, 2]
ax6.set_facecolor('white')  # Set white background
ax6.plot([2, 8], [5, 5], 'k-', linewidth=2)  # Black dendrite
ax6.plot([3, 3], [5, 3], 'k-', linewidth=1.5)  # Black branch
ax6.plot(3, 3, 'ro', markersize=8)  # Red synapse
ax6.plot([7, 7], [5, 7], 'k-', linewidth=1.5)  # Black branch
ax6.plot(7, 7, 'bo', markersize=8)  # Blue synapse

# Adjust layout and save
plt.tight_layout()
plt.savefig('dendrite_visualization.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.show()
