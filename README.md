# Geospatial Grid Assignment using the Hungarian Algorithm

This repository provides Python code to transform geospatial polygons (e.g., states, counties, or other administrative boundaries) into regular or hexagonal grids. It assigns each original polygon to a grid cell using the Hungarian Algorithm to minimize the total distance between centroids. This process is useful for creating cartograms or spatial visualizations where uniform grid cells are preferred over irregular polygons.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Preparation](#data-preparation)
  - [Running the Script](#running-the-script)
  - [Parameters](#parameters)
- [Code Explanation](#code-explanation)
  - [1. Load Geospatial Data](#1-load-geospatial-data)
  - [2. Grid Generation](#2-grid-generation)
    - [Hexagonal Grid Generation](#hexagonal-grid-generation)
  - [3. Assignment using the Hungarian Algorithm](#3-assignment-using-the-hungarian-algorithm)
  - [4. Saving and Visualizing Results](#4-saving-and-visualizing-results)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

When visualizing geospatial data, using irregular polygons can sometimes mislead the audience due to varying sizes and shapes of the areas. Transforming these polygons into a regular grid (square or hexagonal) ensures uniform representation and avoids visual bias.

This project automates the process of:

- Generating regular or hexagonal grids over a given geographic area.
- Assigning original polygons to grid cells based on centroid proximity using the Hungarian Algorithm.
- Providing multiple grid assignments with slight variations to choose the best fit.

## Features

- **Automated Grid Generation**: Create regular or hexagonal grids covering your area of interest.
- **Optimal Assignment**: Use the Hungarian Algorithm to assign original polygons to grid cells, minimizing centroid distances.
- **Multiple Assignments**: Generate multiple grid variations with random offsets to select the most suitable one.
- **Flexible Parameters**: Adjust grid cell sizes and the number of assignments according to your needs.
- **Visualization**: Optional plotting of the assigned grids for quick inspection.
- **Output Formats**: Save the assigned grids as GeoJSON or Shapefiles for further use.

## Requirements

- Python 3.6 or higher
- Packages:
  - `geopandas`
  - `numpy`
  - `shapely`
  - `scipy`
  - `matplotlib`

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install geopandas numpy shapely scipy matplotlib
   ```

## Usage

### Data Preparation

- **Input Data**: Prepare your geospatial data file (e.g., Shapefile, GeoJSON) containing the polygons you wish to transform.
- **Coordinate Reference System (CRS)**: Ensure your data is projected in a suitable CRS for distance calculations (e.g., EPSG:3857). Geographic coordinates (latitude and longitude) may not provide accurate distance measurements.

### Running the Script

1. **Place Your Data File**: Ensure your data file is accessible, and note its path (e.g., `data/your_file.shp`).

2. **Update the Script**:

   - **Data File Path**: Replace `'your_file.shp'` in the script with the path to your data file.

     ```python
     gdf = gpd.read_file('data/your_file.shp')
     ```

   - **Attribute for Visualization**: Replace `'your_attribute'` with a valid column name from your data for coloring the grid during visualization.

     ```python
     assigned_grid.plot(ax=ax, column='your_attribute', cmap='viridis', edgecolor='black')
     ```

3. **Adjust Parameters** (Optional):

   - **Grid Cell Size**: Modify the `size` variable to control the hexagon size.

     ```python
     size = 50000  # Adjust based on your data's scale
     ```

   - **Number of Assignments**: Change `num_assignments` to generate more or fewer grid variations.

     ```python
     num_assignments = 5  # Number of different grids to generate
     ```

4. **Run the Script**:

   Execute the script in your Python environment:

   ```bash
   python grid_assignment.py
   ```

### Parameters

- **Grid Type**: The script currently generates hexagonal grids. You can modify it to generate square grids by adjusting the grid generation function.
- **Cell Size (`size`)**: Determines the dimensions of the hexagons. Larger sizes result in fewer, larger hexagons.
- **Number of Assignments (`num_assignments`)**: Number of grid variations to generate with random offsets.
- **Random Offsets**: Introduces slight shifts in the grid to produce different assignments.

## Code Explanation

### 1. Load Geospatial Data

```python
gdf = gpd.read_file('your_file.shp')
gdf = gdf.to_crs(epsg=3857)
```

- **Load Data**: Reads the geospatial data file into a GeoDataFrame.
- **Project Data**: Reprojects the data to a suitable CRS for accurate distance calculations.

### 2. Grid Generation

#### Hexagonal Grid Generation

```python
def create_hex_grid(gdf, size, offset_x=0, offset_y=0):
    # Grid generation logic...
```

- **Parameters**:
  - `size`: Radius of the hexagons.
  - `offset_x`, `offset_y`: Random offsets to shift the grid.
- **Hexagon Spacing**:
  - **Horizontal (`dx`)**: \(1.5 \times \text{size}\).
  - **Vertical (`dy`)**: \(\sqrt{3} \times \text{size}\).
- **Grid Creation**: Iterates over columns and rows to create hexagon polygons.

### 3. Assignment using the Hungarian Algorithm

```python
def assign_and_save_grid(gdf, grid, iteration, output_dir):
    # Centroid calculations...
    # Cost matrix computation...
    # Assignment using linear_sum_assignment...
    # Saving the assigned grid...
```

- **Centroid Calculation**: Computes centroids of original polygons and grid cells.
- **Cost Matrix**: Calculates the Euclidean distances between centroids.
- **Optimal Assignment**: Uses `linear_sum_assignment` from `scipy.optimize` to minimize total distance.
- **Data Joining**: Merges attributes from the original data to the assigned grid cells.
- **Saving Output**: Writes the assigned grid to a GeoJSON file.

### 4. Saving and Visualizing Results

- **Output Directory**: Assigned grids are saved in the `assigned_grids_hex` directory.
- **Visualization**: Optionally plots each assigned grid for inspection.

## Examples

**Generating 3 Hexagonal Grid Assignments with Cell Size 100,000 Units**

1. **Adjust Parameters**:

   ```python
   num_assignments = 3
   size = 100000
   ```

2. **Run the Script**:

   ```bash
   python grid_assignment.py
   ```

3. **Results**:

   - Three GeoJSON files will be saved in `assigned_grids_hex`.
   - Use GIS software to open and compare the grids.

**Visualizing the First Assigned Grid**

```python
assigned_grid = assigned_grids[0]
fig, ax = plt.subplots(figsize=(10, 10))
assigned_grid.boundary.plot(ax=ax, edgecolor='black')
assigned_grid.plot(ax=ax, column='population', cmap='viridis', alpha=0.5)
gdf.boundary.plot(ax=ax, edgecolor='red')
ax.set_title('Assigned Hex Grid with Original Boundaries')
ax.axis('off')
plt.show()
```

- **Visualization Details**:
  - **Assigned Grid**: Displayed with semi-transparent fill and black edges.
  - **Original Polygons**: Boundaries overlaid in red.

## Troubleshooting

- **Overlapping Hexagons**:
  - Ensure the `size` parameter and spacing calculations are correct.
  - Use the corrected `create_hex_grid` function provided.

- **Not Enough Grid Cells**:
  - Reduce the `size` parameter to create more grid cells.
  - Increase the number of columns and rows in the grid generation.

- **Multiple Geometry Columns Error**:
  - Ensure only one geometry column exists before saving the GeoDataFrame.
  - Modify the data joining process to exclude extra geometry columns.

- **Attribute Errors in Visualization**:
  - Verify that the attribute used for coloring exists in your data.
  - Replace `'your_attribute'` with a valid column name.

- **Projection Issues**:
  - Confirm that all geospatial data layers are in the same CRS.
  - Reproject data as necessary using `to_crs`.

## Contributing

Contributions are welcome! If you find a bug or have a suggestion, please open an issue or submit a pull request.

**To contribute:**

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note**: Always ensure you have the rights and permissions to use and share the geospatial data you are working with.

**Acknowledgments**:

- The use of the Hungarian Algorithm (`linear_sum_assignment`) from `scipy.optimize`.
- Geospatial processing capabilities provided by `geopandas` and `shapely`.
