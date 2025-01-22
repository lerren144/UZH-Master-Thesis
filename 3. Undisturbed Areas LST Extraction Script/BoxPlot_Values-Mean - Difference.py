import matplotlib.pyplot as plt

# Updated data for box plots
updated_data = {
    "Regress Combination": {
        "Q1": -0.04884285666048527,
        "Median": 0.4309965968132019,
        "Mean": 0.46667900681495667,
        "Q3": 1.0885316133499146
    },
    "Mean Average 1": {
        "Q1": -0.232818603515625,
        "Median": 0.5009307861328125,
        "Mean": 0.5994868278503418,
        "Q3": 1.507354736328125
    },
    "Mean Average 2": {
        "Q1": -0.0501861572265625,
        "Median": 0.410247802734375,
        "Mean": 0.4146546721458435,
        "Q3": 0.9768829345703125
    }
}

# Prepare box plot data (Q1, Median, Mean, Q3)
box_data_no_whiskers = [
    [info["Q1"], info["Median"], info["Mean"], info["Q3"]] for info in updated_data.values()
]

# Labels for the plots
labels_no_whiskers = list(updated_data.keys())

# Create the box plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create a custom box plot without whiskers
for i, (label, values) in enumerate(zip(labels_no_whiskers, box_data_no_whiskers), start=1):
    # Draw a smaller box for Q1 to Q3
    ax.add_patch(plt.Rectangle((i - 0.2, values[0]), 0.4, values[3] - values[0], fill=None, edgecolor='black'))
    # Draw a line for the median
    ax.plot([i - 0.2, i + 0.2], [values[1], values[1]], color='black', lw=2)
    # Plot the mean as a red dot
    ax.plot(i, values[2], 'ro')

    # Annotate values outside the box
    for j, value in enumerate(values):
        ax.text(i + 0.2, value, f'{value:.2f}', ha='left', va='center', fontsize=9)

# Configure plot
ax.set_xticks(range(1, len(labels_no_whiskers) + 1))
ax.set_xticklabels(labels_no_whiskers, rotation=15)
ax.set_title('Box Plot Without Whiskers (Labels Outside, No Vertical Offset)', fontsize=14)
ax.set_ylabel('Values', fontsize=12)

# Save the plot
plt.tight_layout()
plt.savefig("box_plot_no_whiskers_labels_outside_no_offset.png", dpi=300)  # Save at 300 DPI
plt.show()
