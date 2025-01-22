import os
import xarray as xr
import dask.array as da
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Compression
from tqdm import tqdm

# Define input and output directories
input_directory = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\Copernicus Land Cover Classification Gridded Maps'
output_directory = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\Converted Copernicus LC Gridded'

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Specify the variable to extract
variable_name = 'lccs_class'

# Loop through all .nc files in the input directory
for filename in tqdm(os.listdir(input_directory)):
    if filename.endswith('.nc'):
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.tif")

        # Open the .nc file with xarray
        ds = xr.open_dataset(input_path)
        
        # Check if the specified variable exists
        if variable_name not in ds:
            print(f"Variable '{variable_name}' not found in {filename}. Skipping...")
            continue
        
        # Extract the variable data
        data = ds[variable_name]

        # If the data has more than 2 dimensions, select the first slice or reduce it to 2D
        if data.ndim > 2:
            data = data.isel(time=0)  # Adjust if needed

        # Convert the data to a Dask array for memory-efficient chunked processing
        data = data.chunk({'lat': 1000, 'lon': 1000})  # Adjust chunk size as needed

        # Convert to a 2D array if necessary and ensure the data type
        data_2d = data.squeeze().astype('uint8')

        # Check if latitude and longitude bounds are available
        if 'lat_bounds' in ds and 'lon_bounds' in ds:
            lats = ds['lat_bounds'].values
            lons = ds['lon_bounds'].values
            transform = from_bounds(lons.min(), lats.min(), lons.max(), lats.max(), data_2d.shape[1], data_2d.shape[0])
        else:
            raise KeyError("Latitude and longitude bounds ('lat_bounds' and 'lon_bounds') not found in the dataset.")

        # Write data to GeoTIFF with compression and chunking
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=data_2d.shape[0],
            width=data_2d.shape[1],
            count=1,
            dtype='uint8',
            crs='EPSG:4326',  # Assuming the coordinate reference system is WGS84
            transform=transform,
            compress='LZW'  # Use LZW compression for better file size
        ) as dst:
            # Iterate over the Dask array in chunks and write them to the output file
            for i in range(0, data_2d.shape[0], 1000):  # Process by row chunks
                for j in range(0, data_2d.shape[1], 1000):  # Process by column chunks
                    window = data_2d.isel(lat=slice(i, i + 1000), lon=slice(j, j + 1000)).values
                    dst.write(window, 1, window=((i, i + window.shape[0]), (j, j + window.shape[1])))

        # Close the dataset
        ds.close()

        print(f"Processed {filename} to {output_path} with compression and chunked processing")
