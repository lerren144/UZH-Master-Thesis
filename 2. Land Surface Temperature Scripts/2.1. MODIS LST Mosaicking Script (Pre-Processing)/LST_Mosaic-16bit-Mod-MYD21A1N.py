import os
from osgeo import gdal
import re
from tqdm import tqdm
from collections import defaultdict

# Directory where the TIF images are stored
input_dir = os.getcwd()  # Assumes the script is in the same directory as the TIFs
output_dir = os.path.join(input_dir, "Mosaic_Data")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to mosaic multiple TIF files while retaining decimal points, negative values, and original coordinate system
def mosaic_tif_files(file_list, output_name):
    output_file = os.path.join(output_dir, output_name)
    
    # Open the source files
    src_datasets = [gdal.Open(file) for file in tqdm(file_list, desc=f"Opening files for {output_name}")]

    # Create a VRT (Virtual Dataset) that references all input datasets
    vrt_options = gdal.BuildVRTOptions(separate=False)
    vrt = gdal.BuildVRT(output_file.replace(".tif", ".vrt"), src_datasets, options=vrt_options)

    # Get metadata (geotransform and projection) from the VRT
    geotransform = vrt.GetGeoTransform()
    projection = vrt.GetProjection()
    x_size = vrt.RasterXSize
    y_size = vrt.RasterYSize

    # Create a new dataset to write the data to a floating-point GeoTIFF
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Float32, ['COMPRESS=LZW'])
    dst_ds.SetGeoTransform(geotransform)  # Set geotransform (coordinates)
    dst_ds.SetProjection(projection)     # Set the coordinate system (projection)

    # Read and write data band by band
    for i in tqdm(range(1, vrt.RasterCount + 1), desc=f"Processing bands for {output_name}"):
        vrt_band = vrt.GetRasterBand(i)
        data = vrt_band.ReadAsArray()
        
        dst_band = dst_ds.GetRasterBand(i)
        dst_band.WriteArray(data)

    # Flush the cache to ensure all data is written
    dst_band.FlushCache()

    # Clean up
    vrt = None
    for ds in src_datasets:
        ds = None
    dst_ds = None

# Regex pattern to match filenames and group by shared prefixes
pattern = re.compile(r"^(MYD21A1N_Global_2000-2020_1000m_vat45_LSTday_[^_]+)_.*\.tif$")

# Group files by their shared prefix
grouped_files = defaultdict(list)
for file in os.listdir(input_dir):
    if file.endswith(".tif"):  # Ensure we're only processing .tif files
        match = pattern.match(file)
        if match:
            prefix = match.group(1)  # Extract the shared prefix
            grouped_files[prefix].append(os.path.join(input_dir, file))

# Process each group of matching files
for prefix, file_list in grouped_files.items():
    if len(file_list) > 1:  # Only process if there are multiple files in the group
        output_name = f"{prefix}_mosaic.tif"
        print(f"Processing group: {prefix} ({len(file_list)} files)")
        mosaic_tif_files(file_list, output_name)
        print(f"Mosaicing completed: {output_name}")
    else:
        print(f"Skipping group with insufficient files: {prefix}")
