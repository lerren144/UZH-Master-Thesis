import os
from osgeo import gdal

# Directory where the TIF images are stored
input_dir = os.getcwd()  # Assumes the script is in the same directory as the TIFs
output_dir = os.path.join(input_dir, "Mosaic_Data")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to mosaic a pair of TIF files, scaling by 100, converting to 16-bit, and applying compression
def mosaic_tif_files(file1, file2, output_name):
    output_file = os.path.join(output_dir, output_name)
    
    # Open the source files
    src_ds1 = gdal.Open(file1)
    src_ds2 = gdal.Open(file2)

    # Create a VRT (Virtual Dataset) that references both input datasets
    vrt_options = gdal.BuildVRTOptions(separate=False)
    vrt = gdal.BuildVRT(output_file.replace(".tif", ".vrt"), [src_ds1, src_ds2], options=vrt_options)

    # Read the VRT as a NumPy array
    vrt_band = vrt.GetRasterBand(1)
    vrt_array = vrt_band.ReadAsArray()

    # Edit Scale Here 
    scaled_array = vrt_array * 1

    # Create a new dataset to write the scaled data to a 16-bit GeoTIFF
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(output_file, vrt.RasterXSize, vrt.RasterYSize, 1, gdal.GDT_UInt16, ['COMPRESS=LZW'])
    dst_ds.SetGeoTransform(vrt.GetGeoTransform())
    dst_ds.SetProjection(vrt.GetProjection())

    # Write the scaled data
    dst_band = dst_ds.GetRasterBand(1)
    dst_band.WriteArray(scaled_array)
    
    # Flush the cache to ensure all data is written
    dst_band.FlushCache()

    # Clean up
    vrt = None
    src_ds1 = None
    src_ds2 = None
    dst_ds = None

# Group files by base name before the final two parts
file_pairs = {}

for file in os.listdir(input_dir):
    if file.endswith(".tif"):
        # Extract the base name before the final two hyphen-separated parts
        base_name = '-'.join(file.split('-')[:-2])
        suffix = '-'.join(file.split('-')[-2:])  # Extract the last two parts of the filename
        
        if base_name not in file_pairs:
            file_pairs[base_name] = []

        # Add file to the list associated with the base name
        file_pairs[base_name].append(file)

# Mosaic the pairs
for base_name, files in file_pairs.items():
    if len(files) == 2:  # Only mosaic if there are exactly two files in the pair
        output_name = f"{base_name}_mosaic.tif"
        mosaic_tif_files(os.path.join(input_dir, files[0]), os.path.join(input_dir, files[1]), output_name)

print("Mosaicing completed. Check the 'Mosaic_Data' folder for output files.")
