import rasterio
import rasterio.warp
import numpy as np
import matplotlib.pyplot as plt

# Input file path
input_file = r'C:\Users\llccl\Downloads\9. Final Visualization v2\Linear Trend\reprojected_corrected_MOYD21A1DN_2000-2020_LinearTrend_RegressCombination.tif'

# Open the raster file and reproject to EPSG:4326 if necessary
with rasterio.open(input_file) as dataset:
    if dataset.crs != 'EPSG:4326':
        transform, width, height = rasterio.warp.calculate_default_transform(
            dataset.crs, 'EPSG:4326', dataset.width, dataset.height, *dataset.bounds
        )
        kwargs = dataset.meta.copy()
        kwargs.update({
            'crs': 'EPSG:4326',
            'transform': transform,
            'width': width,
            'height': height
        })

        output_file = 'reprojected_file.tif'
        with rasterio.open(output_file, 'w', **kwargs) as dest:
            for i in range(1, dataset.count + 1):
                rasterio.warp.reproject(
                    source=rasterio.band(dataset, i),
                    destination=rasterio.band(dest, i),
                    src_transform=dataset.transform,
                    src_crs=dataset.crs,
                    dst_transform=transform,
                    dst_crs='EPSG:4326',
                    resampling=rasterio.warp.Resampling.nearest
                )
        dataset = rasterio.open(output_file)

    data = dataset.read(1)  # Read the first band
    data[data == dataset.nodata] = np.nan  # Replace no-data values with NaN
    transform = dataset.transform

# Get latitude values for each row
nrows, ncols = data.shape
latitudes = np.array([transform * (0, row_idx) for row_idx in range(nrows)])
latitudes = latitudes[:, 1]  # Extract the latitude component

# Separate positive and negative values with corresponding latitudes
positive_lat_values = []
positive_temp_values = []
negative_lat_values = []
negative_temp_values = []

for row_idx, lat in enumerate(latitudes):
    valid_data = data[row_idx, :]
    positive_indices = np.where((valid_data > 0) & (valid_data <= 1))[0]  # Positive values between 0 and 1
    negative_indices = np.where((valid_data < 0) & (valid_data >= -0.5))[0]  # Negative values between -1 and 0

    if positive_indices.size > 0:
        positive_lat_values.extend([lat] * len(positive_indices))
        positive_temp_values.extend(valid_data[positive_indices])

    if negative_indices.size > 0:
        negative_lat_values.extend([lat] * len(negative_indices))
        negative_temp_values.extend(valid_data[negative_indices])

# Convert to numpy arrays
positive_lat_values = np.array(positive_lat_values)
positive_temp_values = np.array(positive_temp_values)
negative_lat_values = np.array(negative_lat_values)
negative_temp_values = np.array(negative_temp_values)

# Randomly sample 50,000 values if available for each set
sample_size = 50000

# Positive values
if len(positive_temp_values) > sample_size:
    sampled_indices = np.random.choice(len(positive_temp_values), sample_size, replace=False)
    positive_lat_values = positive_lat_values[sampled_indices]
    positive_temp_values = positive_temp_values[sampled_indices]

# Negative values
if len(negative_temp_values) > sample_size:
    sampled_indices = np.random.choice(len(negative_temp_values), sample_size, replace=False)
    negative_lat_values = negative_lat_values[sampled_indices]
    negative_temp_values = negative_temp_values[sampled_indices]

# Generate y-ticks from -60 to 80 in steps of 20
lat_ticks = np.arange(-60, 81, 20)

# Scatter plot for positive values
plt.figure(figsize=(2, 8), dpi=400)  # Further reduced width
plt.scatter(positive_temp_values, positive_lat_values, alpha=0.5, s=10, c='red')
plt.ylabel('Latitude (degrees)')
plt.xlabel('Temperature Value (0 to 1)')
plt.title('Positive Temperature Values by Latitude (0 to 1)')
plt.yticks(lat_ticks, labels=lat_ticks)
plt.grid(True)
plt.show()

# Scatter plot for negative values (flipped to the left)
plt.figure(figsize=(2, 8), dpi=400)  # Further reduced width
plt.scatter(-negative_temp_values, negative_lat_values, alpha=0.5, s=10, c='blue')
plt.ylabel('Latitude (degrees)')
plt.xlabel('Flipped Temperature Value (-1 to 0)')
plt.title('Negative Temperature Values by Latitude (-1 to 0)')
plt.yticks(lat_ticks, labels=lat_ticks)
plt.grid(True)
plt.show()
