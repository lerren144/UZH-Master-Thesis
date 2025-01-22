import os
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

# Parameters
input_dir = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\7. LC_LST_Results\4. Compiled_Average_Combination\Corrected\Difference'  # Input directory
binary_tif_path = r'C:\Users\llccl\OneDrive\Documents\To Do\Academics\2nd Year - 1st Semester\Master Thesis\2 - Thesis Proper\5 - Processing\3. Disturbed Mask\2000 to 2020 Exports\Copernicus LC\Undisturbed_Mask_Changes\undisturbed_mask.tif'  # Binary mask
export_dir = r'C:\Users\llccl\Downloads\Undisturbed LST\Difference'  # Output directory
os.makedirs(export_dir, exist_ok=True)  # Create output directory if it doesn't exist

# Outlier option (0 = exclude outliers, 1 = include outliers)
outlier_option = 0

# Prepare output text file
output_stats_path = os.path.join(export_dir, 'statistics_results.txt')

with open(output_stats_path, 'w') as stats_file:
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.tif'):
            value_tif_path = os.path.join(input_dir, file_name)
            print(f'Processing: {value_tif_path}')

            # Open the value image
            value_dataset = gdal.Open(value_tif_path)
            value_band = value_dataset.GetRasterBand(1)

            # Get min/max values
            gdal_min = value_band.GetMinimum()
            gdal_max = value_band.GetMaximum()
            if gdal_min is None or gdal_max is None:
                gdal_min, gdal_max = value_band.ComputeRasterMinMax()

            value_image = value_band.ReadAsArray()

            # Open and resample binary mask
            binary_dataset = gdal.Open(binary_tif_path)
            mem_driver = gdal.GetDriverByName('MEM')
            resampled_binary_dataset = mem_driver.Create(
                '', value_dataset.RasterXSize, value_dataset.RasterYSize, 1, gdal.GDT_Byte
            )
            resampled_binary_dataset.SetGeoTransform(value_dataset.GetGeoTransform())
            resampled_binary_dataset.SetProjection(value_dataset.GetProjection())
            gdal.ReprojectImage(binary_dataset, resampled_binary_dataset, None, None, gdal.GRA_NearestNeighbour)
            binary_image = resampled_binary_dataset.GetRasterBand(1).ReadAsArray()

            # Mask the values
            masked_values = value_image[(binary_image == 1) & (value_image != 0)]
            masked_values = masked_values[~np.isnan(masked_values)]

            # Handle outliers
            if outlier_option == 0:
                q1 = np.percentile(masked_values, 25)
                q3 = np.percentile(masked_values, 75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                filtered_values = masked_values[(masked_values >= lower_bound) & (masked_values <= upper_bound)]
                plot_values = filtered_values
            else:
                plot_values = np.append(masked_values, [gdal_min, gdal_max])
                q1 = np.percentile(plot_values, 25)
                q3 = np.percentile(plot_values, 75)

            # Calculate statistics
            plot_values = plot_values / 1
            q1, q3 = q1 / 1, q3 / 1
            median = np.median(plot_values)
            mean = np.mean(plot_values)
            gdal_min, gdal_max = gdal_min / 1, gdal_max / 1

            # Write statistics to file (full precision)
            stats_file.write(f'{file_name}\n')
            stats_file.write(f'  Q1: {q1}\n')
            stats_file.write(f'  Median: {median}\n')
            stats_file.write(f'  Mean: {mean}\n')
            stats_file.write(f'  Q3: {q3}\n')
            if outlier_option == 1:
                stats_file.write(f'  Min: {gdal_min}\n')
                stats_file.write(f'  Max: {gdal_max}\n')
            stats_file.write('\n')

            # Generate and save box plot (rounded values for annotations)
            plt.figure(figsize=(8, 6))
            plt.boxplot(plot_values, showfliers=bool(outlier_option))
            plt.title(f'Box Plot of {file_name} {"(with outliers)" if outlier_option else "(without outliers)"}')
            plt.ylabel('Value')
            plt.plot(1, mean, 'ro')  # Red point for mean
            plt.text(1.1, q1, f'Q1: {q1:.2f}', verticalalignment='center')
            plt.text(1.1, median, f'Median: {median:.2f}', verticalalignment='center')
            plt.text(1.1, mean, f'Mean: {mean:.2f}', verticalalignment='bottom', color='red')
            plt.text(1.1, q3, f'Q3: {q3:.2f}', verticalalignment='center')
            plt.axhline(y=0, color='black', linestyle='--', linewidth=1)

            if outlier_option == 1:
                plt.text(1.1, gdal_min, f'Min: {gdal_min:.2f}', verticalalignment='center')
                plt.text(1.1, gdal_max, f'Max: {gdal_max:.2f}', verticalalignment='center')
                y_min_padding = gdal_min - abs(gdal_min) * 0.05
                y_max_padding = gdal_max + abs(gdal_max) * 0.05
                plt.ylim([y_min_padding, y_max_padding])

            plot_path = os.path.join(export_dir, f'{os.path.splitext(file_name)[0]}_boxplot.png')
            plt.savefig(plot_path)
            plt.close()

print(f'Statistics and box plots exported to {export_dir}')
