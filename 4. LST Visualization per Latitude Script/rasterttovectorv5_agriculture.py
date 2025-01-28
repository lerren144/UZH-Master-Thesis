import rasterio
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from tqdm import tqdm

# Input and output file paths
input_tif = "before_landcover_rev.tif"  # Input raster
output_shp = "before_points_agriculture.shp"  # Output shapefile for sampled points

# Values to filter
target_values = [10, 20, 30, 40]

# Open the raster file
with rasterio.open(input_tif) as src:
    # Read the first band and transform
    data = src.read(1)
    transform = src.transform
    crs = src.crs  # Coordinate reference system

# Find rows and columns where pixel values match the target values
rows, cols = np.where(np.isin(data, target_values))

# Efficiently compute coordinates
coords = rasterio.transform.xy(transform, rows, cols, offset='center')
coords = np.array(coords).T  # Transpose to align x, y pairs

# Randomly sample 50,000 points if possible
num_points = len(coords)
sample_size = min(50000, num_points)  # Ensure sample size does not exceed available points
sample_indices = np.random.choice(num_points, size=sample_size, replace=False)
sample_coords = coords[sample_indices]

# Get the corresponding pixel values for the sampled points
sample_values = data[rows[sample_indices], cols[sample_indices]]

# Create a GeoDataFrame for the sampled points
gdf = gpd.GeoDataFrame(
    {"value": sample_values},  # Assign corresponding pixel values to points
    geometry=[Point(x, y) for x, y in tqdm(sample_coords, desc="Creating sampled points")],
    crs=crs
)

# Save to shapefile
gdf.to_file(output_shp, driver="ESRI Shapefile")
print(f"Shapefile with sampled points (values={target_values}) saved to {output_shp}")
