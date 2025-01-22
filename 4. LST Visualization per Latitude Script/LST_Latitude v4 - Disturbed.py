import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Input file path
input_file = r'C:\\Users\\llccl\\Downloads\\9. Final Visualization v2\\disturbed_mask.tif'

# Open the raster file
with rasterio.open(input_file) as dataset:
    if dataset.crs != 'EPSG:4326':
        raise ValueError("The raster file is not in EPSG:4326 CRS. Please reproject the file before running this script.")

    # Get raster dimensions and transformation
    nrows, ncols = dataset.height, dataset.width
    transform = dataset.transform

    # Initialize variables for counting positive pixels
    positive_pixel_counts = []
    latitude_bins = []

    # Process row by row
    for row_idx in range(nrows):
        # Read one row at a time
        row_data = dataset.read(1, window=((row_idx, row_idx + 1), (0, ncols))).astype(float)

        # Replace no-data values with NaN
        row_data[row_data == dataset.nodata] = np.nan

        # Count positive values
        positive_count = np.sum(row_data > 0)

        if positive_count > 0:
            # Calculate the latitude for the row
            lat = transform * (0, row_idx)
            latitude_bins.append(lat[1])  # Latitude is the second component of the transformation
            positive_pixel_counts.append(positive_count)

# Convert to numpy arrays
latitude_bins = np.array(latitude_bins)
positive_pixel_counts = np.array(positive_pixel_counts)

# Generate y-ticks from -60 to 80 in steps of 20
lat_ticks = np.arange(-60, 81, 20)

# Scatter plot for positive pixel counts by latitude
plt.figure(figsize=(3.5, 8), dpi=400)  # Adjusted figure size
plt.scatter(positive_pixel_counts, latitude_bins, alpha=0.5, s=10, c='black')
plt.ylabel('Latitude (degrees)')
plt.xlabel('Positive Pixel Count')
plt.title('Positive Pixel Counts by Latitude')
plt.yticks(lat_ticks, labels=lat_ticks)
plt.grid(True)
plt.show()
