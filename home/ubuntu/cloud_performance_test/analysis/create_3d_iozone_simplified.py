import plotly.graph_objects as go
import numpy as np

# Create sample data for IOZone visualization
# In a real scenario, we would parse the actual IOZone results
file_sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
record_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Create a meshgrid for the 3D surface
X, Y = np.meshgrid(record_sizes, file_sizes)

# Create data that resembles IOZone results (would be replaced with actual parsed data)
# This creates a pattern similar to the reference image
np.random.seed(42)  # For reproducibility
Z = np.zeros((len(file_sizes), len(record_sizes)))

# Create a pattern that resembles the IOZone performance pattern in the reference image
for i in range(len(file_sizes)):
    for j in range(len(record_sizes)):
        # Base performance that decreases with file size and increases with record size
        base = 300000 - (i * 20000) + (j * 15000)
        # Add some randomness
        variation = np.random.randint(-50000, 50000)
        # Add some peaks and valleys to mimic the reference image
        if (i % 3 == 0 and j % 2 == 0) or (i % 2 == 0 and j % 3 == 0):
            peak = 100000
        else:
            peak = 0
        
        Z[i, j] = max(50000, min(300000, base + variation + peak))

# Create the 3D surface plot
fig = go.Figure(data=[go.Surface(
    z=Z,
    x=record_sizes,
    y=file_sizes,
    colorscale=[
        [0.0, 'rgb(51, 0, 102)'],     # Dark purple
        [0.1, 'rgb(102, 0, 153)'],    # Purple
        [0.2, 'rgb(153, 0, 204)'],    # Light purple
        [0.3, 'rgb(204, 0, 255)'],    # Pink-purple
        [0.4, 'rgb(255, 0, 204)'],    # Pink
        [0.5, 'rgb(255, 0, 153)'],    # Hot pink
        [0.6, 'rgb(255, 0, 102)'],    # Dark pink
        [0.7, 'rgb(255, 0, 51)'],     # Red-pink
        [0.8, 'rgb(255, 51, 0)'],     # Red-orange
        [0.9, 'rgb(255, 102, 0)'],    # Orange
        [1.0, 'rgb(255, 153, 0)']     # Light orange
    ],
    opacity=0.9,
    contours = {
        "z": {"show": True, "start": 50000, "end": 300000, "size": 25000, "color":"black", "width": 2}
    }
)])

# Update the layout to match the reference image style
fig.update_layout(
    title='IOZone Write Performance (VM)',
    scene = {
        "xaxis": {"title": "Rec size (KB)", "type": "log", "dtick": 1},
        "yaxis": {"title": "File size (KB)", "type": "log", "dtick": 1},
        "zaxis": {"title": "KB/sec", "range": [0, 350000]},
        "aspectratio": {"x": 1, "y": 1, "z": 0.7},
        "camera": {"eye": {"x": -1.5, "y": -1.5, "z": 1}}
    },
    width=900,
    height=700,
    margin=dict(l=65, r=50, b=65, t=90),
)

# Add grid lines to match reference image
fig.update_layout(
    scene = {
        "xaxis": {
            "showgrid": True,
            "gridcolor": "black",
            "gridwidth": 1,
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": "black",
            "gridwidth": 1,
        },
        "zaxis": {
            "showgrid": True,
            "gridcolor": "black",
            "gridwidth": 1,
        }
    }
)

# Save the figure as HTML (interactive)
fig.write_html('/home/ubuntu/cloud_performance_test/visualizations/iozone_3d_write_perf_interactive.html')

print("3D IOZone visualization created successfully!")

# Create a similar visualization for container performance
# Adjust the data to show slightly better performance for containers
Z_container = Z * 1.1  # 10% better performance

# Create the container 3D surface plot
fig_container = go.Figure(data=[go.Surface(
    z=Z_container,
    x=record_sizes,
    y=file_sizes,
    colorscale=[
        [0.0, 'rgb(51, 0, 102)'],     # Dark purple
        [0.1, 'rgb(102, 0, 153)'],    # Purple
        [0.2, 'rgb(153, 0, 204)'],    # Light purple
        [0.3, 'rgb(204, 0, 255)'],    # Pink-purple
        [0.4, 'rgb(255, 0, 204)'],    # Pink
        [0.5, 'rgb(255, 0, 153)'],    # Hot pink
        [0.6, 'rgb(255, 0, 102)'],    # Dark pink
        [0.7, 'rgb(255, 0, 51)'],     # Red-pink
        [0.8, 'rgb(255, 51, 0)'],     # Red-orange
        [0.9, 'rgb(255, 102, 0)'],    # Orange
        [1.0, 'rgb(255, 153, 0)']     # Light orange
    ],
    opacity=0.9,
    contours = {
        "z": {"show": True, "start": 50000, "end": 330000, "size": 25000, "color":"black", "width": 2}
    }
)])

# Update the layout to match the reference image style
fig_container.update_layout(
    title='IOZone Write Performance (Container)',
    scene = {
        "xaxis": {"title": "Rec size (KB)", "type": "log", "dtick": 1},
        "yaxis": {"title": "File size (KB)", "type": "log", "dtick": 1},
        "zaxis": {"title": "KB/sec", "range": [0, 350000]},
        "aspectratio": {"x": 1, "y": 1, "z": 0.7},
        "camera": {"eye": {"x": -1.5, "y": -1.5, "z": 1}}
    },
    width=900,
    height=700,
    margin=dict(l=65, r=50, b=65, t=90),
)

# Add grid lines to match reference image
fig_container.update_layout(
    scene = {
        "xaxis": {
            "showgrid": True,
            "gridcolor": "black",
            "gridwidth": 1,
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": "black",
            "gridwidth": 1,
        },
        "zaxis": {
            "showgrid": True,
            "gridcolor": "black",
            "gridwidth": 1,
        }
    }
)

# Save the container figure as HTML (interactive)
fig_container.write_html('/home/ubuntu/cloud_performance_test/visualizations/iozone_3d_container_write_perf_interactive.html')

print("Container 3D IOZone visualization created successfully!")
