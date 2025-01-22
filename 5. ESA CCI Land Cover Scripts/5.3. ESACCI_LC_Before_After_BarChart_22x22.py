import matplotlib.pyplot as plt
import pandas as pd

# Input data
data = {
    "Class": [
        10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170,
        180, 190, 200, 210, 220
    ],
    "Pixel_Count_Before": [
        4740556, 783355, 3082565, 4494720, 7040011, 6258551, 8563247,
        5271459, 1041994, 2880277, 1707806, 8257610, 7474365, 131,
        10011670, 937029, 75928, 3594530, 0, 6992931, 1752748, 8
    ],
    "Pixel_Count_After": [
        5813663, 700387, 3958550, 4566748, 3882131, 6867684, 4715182, 
        2740853, 667726, 11599400, 1691550, 7450463, 9170683, 0, 
        8563181, 888690, 150373, 2863786, 4993119, 2527257, 1150065, 0
    ]
}

# Copernicus class names
copernicus_class_names = {
    10: "Cropland rainfed",
    20: "Cropland irrigated or post-flooding",
    30: "Mosaic cropland (>50%) / natural vegetation (tree, shrub, herbaceous cover) (<50%) ",
    40: "Mosaic natural vegetation (tree, shrub, herbaceous cover) (>50%) / cropland (<50%)",
    50: "Tree cover, broadleaved, evergreen, closed to open (>15%)",
    60: "Tree cover, broadleaved, deciduous, closed to open (>15%) ",
    70: "Tree cover, needleleaved, evergreen, closed to open (>15%)",
    80: "Tree cover, needleleaved, deciduous, closed to open (>15%)",
    90: "Tree cover, mixed leaf type (broadleaved and needleleaved)",
    100: "Mosaic tree and shrub (>50%) / herbaceous cover (<50%)",
    110: "Mosaic herbaceous cover (>50%) / tree and shrub (<50%)",
    120: "Shrubland",
    130: "Grassland",
    140: "Lichens and mosses",
    150: "Sparse vegetation (tree, shrub, herbaceous cover) (<15%)",
    160: "Tree cover, flooded, fresh or brackish water ",
    170: "Tree cover, flooded, saline water",
    180: "Shrub or herbaceous cover, flooded, fresh/saline/brackish water",
    190: "Urban areas",
    200: "Bare areas",
    210: "Water bodies",
    220: "Permanent snow and ice"
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
gap = 0.02  # Small gap between bars
bar_positions = df["Adjusted_Height"].cumsum() + gap * (df.index + 0.5) - df["Adjusted_Height"] / 2

# Map Copernicus class names to the Class column
df["Class_Name"] = df["Class"].map(copernicus_class_names)

# Dynamically calculate figure size
base_height = 6  # Minimum height for the figure
extra_height_per_class = 0.5
fig_height = base_height + len(df) * extra_height_per_class

fig, ax = plt.subplots(figsize=(10, fig_height), dpi=300)  # Increased resolution

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
for i, pos in enumerate(bar_positions):
    percentage_label = f"{df['Normalized_Height'][i] * 100:.1f}%"
    ax.text(
        1.01,  # Position slightly to the right of the maximum x-value
        pos,
        percentage_label,
        ha="left",
        va="center",
        rotation=0,
        fontsize=14,
        color="black"
    )

# Reverse the y-axis to ensure Class 1 is at the top
ax.invert_yaxis()

# Add labels and title
ax.set_ylabel("Land Cover Type", fontsize=14)
ax.set_xlabel("Proportion (Total = 100%)", fontsize=14)
ax.set_title("Stacked Bar Chart of Land Cover Changes with Percentage Labels (Copernicus)", fontsize=16)

# Customize x-axis labels to percentages
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=14)

# Set y-axis labels using Copernicus class names
ax.set_yticks(bar_positions)
ax.set_yticklabels(df["Class_Name"], fontsize=14)

# Move legend to the lower left, outside the plot boundary, and increase its size
ax.legend(loc="lower left", bbox_to_anchor=(-0.20, -0.10), fontsize=14)

# Adjust axis limits to tightly fit bars and include gaps at top and bottom
ax.set_xlim(0, 1.0)
ax.set_ylim(
    bar_positions.min() - gap,  # Add gap to bottom
    bar_positions.max() + gap   # Add gap to top
)

# Adjust layout to remove all border gaps, including the right side
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.02)

# Display the plot
plt.show()
