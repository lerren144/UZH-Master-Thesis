import rasterio
import numpy as np
import os

# Define file paths
input_directory = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\7. LC_LST_Results\3. Compiled_2000_2020"
output_directory = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\7. LC_LST_Results\4. Compiled_Average_Combination"
output_path = os.path.join(output_directory, "MOYD21A1DN_2000-2020_LinearTrend_Average.tif")

# File paths for the four images
image_paths = [
    os.path.join(input_directory, "MOD21A1D_Global_2000-2020_1000m_vat45_LSTday_LinearTrend_mosaic.tif"),
    os.path.join(input_directory, "MOD21A1N_Global_2000-2020_1000m_vat45_LSTday_LinearTrend_mosaic.tif"),
    os.path.join(input_directory, "MYD21A1D_Global_2000-2020_1000m_vat45_LSTday_LinearTrend_mosaic.tif"),
    os.path.join(input_directory, "MYD21A1N_Global_2000-2020_1000m_vat45_LSTday_LinearTrend_mosaic.tif")
]

# Open all images to ensure they have the same dimensions and profile
with rasterio.open(image_paths[0]) as src:
    # Check that all images have the same dimensions
    for img_path in image_paths[1:]:
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
        "crs": "EPSG:4326"  # Ensure the CRS is set to EPSG:4326
    })

    # Create output file
    with rasterio.open(output_path, "w", **out_meta) as dest:
        # Process in chunks
        for ji, window in src.block_windows(1):
            # Read each window from each image as float32
            image_data = []
            for img_path in image_paths:
                with rasterio.open(img_path) as img_src:
                    image_data.append(img_src.read(1, window=window).astype('float32'))

            # Stack images and calculate the average, ignoring NaN values
            stacked_data = np.stack(image_data)
            avg_data = np.nanmean(stacked_data, axis=0)
            
            # Write the result to the corresponding window in the output file
            dest.write(avg_data, 1, window=window)

print("Average image created successfully:", output_path)
