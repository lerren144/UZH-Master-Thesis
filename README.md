# UZH-Master-Thesis
This repository contains scripts and code developed as part of the research study: Quantifying Land Surface Temperature Changes Associated with Land Cover Changes. The study was conducted for a Master's degree in Geography with a concentration in Remote Sensing at the University of Zurich.


1. MODIS LST and Visualization:
All the scripts provided in text file format were extracted directly from Google Earth Engine. These scripts contain the code used for processing the harmonics and extracting the MODIS LST Products.

1.1 MODIS LST Global Coverage
Google Earth Engine Code Editor: https://code.earthengine.google.com/a4cc8f8b94e8bd6cfbb1b37854a200b1
GitHub Repository: 
https://github.com/lerren144/UZH-Master-Thesis/blob/32b2d3cfb849a11779f093e3e67c9bb760159e1c/1.%20MODIS%20LST%20and%20Visualization/1.1%20MODIS%20LST%20Global%20Coverage.txt

1.2 MODIS LST Divided Global Coverage
Google Earth Engine Code Editor: 
https://code.earthengine.google.com/011b0909ddea608c5660b4cd632a9cfd
GitHub Repository:
https://github.com/lerren144/UZH-Master-Thesis/blob/32b2d3cfb849a11779f093e3e67c9bb760159e1c/1.%20MODIS%20LST%20and%20Visualization/1.2%20MODIS%20LST%20Divided%20Global%20Coverage.txt

1.3 MODIS Satellite Image Visualization
Google Earth Engine Code Editor:
https://code.earthengine.google.com/d0d4b84d72ef78c535e87151903e6cc9
GitHub Repository: 
https://github.com/lerren144/UZH-Master-Thesis/blob/32b2d3cfb849a11779f093e3e67c9bb760159e1c/1.%20MODIS%20LST%20and%20Visualization/1.3%20MODIS%20Satellite%20Image%20Visualization.txt

2. Land Surface Temperature Scripts:
The folder contains all the scripts for LST Mosaicking, generating the LST Difference images, generating the LST Combination images, and extracting the LST from the LC - creating transition matrix.

2.1. MODIS LST Mosaicking Script (Pre-Processing):
The folder contains all the scripts used for mosaicking the MODIS LST (Land Surface Temperature) products exported from Google Earth Engine. These scripts ensure the proper merging of datasets into a single mosaic image for further analysis.
https://github.com/lerren144/UZH-Master-Thesis/tree/32b2d3cfb849a11779f093e3e67c9bb760159e1c/2.%20Land%20Surface%20Temperature%20Scripts/2.1.%20MODIS%20LST%20Mosaicking%20Script%20(Pre-Processing)

2.2. MODIS LST Difference Script:
The folder contains all the scripts used to calculate the differences between the mosaicked MODIS LST product images: End Period and Start Period. https://github.com/lerren144/UZH-Master-Thesis/tree/32b2d3cfb849a11779f093e3e67c9bb760159e1c/2.%20Land%20Surface%20Temperature%20Scripts/2.2.%20MODIS%20LST%20Difference%20Script%3A

2.3 MODIS LST Combination Script:
The folder contains all the scripts used to combine the mosaicked MODIS LST product images using three methods: Combination 1: Linear Regression Equation, Combination 2: Average MODIS Terra Aqua Day, Combination 3: Average MODIS Terra Aqua Night.
https://github.com/lerren144/UZH-Master-Thesis/tree/32b2d3cfb849a11779f093e3e67c9bb760159e1c/2.%20Land%20Surface%20Temperature%20Scripts/2.3%20MODIS%20LST%20Combination%20Script

2.4 LST-LC Transition Matrix Script:
The folder contains all the scripts used to extract LST values for each land cover mask. Additionally, the reference scripts include the trial-and-error scripts that were initially tested and refined during the development process.
https://github.com/lerren144/UZH-Master-Thesis/tree/f3a249aef9f44e5dd8b41a86bf1e29a3b394e7c9/2.%20Land%20Surface%20Temperature%20Scripts/2.4%20LST-LC%20Transition%20Matrix%20Script

3. Undisturbed Areas LST Extraction Script
The folder contains all the scripts used to extract LST values from the undisturbed land cover mask. Additionally, the reference scripts include the trial-and-error scripts that were initially tested and refined during the development process.
https://github.com/lerren144/UZH-Master-Thesis/tree/f3a249aef9f44e5dd8b41a86bf1e29a3b394e7c9/3.%20Undisturbed%20Areas%20LST%20Extraction%20Script

