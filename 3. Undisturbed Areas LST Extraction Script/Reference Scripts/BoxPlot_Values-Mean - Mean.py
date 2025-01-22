import matplotlib.pyplot as plt

# Updated data for box plots
updated_data = {
    "Regress Combination": {
        "Q1": 271.518798828125,
        "Median": 290.6324462890625,
        "Mean": 286.2991943359375,
        "Q3": 303.28948974609375
    },
    "Average (Day)": {
        "Q1": 274.6114501953125,
        "Median": 296.5390930175781,
        "Mean": 292.1003112792969,
        "Q3": 308.85888671875
    },
    "Average (Night)": {
        "Q1": 262.0402526855469,
        "Median": 279.5489196777344,
        "Mean": 275.609375,
        "Q3": 291.57196044921875
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
ax.set_title('Box Plot Without Whiskers (Updated Values)', fontsize=14)
ax.set_ylabel('Values (Temperature)', fontsize=12)

# Save the plot
plt.tight_layout()
plt.savefig("box_plot_updated_values.png", dpi=300)  # Save at 300 DPI
plt.show()
