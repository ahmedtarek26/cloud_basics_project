#!/bin/bash

# This script runs IOZone tests on both VMs and containers
# using the command specified by the user: iozone -a -R -O | tee iozone_results.txt
# and generates 3D visualizations of the results

# Create results directory
mkdir -p /shared/results

# ===== Run IOZone on VMs =====

echo "Running IOZone test on VMs..."
cd /shared
iozone -a -R -O | tee /shared/results/vm_iozone_results.txt

# ===== Run IOZone on Containers =====

echo "Running IOZone test on containers..."
docker exec Master bash -c "cd /shared && iozone -a -R -O | tee /shared/results/container_iozone_results.txt"

# ===== Generate Visualizations =====

echo "Generating IOZone visualizations..."

# Generate 3D visualization using Plotly
python3 /home/ubuntu/cloud_performance_test/visualizations/generate_iozone_visualization.py /shared/results/vm_iozone_results.txt /shared/results/container_iozone_results.txt

# Generate alternative visualization using Matplotlib
python3 /home/ubuntu/cloud_performance_test/visualizations/iozone_visualize_matplotlib.py /shared/results/vm_iozone_results.txt /shared/results/container_iozone_results.txt

# Move generated files to results directory
mv iozone_3d_visualization.html /shared/results/
mv iozone_comparison.html /shared/results/

# Check if Matplotlib visualization files were created
if [ -d "visualizations" ]; then
    cp -r visualizations/* /shared/results/
fi

echo "IOZone testing completed. Results are available in /shared/results/"
echo "3D Visualization: /shared/results/iozone_3d_visualization.html"
echo "Comparison Visualization: /shared/results/iozone_comparison.html"
