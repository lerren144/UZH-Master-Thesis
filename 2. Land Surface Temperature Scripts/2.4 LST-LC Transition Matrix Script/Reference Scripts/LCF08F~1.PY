import os
import rasterio
import numpy as np
import pandas as pd
from rasterio.warp import reproject, Resampling

# Define the specific class labels
classes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220]

# Define directories
mask_dir = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\Disturbed Mask\2000 to 2020 Exports\Copernicus LC\Disturbed_Mask_LC"
lst_path = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_LST_Results\Compiled_Average_Combination\MOYD21A1DN_2000-2000_LinearTrend_Average.tif"
output_csv = r"C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\Thesis New\LC_LST_Results\MOYD21A1DN_transition_matrix_Copernicus_Ave - LinearHarmonized.csv"

# Initialize a 22x22 matrix to store mean values
transition_matrix = np.full((22, 22), np.nan)

# Create a mapping from class label to index
class_to_index = {cls: idx for idx, cls in enumerate(classes)}

# Open the LST image and extract the data and CRS
with rasterio.open(lst_path) as lst_ds:
    lst_data = lst_ds.read(1)
    lst_transform = lst_ds.transform
    lst_crs = lst_ds.crs

# Iterate over each file in the mask directory
for filename in os.listdir(mask_dir):
    if filename.endswith("_Mask.tif"):
        # Parse the class transition from the filename
        parts = filename.split('_')
        class_from = int(parts[0].replace("Class", ""))
        class_to = int(parts[2].replace("Class", ""))

        # Check if class_from and class_to are in the specified classes
        if class_from in class_to_index and class_to in class_to_index:
            # Get corresponding indices for matrix placement
            from_idx = class_to_index[class_from]
            to_idx = class_to_index[class_to]

            # Open the mask image
            mask_path = os.path.join(mask_dir, filename)
            with rasterio.open(mask_path) as mask_ds:
                mask_crs = mask_ds.crs

                # Reproject if the CRS does not match
                if mask_crs != lst_crs:
                    reprojected_mask = np.empty(shape=lst_data.shape, dtype=mask_ds.dtypes[0])
                    reproject(
                        source=rasterio.band(mask_ds, 1),
                        destination=reprojected_mask,
                        src_transform=mask_ds.transform,
                        src_crs=mask_crs,
                        dst_transform=lst_transform,
                        dst_crs=lst_crs,
                        resampling=Resampling.nearest
                    )
                else:
                    reprojected_mask = mask_ds.read(1)

                # Extract LST values where the mask has value 1
                masked_lst_values = lst_data[reprojected_mask == 1]
                masked_lst_values = masked_lst_values[~np.isnan(masked_lst_values)]  # Remove NaN values if any

                # Calculate Q1, Q3 and filter values within the IQR range
                if masked_lst_values.size > 0:
                    q1 = np.percentile(masked_lst_values, 25)
                    q3 = np.percentile(masked_lst_values, 75)
                    filtered_values = masked_lst_values[(masked_lst_values >= q1) & (masked_lst_values <= q3)]

                    # Calculate the mean of the filtered values
                    if filtered_values.size > 0:
                        mean_value = np.mean(filtered_values)
                        transition_matrix[from_idx, to_idx] = mean_value

# Convert matrix to DataFrame and save to CSV
transition_df = pd.DataFrame(transition_matrix, columns=[f'Class{cls}' for cls in classes], index=[f'Class{cls}' for cls in classes])
transition_df.to_csv(output_csv, index=True)

print(f"Class transition matrix saved to {output_csv}")