# Import necessary libraries
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
import os

# Suppress warnings for clean output
import warnings
warnings.filterwarnings('ignore')

# Step 1: Load Your Geospatial Data
gdf = gpd.read_file('/Users/behnamebrahimi/Codes/MAP/MSOA_2021_EW_BFC_V7/MSOA_2021_EW_BFC_V7.shp')  # Replace with your data file path

# Ensure projected CRS for accurate distance calculations
gdf = gdf.to_crs(epsg=3857)  # You can change the EPSG code to suit your data

# Function to create a hexagonal grid with random offsets
def create_hex_grid(gdf, size, offset_x=0, offset_y=0):
    from math import sqrt

    bounds = gdf.total_bounds
    xmin, ymin, xmax, ymax = bounds

    # Apply random offsets
    xmin += offset_x
    ymin += offset_y

    # Hexagon parameters
    w = size * 2  # Width of hexagon (flat sides)
    h = sqrt(3) * size  # Height of hexagon

    dx = 1.5 * size  # Horizontal spacing between hexagon centers
    dy = h  # Vertical spacing between hexagon centers

    # Number of columns and rows needed
    cols = int(np.ceil((xmax - xmin) / dx)) + 2
    rows = int(np.ceil((ymax - ymin) / dy)) + 2

    # Generate grid cells
    grid_cells = []
    for col in range(cols):
        for row in range(rows):
            x = xmin + col * dx
            y = ymin + row * dy
            if col % 2 == 1:
                y += dy / 2  # Offset every other column

            hex_cell = create_hexagon(x, y, size)
            grid_cells.append(hex_cell)

    grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs=gdf.crs)
    return grid

def create_hexagon(x_center, y_center, size):
    angles = np.arange(0, 360, 60)
    angles_rad = np.deg2rad(angles)
    x_hex = x_center + size * np.cos(angles_rad)
    y_hex = y_center + size * np.sin(angles_rad)
    return Polygon(zip(x_hex, y_hex))

# Function to perform assignment and save output
def assign_and_save_grid(gdf, grid, iteration, output_dir):
    # Step 3: Calculate Centroids without adding them as columns
    # Original centroids
    orig_centroids_geom = gdf.geometry.centroid
    orig_centroids = np.array(list(zip(orig_centroids_geom.x, orig_centroids_geom.y)))

    # Grid centroids
    grid_centroids_geom = grid.geometry.centroid
    grid_centroids = np.array(list(zip(grid_centroids_geom.x, grid_centroids_geom.y)))

    # Step 4: Compute the Cost Matrix
    cost_matrix = cdist(orig_centroids, grid_centroids, 'euclidean')

    # Step 5: Apply the Hungarian Algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Step 6: Reassign Polygons to Grid Cells
    assigned_grid = grid.iloc[col_ind].reset_index(drop=True)

    # Assign original data attributes to the grid cells
    # Exclude any geometry columns from gdf
    geom_columns = gdf.select_dtypes(include='geometry').columns.tolist()
    non_geom_columns = gdf.columns.difference(geom_columns)
    assigned_grid = assigned_grid.join(gdf[non_geom_columns].reset_index(drop=True))

    # Ensure only one geometry column
    assigned_grid = assigned_grid.loc[:, ~assigned_grid.columns.duplicated()]
    assigned_grid = assigned_grid.drop(columns=geom_columns[1:], errors='ignore')

    # Step 7: Save the Assigned Grid
    output_filename = os.path.join(output_dir, f'assigned_grid_{iteration}.geojson')
    assigned_grid.to_file(output_filename, driver='GeoJSON')
    print(f"Assigned grid saved to {output_filename}")

    return assigned_grid

# Create an output directory to store the results
output_dir = '/Users/behnamebrahimi/Codes/MAP/MSOA_2021_EW_BFC_V7/assigned_grids_hex/'
os.makedirs(output_dir, exist_ok=True)

# Number of different assignments to generate
num_assignments = 5 # Adjust as needed

# Adjust size based on your data's scale
size = 5000  # Adjust this value as needed

assigned_grids = []

for i in range(num_assignments):
    # Generate random offsets within one cell spacing
    offset_x = np.random.uniform(0, 1.5 * size)
    offset_y = np.random.uniform(0, np.sqrt(3) * size)

    # Generate the grid with random offsets
    grid = create_hex_grid(gdf, size, offset_x, offset_y)

    # Ensure there are enough grid cells
    if len(grid) < len(gdf):
        print(f"Iteration {i+1}: Not enough grid cells. Adjusting size or offsets.")
        continue

    # Perform assignment and save the result
    assigned_grid = assign_and_save_grid(gdf, grid, i+1, output_dir)
    assigned_grids.append(assigned_grid)

# Optional: Visualize the assigned grids
for idx, assigned_grid in enumerate(assigned_grids):
    fig, ax = plt.subplots(figsize=(10, 10))
    assigned_grid.plot(ax=ax, cmap='viridis', edgecolor='black')
    ax.set_title(f'Assigned Hex Grid {idx+1}')
    ax.axis('off')
    plt.show()
