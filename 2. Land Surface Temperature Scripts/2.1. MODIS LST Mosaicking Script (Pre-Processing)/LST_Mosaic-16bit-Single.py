import os
from osgeo import gdal

# Directory where the TIF images are stored
input_dir = os.getcwd()  # Assumes the script is in the same directory as the TIFs
output_dir = os.path.join(input_dir, "Mosaic_Data")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to mosaic multiple TIF files without scaling and keeping negative values
def mosaic_tif_files(file_list, output_name):
    output_file = os.path.join(output_dir, output_name)
    
    # Open the source files
    src_datasets = [gdal.Open(file) for file in file_list]

    # Create a VRT (Virtual Dataset) that references all input datasets
    vrt_options = gdal.BuildVRTOptions(separate=False)
    vrt = gdal.BuildVRT(output_file.replace(".tif", ".vrt"), src_datasets, options=vrt_options)

    # Read metadata from VRT
    geotransform = vrt.GetGeoTransform()
    projection = vrt.GetProjection()
    x_size = vrt.RasterXSize
    y_size = vrt.RasterYSize

    # Create a new dataset to write the data to a 16-bit signed GeoTIFF
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(output_file, x_size, y_size, 1, gdal.GDT_Int16, ['COMPRESS=LZW'])
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(projection)

    # Read and write data band by band
    for i in range(1, vrt.RasterCount + 1):
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

# Define the start name to select the files
start_name = "MYD21A1N_Global_2000-2020_1000m_vat45_LSTday_mean"
file_list = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.startswith(start_name) and file.endswith(".tif")]

# Mosaic all matching files
if file_list:
    output_name = f"{start_name}_mosaic.tif"
    mosaic_tif_files(file_list, output_name)
    print("Mosaicing completed. Check the 'Mosaic_Data' folder for output files.")
else:
    print("No matching files found for mosaicing.")
