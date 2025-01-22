import matplotlib.pyplot as plt
import pandas as pd

# Input data
data = {
    "Class": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Pixel_Count_Before": [
        10004435, 9543858, 16843773, 14507737, 5863919,
        4670823, 91, 744491, 5961978, 222119
    ],
    "Pixel_Count_After": [
        9395753, 9141055, 20687168, 19505529, 552783,
        5325009, 120404, 805209, 2555699, 274615
    ]
}

# MODIS class names
modis_class_names = {
    1: "Forests",
    2: "Shrublands",
    3: "Savannas",
    4: "Grasslands",
    5: "Permanent Wetlands",
    6: "Croplands",
    7: "Urban and Built-up Lands",
    8: "Permanent Snow and Ice",
    9: "Barren",
    10: "Water Bodies"
}

df = pd.DataFrame(data)

# Calculate proportions for "Before" and "After" relative to the total of each classification
df["Total"] = df["Pixel_Count_Before"] + df["Pixel_Count_After"]
df["Proportion_Before"] = df["Pixel_Count_Before"] / df["Total"]
df["Proportion_After"] = df["Pixel_Count_After"] / df["Total"]

# Correct calculation for percentage change
df["Percent_Change"] = ((df["Pixel_Count_After"] - df["Pixel_Count_Before"]) / df["Pixel_Count_Before"]) * 100

# Normalize bar heights and set a minimum height
total_after_sum = df["Pixel_Count_After"].sum()
df["Normalized_Height"] = df["Pixel_Count_After"] / total_after_sum

# Define a minimum height
minimum_height = 0.05
df["Adjusted_Height"] = df["Normalized_Height"].apply(lambda x: max(x, minimum_height))

# Reverse the order of the DataFrame
df = df.iloc[::-1].reset_index(drop=True)

# Add small gaps between bars
gap = 0.02  # Small gap between bars and added gap at borders
bar_positions = df["Adjusted_Height"].cumsum() + gap * (df.index + 0.5) - df["Adjusted_Height"] / 2

# Map MODIS class names to the Class column
df["Class_Name"] = df["Class"].map(modis_class_names)

# Dynamically calculate figure size
base_height = 6  # Minimum height for the figure
extra_height_per_class = 0.5
fig_height = base_height + len(df) * extra_height_per_class

fig, ax = plt.subplots(figsize=(10, fig_height), dpi=300)  # Increased resolution with dpi=300

# Plot stacked bars with adjusted heights and gaps
bars_before = ax.barh(
    bar_positions, df["Proportion_Before"], color="skyblue", label="Before", height=df["Adjusted_Height"]
)
bars_after = ax.barh(
    bar_positions, df["Proportion_After"], left=df["Proportion_Before"], color="orange", label="After", height=df["Adjusted_Height"]
)

# Add a vertical dashed red line at 50%
ax.axvline(0.5, color="red", linestyle="--", linewidth=1)

# Add a single percentage change label per classification
for i, change in enumerate(df["Percent_Change"]):
    total_width = bars_before[i].get_width() + bars_after[i].get_width()
    ax.text(
        total_width / 2,
        bar_positions[i],
        f"{change:.1f}%",
        ha="center",
        va="center",
        fontsize=14,
        color="black"
    )

# Add percentage of total area to the right of each bar
for i, (pos, height) in enumerate(zip(bar_positions, df["Normalized_Height"])):
    percentage_label = f"{df['Normalized_Height'][i] * 100:.1f}%"
    ax.text(
        1.0,  # Position slightly to the right of the maximum x-value
        pos,
        percentage_label,
        ha="left",
        va="center",
        rotation=45,
        fontsize=14,
        color="black"
    )

# Reverse the y-axis to ensure Class 1 is at the top
ax.invert_yaxis()

# Add labels and title
ax.set_ylabel("Land Cover Type", fontsize=14)
ax.set_xlabel("Proportion (Total = 100%)", fontsize=14)
ax.set_title("Stacked Bar Chart of Land Cover Changes with Percentage Labels", fontsize=16)

# Customize x-axis labels to percentages
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=14)

# Set y-axis labels using MODIS class names
ax.set_yticks(bar_positions)
ax.set_yticklabels(df["Class_Name"], fontsize=14)

# Move legend to the lower left, outside the plot boundary, and increase its size
ax.legend(loc="lower left", bbox_to_anchor=(-0.20, -0.10), fontsize=14)

# Adjust axis limits to add a gap at the top and bottom
ax.set_xlim(0, 1.0)  # Remove extra space on the right
ax.set_ylim(bar_positions.min() - gap,  # Add gap below the bars
            bar_positions.max() + gap)  # Add gap above the bars

# Adjust layout to remove unnecessary border gaps
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.02)

# Display the plot
plt.show()
