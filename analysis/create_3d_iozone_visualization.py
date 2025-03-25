import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import matplotlib.cm as cmx

# Create directories for visualizations
import os
os.makedirs('/home/ubuntu/cloud_performance_test/visualizations', exist_ok=True)

# Create sample data for IOZone visualization
# In a real scenario, we would parse the actual IOZone results
file_sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
record_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Create a meshgrid for the 3D surface
X, Y = np.meshgrid(record_sizes, file_sizes)

# Create random data for demonstration (would be replaced with actual parsed data)
np.random.seed(42)  # For reproducibility
Z = np.random.randint(50000, 300000, size=(len(file_sizes), len(record_sizes)))

# Create a stepped appearance by rounding values to specific bands
# This will create the color bands similar to the reference image
Z_bands = np.zeros_like(Z)
bands = [50000, 75000, 100000, 125000, 150000, 175000, 200000, 225000, 250000, 275000, 300000]
band_colors = ['#330066', '#660099', '#9900CC', '#CC00FF', '#FF00CC', '#FF0099', '#FF0066', '#FF0033', '#FF3300', '#FF6600', '#FF9900']

for i in range(len(file_sizes)):
    for j in range(len(record_sizes)):
        for k in range(len(bands)-1):
            if Z[i, j] >= bands[k] and Z[i, j] < bands[k+1]:
                Z_bands[i, j] = k
                break
            if Z[i, j] >= bands[-1]:
                Z_bands[i, j] = len(bands)-1

# Create the 3D plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Create a custom colormap with the specific colors
cmap = colors.ListedColormap(band_colors)
norm = colors.BoundaryNorm(np.arange(len(bands)+1)-0.5, cmap.N)

# Plot the surface with a stepped appearance
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, 
                      facecolors=cmap(norm(Z_bands)),
                      linewidth=1, antialiased=True, shade=False)

# Add a color bar
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), 
                   ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Write Performance (KB/sec)')
cbar.set_ticks(np.arange(len(bands)))
cbar.set_ticklabels([f'{bands[i]}-{bands[i+1]}' if i < len(bands)-1 else f'>{bands[i]}' for i in range(len(bands)-1)])

# Set labels and title
ax.set_xlabel('Record Size (KB)')
ax.set_ylabel('File Size (KB)')
ax.set_zlabel('Write Performance (KB/sec)')
ax.set_title('IOZone Write Performance', fontsize=16)

# Set the viewing angle to match the reference image
ax.view_init(elev=30, azim=-45)

# Set the axis ticks
ax.set_xticks(record_sizes)
ax.set_yticks(file_sizes)
ax.set_zticks(bands)

# Add a grid
ax.grid(True)

# Save the figure
plt.savefig('/home/ubuntu/cloud_performance_test/visualizations/iozone_3d_write_perf.png', 
           dpi=300, bbox_inches='tight')
plt.close()

print("3D IOZone visualization created successfully in /home/ubuntu/cloud_performance_test/visualizations/iozone_3d_write_perf.png")
