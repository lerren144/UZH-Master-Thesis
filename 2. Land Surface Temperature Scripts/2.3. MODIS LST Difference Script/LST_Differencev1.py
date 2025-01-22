import os
import numpy as np
import rasterio
from tqdm import tqdm

# Set your input and output directories
input_directory = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_LST_Results\Compiled_Mosaic'
output_directory = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_LST_Results\Compiled_Difference'

# Define the LST types, year ranges, and item types
lst_types = ['MOD21A1D', 'MOD21A1N', 'MYD21A1D', 'MYD21A1N']
year_range_1 = '2000-2005_'
year_range_2 = '2016-2020_'
item_types = ['amplitude', 'constant', 'data_count', 'mean', 'phase', 'rmse']
divide_factor = 100  # Define the divide factor

# Function to perform pixel-by-pixel raster subtraction and divide output by a factor
def subtract_and_divide_rasters(file1, file2, output_file, divide_factor):
    with rasterio.open(file1) as src1, rasterio.open(file2) as src2:
        # Ensure rasters have the same shape and transform
        if src1.shape != src2.shape:
            print(f"Error: Shapes of {file1} and {file2} do not match.")
            return
        
        if src1.transform != src2.transform:
            print(f"Error: Georeferencing transforms of {file1} and {file2} do not match.")
            return

        # Read the raster data
        data1 = src1.read(1).astype('float32')  # Data for 2000-2005
        data2 = src2.read(1).astype('float32')  # Data for 2016-2020
        
        # Mask no-data values if they exist
        nodata1 = src1.nodata
        nodata2 = src2.nodata
        if nodata1 is not None:
            data1 = np.where(data1 == nodata1, np.nan, data1)
        if nodata2 is not None:
            data2 = np.where(data2 == nodata2, np.nan, data2)

        # Perform the pixel-by-pixel subtraction
        diff_data = data2 - data1
        
        # Divide the result by the divide_factor
        diff_data = diff_data / divide_factor

        # Handle potential NaN values (set to a no-data value, e.g., -9999)
        diff_data = np.where(np.isnan(diff_data), -9999, diff_data)
        
        # Write the result to a new file
        profile = src1.profile
        profile.update(dtype=rasterio.float32, nodata=-9999)
        
        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(diff_data, 1)

# Iterate through each LST type and item type with progress bars
for lst_type in tqdm(lst_types, desc="LST Types", leave=True):
    for item_type in tqdm(item_types, desc=f"Processing {lst_type}", leave=False):
        # Build filenames for the year ranges
        file_2000_2005 = f"{lst_type}_Global_{year_range_1}1000m_vat45_LSTday_{item_type}_mosaic.tif"
        file_2016_2020 = f"{lst_type}_Global_{year_range_2}1000m_vat45_LSTday_{item_type}_mosaic.tif"
        
        # Full paths to the input files
        file_2000_2005_path = os.path.join(input_directory, file_2000_2005)
        file_2016_2020_path = os.path.join(input_directory, file_2016_2020)
        
        # Check if both files exist
        if os.path.exists(file_2000_2005_path) and os.path.exists(file_2016_2020_path):
            # Build output filename
            output_filename = f"{lst_type}_{year_range_2}{year_range_1}{item_type}_difference.tif"
            output_file_path = os.path.join(output_directory, output_filename)
            
            # Perform pixel-by-pixel raster subtraction, division, and save the result
            subtract_and_divide_rasters(file_2000_2005_path, file_2016_2020_path, output_file_path, divide_factor)
        else:
            print(f"Files missing for {lst_type} {item_type}, skipping...")
