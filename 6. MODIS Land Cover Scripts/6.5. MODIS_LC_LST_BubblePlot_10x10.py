import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import textwrap
import numpy as np

# Define the input file paths
transition_matrix_file = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_MODIS_transition_matrix_10x10_Final.xlsx'
lst_temperature_file = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_LST_Results\MOYD21A1DN_transition_matrix_LCType1_RegressCombination_Adjusted - LinearHarmonized.csv'

# Load the data
df = pd.read_excel(transition_matrix_file, index_col=0)
lst_temperature = pd.read_csv(lst_temperature_file, index_col=0)

# Fill missing values in LST temperature matrix
lst_temperature.fillna(0, inplace=True)

# Standardize labels in both files
standardized_labels = {f"Class_{i}": f"Class{i}" for i in range(1, 11)}

df.rename(index=standardized_labels, columns=standardized_labels, inplace=True)
lst_temperature.rename(index=standardized_labels, columns=standardized_labels, inplace=True)

# Update class labels with MODIS class names
modis_class_names = {
    "Class1": "Forests",
    "Class2": "Shrublands",
    "Class3": "Savannas",
    "Class4": "Grasslands",
    "Class5": "Permanent Wetlands",
    "Class6": "Croplands",
    "Class7": "Urban and Built-up Lands",
    "Class8": "Permanent Snow and Ice",
    "Class9": "Barren",
    "Class10": "Water Bodies"
}

# Wrap long labels
wrapped_modis_class_names = {
    key: "\n".join(textwrap.wrap(value, width=12))  # Reduced width for compact wrapping
    for key, value in modis_class_names.items()
}

# Rename rows and columns with MODIS names
df.rename(index=wrapped_modis_class_names, columns=wrapped_modis_class_names, inplace=True)
lst_temperature.rename(index=wrapped_modis_class_names, columns=wrapped_modis_class_names, inplace=True)

# Prepare the data for plotting
x = []
y = []
sizes = []
colors = []

# Set minimum and maximum bubble sizes
min_bubble_size = 5000  # Minimum size
scaling_factor = 20000  # Maximum size scaling factor

# Normalize the LST values to [-3, 3] for color mapping
norm = mcolors.Normalize(vmin=-0.1, vmax=0.1)
cmap = cm.get_cmap("bwr")  # Blue-white-red colormap

# Normalize the sizes starting from the minimum size
max_value = max(df.values.flatten())
for row_idx, row_label in enumerate(df.index):
    for col_idx, col_label in enumerate(df.columns):
        value = df.loc[row_label, col_label]
        lst_value = lst_temperature.loc[row_label, col_label]

        # Clip LST values for color mapping
        clipped_lst_value = max(-0.1, min(0.1, lst_value))

        x.append(col_idx + 1)  # x position (column index)
        y.append(len(df.index) - row_idx)  # y position (row index, reversed for better visualization)
        
        # Set size
        if value <= 1000:
            sizes.append(min_bubble_size)  # Minimum size for small values
            colors.append('gray')  # Gray color for small values
        else:
            # Scale starting from minimum size with increased max size
            scaled_size = min_bubble_size + (value / max_value) * scaling_factor
            sizes.append(scaled_size)
            
            # Color based on the clipped LST value
            colors.append(cmap(norm(clipped_lst_value)))

# Create the bubble chart
plt.figure(figsize=(28, 24), dpi=600)  # Larger figure and higher resolution
scatter = plt.scatter(x, y, s=sizes, c=colors, alpha=0.8, edgecolors="w")

# Add LST values as text annotations inside the bubbles
for row_idx, row_label in enumerate(df.index):
    for col_idx, col_label in enumerate(df.columns):
        lst_value = lst_temperature.loc[row_label, col_label]
        original_value = df.loc[row_label, col_label]
        # Only add values to bubbles with original values >= 1000
        if original_value >= 1000:
            plt.text(
                col_idx + 1,
                len(df.index) - row_idx,
                f"{lst_value:.3f}",  # Display actual LST value with 2 decimal points
                color="black",
                fontsize=24,  # Increased font size
                ha="center",
                va="center"
            )

# Customize the axes
plt.xticks(range(1, len(df.columns) + 1), df.columns, fontsize=24)  # Reduced font size for x-axis
plt.yticks(range(1, len(df.index) + 1), reversed(df.index), fontsize=24)  # Reduced font size for y-axis
plt.xlabel("To Classes", fontsize=24, labelpad=40)
plt.ylabel("From Classes", fontsize=24, labelpad=40)
plt.title("Land Cover Transition Bubble Chart with LST Values", fontsize=28, pad=60)

# Move x-axis labels to the top
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()

# Add padding to avoid overlap with the border
plt.gca().set_xlim(0.2, len(df.columns) + 0.8)  # Increased padding on x-axis
plt.gca().set_ylim(0.2, len(df.index) + 0.8)  # Increased padding on y-axis

# Add a colorbar to explain the color ramp
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, orientation="vertical", pad=0.02)
cbar.set_label("LST Value (clipped for color)", fontsize=24)
cbar.ax.tick_params(labelsize=20)

# Add grid for better visualization
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
