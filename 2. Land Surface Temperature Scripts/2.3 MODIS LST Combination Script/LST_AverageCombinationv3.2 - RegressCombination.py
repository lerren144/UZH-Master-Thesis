import rasterio
import numpy as np
import os

# Define file paths
input_directory = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\7. LC_LST_Results\2. Compiled_Difference"
output_directory = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\7. LC_LST_Results\4. Compiled_Average_Combination"
output_path = os.path.join(output_directory, "MOYD21A1DN_2016-2020_2000-2005_RegressCombination.tif")

# File paths for the four images
Tday_image = os.path.join(input_directory, "MOD21A1D_2016-2020_2000-2005_mean_difference.tif")
Tnight_image = os.path.join(input_directory, "MOD21A1N_2016-2020_2000-2005_mean_difference.tif")
Aday_image = os.path.join(input_directory, "MYD21A1D_2016-2020_2000-2005_mean_difference.tif")
Anight_image = os.path.join(input_directory, "MYD21A1N_2016-2020_2000-2005_mean_difference.tif")

# Coefficients
k1, k2, k3, k4 = 0.1807, 0.3210, 0.1907, 0.3241

# Open all images to ensure they have the same dimensions and profile
with rasterio.open(Tday_image) as src:
    # Check that all images have the same dimensions
    for img_path in [Tnight_image, Aday_image, Anight_image]:
        with rasterio.open(img_path) as check_src:
            if src.shape != check_src.shape:
                raise ValueError("Images do not have the same shape.")

    # Set up metadata for the output file
    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": src.height,
        "width": src.width,
        "transform": src.transform,
        "dtype": "float32",
        "count": 1,
        "crs": "EPSG:4326"  # Assign CRS as WGS 84
    })

    # Create output file
    with rasterio.open(output_path, "w", **out_meta) as dest:
        # Process in chunks
        for ji, window in src.block_windows(1):
            # Read each window from each image as float32
            Tday = rasterio.open(Tday_image).read(1, window=window).astype('float32')
            Tnight = rasterio.open(Tnight_image).read(1, window=window).astype('float32')
            Aday = rasterio.open(Aday_image).read(1, window=window).astype('float32')
            Anight = rasterio.open(Anight_image).read(1, window=window).astype('float32')

            # Apply the equation to compute dmLSTg
            dmLSTg = (
                k1 * Tday +
                k2 * Tnight +
                k3 * Aday +
                k4 * Anight
            )
            
            # Write the result to the corresponding window in the output file
            dest.write(dmLSTg, 1, window=window)

print("dmLSTg image created successfully:", output_path)
