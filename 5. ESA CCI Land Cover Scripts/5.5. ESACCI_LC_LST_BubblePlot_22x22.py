import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

# Define the input file paths
transition_matrix_file = r'C:\\Users\\llccl\\OneDrive\\Documents\\To Do\\Academics\\2nd Year - 1st Semester\\Master Thesis\\2 - Thesis Proper\\5 - Processing\\6. Transition Matrix\\LC_ESACCI_0615_transition_matrix_22x22 - Area.csv'
lst_temperature_file = r'C:\\Users\\llccl\\Downloads\\2_LC_ESACCI_0615_v2\\1.Difference\\MOYD21A1DN_2016-2020_2000-2005_RegressCombination_transition_matrix - Final.csv'

# Load the data
df = pd.read_csv(transition_matrix_file, index_col=0)
lst_temperature = pd.read_csv(lst_temperature_file, index_col=0)

# Map labels from `Class_XX` to `ClassXX`
df.index = df.index.str.replace("_", "")
df.columns = df.columns.str.replace("_", "")

lst_temperature.index = lst_temperature.index.str.replace("_", "")
lst_temperature.columns = lst_temperature.columns.str.replace("_", "")

# Verify that the labels are now consistent
if not df.index.equals(lst_temperature.index) or not df.columns.equals(lst_temperature.columns):
    print("Mismatch found after renaming labels.")
    print("Transition Matrix Labels:", df.index.tolist(), df.columns.tolist())
    print("LST Matrix Labels:", lst_temperature.index.tolist(), lst_temperature.columns.tolist())
    raise ValueError("Row and column labels still do not match after renaming.")

# Fill missing values in LST temperature matrix
lst_temperature.fillna(0, inplace=True)

# Prepare the data for plotting
x = []
y = []
sizes = []
colors = []

# Set minimum and maximum bubble sizes
min_bubble_size = 3000  # Minimum size
scaling_factor = 15000  # Maximum size scaling factor

# Normalize the LST values to [-3, 3] for color mapping, with clipping for values outside this range
norm = mcolors.Normalize(vmin=-3, vmax=3)
cmap = cm.get_cmap("bwr")  # Blue-white-red colormap

# Normalize the sizes starting from the minimum size
max_value = max(df.values.flatten())
for row_idx, row_label in enumerate(df.index):
    for col_idx, col_label in enumerate(df.columns):
        value = df.loc[row_label, col_label]
        lst_value = lst_temperature.loc[row_label, col_label]

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
            
            # Clip LST values to [-3, 3] range and apply colormap
            clipped_lst_value = np.clip(lst_value, -3, 3)
            colors.append(cmap(norm(clipped_lst_value)))

# Create the bubble chart
plt.figure(figsize=(40, 24), dpi=600)  # Larger figure and higher resolution
scatter = plt.scatter(x, y, s=sizes, c=colors, alpha=0.8, edgecolors="w")

# Add LST values as text annotations inside the bubbles
for row_idx, row_label in enumerate(df.index):
    for col_idx, col_label in enumerate(df.columns):
        lst_value = lst_temperature.loc[row_label, col_label]
        original_value = df.loc[row_label, col_label]
        
        # Only annotate for bubbles with original values >= 1000
        if original_value >= 1000:
            # Display clipped values for color consistency, but annotate original LST value
            if lst_value > 3:
                annotation = ">3"  # Indicate it's above the range
            elif lst_value < -3:
                annotation = "<-3"  # Indicate it's below the range
            else:
                annotation = f"{lst_value:.3f}"  # Display actual LST value within range
            
            # Add the annotation text
            plt.text(
                col_idx + 1,
                len(df.index) - row_idx,
                annotation,
                color="black",
                fontsize=24,
                ha="center",
                va="center"
            )

# Customize the axes
plt.xticks(range(1, len(df.columns) + 1), df.columns, fontsize=20)  # Adjusted font size for x-axis
plt.yticks(range(1, len(df.index) + 1), reversed(df.index), fontsize=24)  # Adjusted font size for y-axis
plt.xlabel("To Classes", fontsize=16, labelpad=20)
plt.ylabel("From Classes", fontsize=16, labelpad=20)
plt.title("Land Cover Transition Bubble Chart with LST Values", fontsize=20, pad=40)

# Move x-axis labels to the top
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()

# Add padding to avoid overlap with the border
plt.gca().set_xlim(0.2, len(df.columns) + 0.8)  # Adjusted padding on x-axis
plt.gca().set_ylim(0.2, len(df.index) + 0.8)  # Adjusted padding on y-axis

# Add a colorbar to explain the color ramp
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, orientation="vertical", pad=0.02)
cbar.set_label("LST Value", fontsize=24)
cbar.ax.tick_params(labelsize=20)

# Add grid for better visualization
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
