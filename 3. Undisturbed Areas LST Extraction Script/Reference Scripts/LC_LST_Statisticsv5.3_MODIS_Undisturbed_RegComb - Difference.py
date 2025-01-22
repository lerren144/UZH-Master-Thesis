from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

# Option to include or exclude outliers
outlier_option = 0  # 0 if without outliers, 1 if with outliers

# Define the paths to your binary and value TIF files
binary_tif_path = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\Disturbed Mask\2000 to 2020 Exports\MODIS LC\Undisturbed_Mask_Changes\Undisturbed_Mask_mosaic.tif'
value_tif_path = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_LST_Results\Compiled_Average_Combination\MOYD21A1DN_2016-2020_2000-2005_Mean_RegressCombination.tif'

# Open the value image using GDAL
value_dataset = gdal.Open(value_tif_path)
value_band = value_dataset.GetRasterBand(1)

# Retrieve the minimum and maximum values using GDAL's GetMinimum() and GetMaximum()
gdal_min = value_band.GetMinimum()
gdal_max = value_band.GetMaximum()

# If min/max is not defined in the metadata, compute the values
if gdal_min is None or gdal_max is None:
    gdal_min, gdal_max = value_band.ComputeRasterMinMax()

# Read the value image data
value_image = value_band.ReadAsArray()

# Open the binary mask image using GDAL
binary_dataset = gdal.Open(binary_tif_path)
binary_band = binary_dataset.GetRasterBand(1)

# Create an in-memory dataset for resampling the binary image
mem_driver = gdal.GetDriverByName('MEM')
resampled_binary_dataset = mem_driver.Create('', value_dataset.RasterXSize, value_dataset.RasterYSize, 1, gdal.GDT_Byte)
resampled_binary_dataset.SetGeoTransform(value_dataset.GetGeoTransform())
resampled_binary_dataset.SetProjection(value_dataset.GetProjection())

# Perform the reprojection/resampling
gdal.ReprojectImage(binary_dataset, resampled_binary_dataset, None, None, gdal.GRA_NearestNeighbour)

# Read the resampled binary image
binary_image = resampled_binary_dataset.GetRasterBand(1).ReadAsArray()

# Apply the binary mask (only keep values where binary image is 1)
# masked_values = value_image[binary_image == 1]
masked_values = value_image[(binary_image == 1) & (value_image != 0)]  # Skip 0 values

# Remove NoData or invalid values (assuming they are represented by NaN)
masked_values = masked_values[~np.isnan(masked_values)]

# If outlier_option is 0, remove outliers using the IQR method
if outlier_option == 0:
    # Calculate the interquartile range (IQR) and use it to remove outliers
    q1 = np.percentile(masked_values, 25)
    q3 = np.percentile(masked_values, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Remove outliers by keeping only values within the IQR bounds
    filtered_values = masked_values[(masked_values >= lower_bound) & (masked_values <= upper_bound)]
    plot_values = filtered_values
else:
    # If outlier_option is 1, include all values and append gdal_min and gdal_max to adjust the plot range
    plot_values = np.append(masked_values, [gdal_min, gdal_max])
    q1 = np.percentile(plot_values, 25)  # Calculate Q1 for printing
    q3 = np.percentile(plot_values, 75)  # Calculate Q3 for printing

# Calculate basic statistics on the selected data
median = np.median(plot_values)
mean = np.mean(plot_values)

# Print the statistics
print(f"First Quartile (Q1, 25th percentile): {q1}")
print(f"Median (Q2, 50th percentile): {median}")
print(f"Mean: {mean}")
print(f"Third Quartile (Q3, 75th percentile): {q3}")

# Generate the box plot based on the outlier option
plt.figure(figsize=(8, 6))
plt.boxplot(plot_values, showfliers=bool(outlier_option))  # Show or hide outliers based on the option
plt.title(f'Box Plot of Masked Values {"(with outliers)" if outlier_option else "(without outliers)"}')
plt.ylabel('Value')

# Add the mean as a red point on the box plot
plt.plot(1, mean, 'ro')  # Red point for the mean

# Annotate the box plot with statistics and place the mean label above the median
plt.text(1.1, q1, f'Q1: {q1:.2f}', verticalalignment='center')
plt.text(1.1, median, f'Median: {median:.2f}', verticalalignment='center')
plt.text(1.1, mean, f'Mean: {mean:.2f}', verticalalignment='bottom', color='red')  # Label mean above median
plt.text(1.1, q3, f'Q3: {q3:.2f}', verticalalignment='center')

# Add a broken line (dashed line) at the 0-axis
plt.axhline(y=0, color='black', linestyle='--', linewidth=1)  # Dashed line at y=0

# Only set y-axis limits if outlier_option is 1 (with outliers), to match GDAL-provided min and max
if outlier_option == 1:
    plt.text(1.1, gdal_min, f'Min: {gdal_min:.2f}', verticalalignment='center')
    plt.text(1.1, gdal_max, f'Max: {gdal_max:.2f}', verticalalignment='center')

    # Add padding to the y-axis to ensure min/max are not on the edge
    y_min_padding = gdal_min - abs(gdal_min) * 0.05  # 5% padding below min
    y_max_padding = gdal_max + abs(gdal_max) * 0.05  # 5% padding above max
    plt.ylim([y_min_padding, y_max_padding])

# Show the plot
plt.show()