4. LST Visualization per Latitude Script
The folder contains all the scripts used to create visualization plots for extracting LST pixel values across different latitudes. These scripts are designed to analyze and represent the spatial distribution of LST data effectively in each latitude.
https://github.com/lerren144/UZH-Master-Thesis/tree/f3a249aef9f44e5dd8b41a86bf1e29a3b394e7c9/4.%20LST%20Visualization%20per%20Latitude%20Script

5. ESA CCI Land Cover Scripts:
The folder contains all the scripts used to extract the ESA CCI LC masks for disturbed and undisturbed areas, preprocess the LC masks, and generate various visualizations, including charts, transition matrices, bubble plots, and Sankey diagrams. These scripts play a crucial role in analyzing and visualizing land cover changes effectively.
https://github.com/lerren144/UZH-Master-Thesis/tree/329ce443f9a1fa1b4ee050b5693a6c5adce48af3/5.%20ESA%20CCI%20Land%20Cover%20Scripts

5.1. ESA CCI Land Cover Disturbed and Undisturbed Analysis (Extraction of Masks)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/5.%20ESA%20CCI%20Land%20Cover%20Scripts/5.1.%20%20ESACCI_LandCover_Analysis.ipynb

5.2. ESA CCI Land Cover Conversion from NETCDF4 to GeoTIFF (Pre-Processing)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/5.%20ESA%20CCI%20Land%20Cover%20Scripts/5.2.%20Conversion_ESACCILC_Geotiff.py

5.3. ESA CCI LC Before and After Bar Chart (Graph)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/5.%20ESA%20CCI%20Land%20Cover%20Scripts/5.3.%20ESACCI_LC_Before_After_BarChart_22x22.py

5.4. ESA CCI LC Transition Matrix (Table)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/5.%20ESA%20CCI%20Land%20Cover%20Scripts/5.4.%20ESACCI_LC_Transition_Matrix_22x22.ipynb

5.5. ESA CCI LC-LST Bubble Plot (Graph)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/5.%20ESA%20CCI%20Land%20Cover%20Scripts/5.5.%20ESACCI_LC_LST_BubblePlot_22x22.py

5.6. ESA CCI LC-LST Sankey Diagram (Graph)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/5.%20ESA%20CCI%20Land%20Cover%20Scripts/5.6.%20Sankey_Diagram_Copernicus_22x22.ipynb

6. MODIS Land Cover Scripts:
The folder contains all the scripts used to extract the MODIS LC masks for disturbed and undisturbed areas, preprocess the LC masks, and generate various visualizations, including charts, transition matrices, bubble plots, and Sankey diagrams. These scripts play a crucial role in analyzing and visualizing land cover changes effectively.
https://github.com/lerren144/UZH-Master-Thesis/tree/329ce443f9a1fa1b4ee050b5693a6c5adce48af3/6.%20MODIS%20Land%20Cover%20Scripts

6.1. MODIS Land Cover Disturbed and Undisturbed Analysis (Extraction of Masks)
https://colab.research.google.com/drive/1ANxziJ66DZ1oyW0K0LhR4e_a3DXLcO8h?usp=sharing
https://github.com/lerren144/UZH-Master-Thesis/tree/329ce443f9a1fa1b4ee050b5693a6c5adce48af3/6.%20MODIS%20Land%20Cover%20Scripts/6.1.%20MODIS%20Land%20Cover%20Disturbed%20and%20Undisturbed%20Analysis%20(Extraction%20of%20Masks)

6.2. MODIS LC Mosaicking Script (Pre-Processing)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/6.%20MODIS%20Land%20Cover%20Scripts/6.2.%20MODIS_LC_Mosaic_Script.py

6.3. MODIS LC Before and After Bar Chart (Graph)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/6.%20MODIS%20Land%20Cover%20Scripts/6.3.%20MODIS_LC_Before_After_BarChart_10x10.py

6.4. MODIS LC Transition Matrix (Table)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/6.%20MODIS%20Land%20Cover%20Scripts/6.4.%20MODIS_LC_Transtion_Matrix_10x10.ipynb

6.5. MODIS LC-LST Bubble Plot (Graph)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/6.%20MODIS%20Land%20Cover%20Scripts/6.5.%20MODIS_LC_LST_BubblePlot_10x10.py

6.6. MODIS LC-LST Sankey Diagram (Graph)
https://github.com/lerren144/UZH-Master-Thesis/blob/722d18aca23de02e8658ac09d0dc3ed51452de64/6.%20MODIS%20Land%20Cover%20Scripts/6.6.%20Sankey_Diagram_MODIS_10x10.ipynb
