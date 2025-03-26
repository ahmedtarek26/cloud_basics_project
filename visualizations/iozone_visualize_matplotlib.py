#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

def extract_iozone_data(file_path):
    """
    Extract IOZone data from the results file
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the start of the write/rewrite table
    write_start = None
    for i, line in enumerate(lines):
        if "KB  reclen   write rewrite" in line:
            write_start = i
            break
    
    if write_start is None:
        print("Could not find write/rewrite table in the results file")
        return None
    
    # Extract data from the write/rewrite table
    data = []
    i = write_start + 1
    while i < len(lines) and lines[i].strip():
        parts = lines[i].split()
        if len(parts) >= 4:  # Ensure we have at least KB, reclen, write, rewrite
            try:
                kb = int(parts[0])
                reclen = int(parts[1])
                write = int(parts[2])
                rewrite = int(parts[3])
                data.append([kb, reclen, write, rewrite])
            except ValueError:
                pass  # Skip lines that can't be converted to integers
        i += 1
    
    # Find the start of the read/reread table
    read_start = None
    for i, line in enumerate(lines):
        if "KB  reclen    read reread" in line:
            read_start = i
            break
    
    if read_start is None:
        print("Could not find read/reread table in the results file")
        return None
    
    # Extract data from the read/reread table
    i = read_start + 1
    read_data = []
    while i < len(lines) and lines[i].strip():
        parts = lines[i].split()
        if len(parts) >= 4:  # Ensure we have at least KB, reclen, read, reread
            try:
                kb = int(parts[0])
                reclen = int(parts[1])
                read = int(parts[2])
                reread = int(parts[3])
                read_data.append([kb, reclen, read, reread])
            except ValueError:
                pass  # Skip lines that can't be converted to integers
        i += 1
    
    # Find the start of the random read/write table
    random_start = None
    for i, line in enumerate(lines):
        if "KB  reclen" in line and "random" in line:
            random_start = i
            break
    
    if random_start is None:
        print("Could not find random read/write table in the results file")
        return None
    
    # Extract data from the random read/write table
    i = random_start + 1
    random_data = []
    while i < len(lines) and lines[i].strip():
        parts = lines[i].split()
        if len(parts) >= 4:  # Ensure we have at least KB, reclen, random read, random write
            try:
                kb = int(parts[0])
                reclen = int(parts[1])
                random_read = int(parts[2])
                random_write = int(parts[3])
                random_data.append([kb, reclen, random_read, random_write])
            except ValueError:
                pass  # Skip lines that can't be converted to integers
        i += 1
    
    return {
        'write_data': np.array(data),
        'read_data': np.array(read_data),
        'random_data': np.array(random_data)
    }

def create_3d_plot(data, title, output_file, operation_index, zlabel):
    """
    Create a 3D surface plot of IOZone data
    """
    # Extract unique file sizes and record sizes
    file_sizes = np.unique(data[:, 0])
    record_sizes = np.unique(data[:, 1])
    
    # Create a grid of file sizes and record sizes
    X, Y = np.meshgrid(record_sizes, file_sizes)
    
    # Create a 2D array for the Z values (performance)
    Z = np.zeros((len(file_sizes), len(record_sizes)))
    
    # Fill in the Z values
    for i, file_size in enumerate(file_sizes):
        for j, record_size in enumerate(record_sizes):
            # Find the data point with this file size and record size
            mask = (data[:, 0] == file_size) & (data[:, 1] == record_size)
            if np.any(mask):
                Z[i, j] = data[mask, operation_index][0]
    
    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    
    # Add labels and title
    ax.set_xlabel('Record Size (KB)')
    ax.set_ylabel('File Size (KB)')
    ax.set_zlabel(zlabel)
    ax.set_title(title)
    
    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_comparison_plot(vm_data, container_data, output_file, operation_index, title, ylabel):
    """
    Create a bar chart comparing VM and container performance
    """
    # Calculate average performance for each file size
    vm_file_sizes = np.unique(vm_data[:, 0])
    container_file_sizes = np.unique(container_data[:, 0])
    
    # Use the intersection of file sizes
    file_sizes = np.intersect1d(vm_file_sizes, container_file_sizes)
    
    vm_avg = []
    container_avg = []
    
    for file_size in file_sizes:
        vm_mask = vm_data[:, 0] == file_size
        container_mask = container_data[:, 0] == file_size
        
        vm_avg.append(np.mean(vm_data[vm_mask, operation_index]))
        container_avg.append(np.mean(container_data[container_mask, operation_index]))
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(file_sizes))
    width = 0.35
    
    ax.bar(x - width/2, vm_avg, width, label='VM')
    ax.bar(x + width/2, container_avg, width, label='Container')
    
    ax.set_xlabel('File Size (KB)')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels([str(size) for size in file_sizes])
    ax.legend()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_html_visualization(vm_data, container_data, output_file):
    """
    Create an HTML file with all visualizations embedded
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>IOZone Performance Comparison: VMs vs Containers</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            h2 {
                color: #444;
                margin-top: 30px;
            }
            .plot-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin: 20px 0;
            }
            .plot {
                max-width: 45%;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-radius: 5px;
                padding: 10px;
                background: white;
            }
            .plot img {
                width: 100%;
                height: auto;
            }
            .comparison {
                max-width: 90%;
                margin: 30px auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-radius: 5px;
                padding: 10px;
                background: white;
            }
            .comparison img {
                width: 100%;
                height: auto;
            }
            .caption {
                text-align: center;
                font-style: italic;
                margin-top: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: right;
            }
            th {
                background-color: #f2f2f2;
                text-align: center;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>IOZone Performance Comparison: VMs vs Containers</h1>
        
        <h2>3D Performance Visualizations</h2>
        
        <div class="plot-container">
            <div class="plot">
                <img src="vm_write_performance.png" alt="VM Write Performance">
                <div class="caption">VM Write Performance</div>
            </div>
            <div class="plot">
                <img src="container_write_performance.png" alt="Container Write Performance">
                <div class="caption">Container Write Performance</div>
            </div>
        </div>
        
        <div class="plot-container">
            <div class="plot">
                <img src="vm_read_performance.png" alt="VM Read Performance">
                <div class="caption">VM Read Performance</div>
            </div>
            <div class="plot">
                <img src="container_read_performance.png" alt="Container Read Performance">
                <div class="caption">Container Read Performance</div>
            </div>
        </div>
        
        <div class="plot-container">
            <div class="plot">
                <img src="vm_random_read_performance.png" alt="VM Random Read Performance">
                <div class="caption">VM Random Read Performance</div>
            </div>
            <div class="plot">
                <img src="container_random_read_performance.png" alt="Container Random Read Performance">
                <div class="caption">Container Random Read Performance</div>
            </div>
        </div>
        
        <div class="plot-container">
            <div class="plot">
                <img src="vm_random_write_performance.png" alt="VM Random Write Performance">
                <div class="caption">VM Random Write Performance</div>
            </div>
            <div class="plot">
                <img src="container_random_write_performance.png" alt="Container Random Write Performance">
                <div class="caption">Container Random Write Performance</div>
            </div>
        </div>
        
        <h2>Performance Comparisons</h2>
        
        <div class="comparison">
            <img src="write_comparison.png" alt="Write Performance Comparison">
            <div class="caption">Write Performance Comparison</div>
        </div>
        
        <div class="comparison">
            <img src="read_comparison.png" alt="Read Performance Comparison">
            <div class="caption">Read Performance Comparison</div>
        </div>
        
        <div class="comparison">
            <img src="random_read_comparison.png" alt="Random Read Performance Comparison">
            <div class="caption">Random Read Performance Comparison</div>
        </div>
        
        <div class="comparison">
            <img src="random_write_comparison.png" alt="Random Write Performance Comparison">
            <div class="caption">Random Write Performance Comparison</div>
        </div>
        
        <h2>Performance Summary</h2>
        
        <table>
            <tr>
                <th>Operation</th>
                <th>VM Average (KB/s)</th>
                <th>Container Average (KB/s)</th>
                <th>Difference (%)</th>
            </tr>
            <tr>
                <td>Write</td>
                <td id="vm-write-avg"></td>
                <td id="container-write-avg"></td>
                <td id="write-diff"></td>
            </tr>
            <tr>
                <td>Read</td>
                <td id="vm-read-avg"></td>
                <td id="container-read-avg"></td>
                <td id="read-diff"></td>
            </tr>
            <tr>
                <td>Random Read</td>
                <td id="vm-random-read-avg"></td>
                <td id="container-random-read-avg"></td>
                <td id="random-read-diff"></td>
            </tr>
            <tr>
                <td>Random Write</td>
                <td id="vm-random-write-avg"></td>
                <td id="container-random-write-avg"></td>
                <td id="random-write-diff"></td>
            </tr>
        </table>
        
        <script>
            // Calculate averages and differences
            const vmWriteAvg = {vm_write_avg};
            const containerWriteAvg = {container_write_avg};
            const writeDiff = ((containerWriteAvg - vmWriteAvg) / vmWriteAvg * 100).toFixed(2);
            
            const vmReadAvg = {vm_read_avg};
            const containerReadAvg = {container_read_avg};
            const readDiff = ((containerReadAvg - vmReadAvg) / vmReadAvg * 100).toFixed(2);
            
            const vmRandomReadAvg = {vm_random_read_avg};
            const containerRandomReadAvg = {container_random_read_avg};
            const randomReadDiff = ((containerRandomReadAvg - vmRandomReadAvg) / vmRandomReadAvg * 100).toFixed(2);
            
            const vmRandomWriteAvg = {vm_random_write_avg};
            const containerRandomWriteAvg = {container_random_write_avg};
            const randomWriteDiff = ((containerRandomWriteAvg - vmRandomWriteAvg) / vmRandomWriteAvg * 100).toFixed(2);
            
            // Update the table
            document.getElementById('vm-write-avg').textContent = vmWriteAvg.toFixed(2);
            document.getElementById('container-write-avg').textContent = containerWriteAvg.toFixed(2);
            document.getElementById('write-diff').textContent = writeDiff + '%';
            
            document.getElementById('vm-read-avg').textContent = vmReadAvg.toFixed(2);
            document.getElementById('container-read-avg').textContent = containerReadAvg.toFixed(2);
            document.getElementById('read-diff').textContent = readDiff + '%';
            
            document.getElementById('vm-random-read-avg').textContent = vmRandomReadAvg.toFixed(2);
            document.getElementById('container-random-read-avg').textContent = containerRandomReadAvg.toFixed(2);
            document.getElementById('random-read-diff').textContent = randomReadDiff + '%';
            
            document.getElementById('vm-random-write-avg').textContent = vmRandomWriteAvg.toFixed(2);
            document.getElementById('container-random-write-avg').textContent = containerRandomWriteAvg.toFixed(2);
            document.getElementById('random-write-diff').textContent = randomWriteDiff + '%';
        </script>
    </body>
    </html>
    """
    
    # Calculate averages for the summary table
    vm_write_avg = np.mean(vm_data['write_data'][:, 2])
    container_write_avg = np.mean(container_data['write_data'][:, 2])
    
    vm_read_avg = np.mean(vm_data['read_data'][:, 2])
    container_read_avg = np.mean(container_data['read_data'][:, 2])
    
    vm_random_read_avg = np.mean(vm_data['random_data'][:, 2])
    container_random_read_avg = np.mean(container_data['random_data'][:, 2])
    
    vm_random_write_avg = np.mean(vm_data['random_data'][:, 3])
    container_random_write_avg = np.mean(container_data['random_data'][:, 3])
    
    # Replace placeholders with actual values
    html_content = html_content.format(
        vm_write_avg=vm_write_avg,
        container_write_avg=container_write_avg,
        vm_read_avg=vm_read_avg,
        container_read_avg=container_read_avg,
        vm_random_read_avg=vm_random_read_avg,
        container_random_read_avg=container_random_read_avg,
        vm_random_write_avg=vm_random_write_avg,
        container_random_write_avg=container_random_write_avg
    )
    
    # Write the HTML file
    with open(output_file, 'w') as f:
        f.write(html_content)

def main():
    if len(sys.argv) < 3:
        print("Usage: python iozone_visualize.py <vm_results_file> <container_results_file>")
        sys.exit(1)
    
    vm_results_file = sys.argv[1]
    container_results_file = sys.argv[2]
    
    # Create output directory if it doesn't exist
    output_dir = "visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract data from IOZone results
    vm_data = extract_iozone_data(vm_results_file)
    container_data = extract_iozone_data(container_results_file)
    
    if vm_data is None or container_data is None:
        print("Failed to extract data from IOZone results files")
        sys.exit(1)
    
    # Create 3D plots for VM performance
    create_3d_plot(
        vm_data['write_data'],
        "VM Write Performance",
        os.path.join(output_dir, "vm_write_performance.png"),
        2,
        "Write Throughput (KB/s)"
    )
    
    create_3d_plot(
        vm_data['read_data'],
        "VM Read Performance",
        os.path.join(output_dir, "vm_read_performance.png"),
        2,
        "Read Throughput (KB/s)"
    )
    
    create_3d_plot(
        vm_data['random_data'],
        "VM Random Read Performance",
        os.path.join(output_dir, "vm_random_read_performance.png"),
        2,
        "Random Read Throughput (KB/s)"
    )
    
    create_3d_plot(
        vm_data['random_data'],
        "VM Random Write Performance",
        os.path.join(output_dir, "vm_random_write_performance.png"),
        3,
        "Random Write Throughput (KB/s)"
    )
    
    # Create 3D plots for Container performance
    create_3d_plot(
        container_data['write_data'],
        "Container Write Performance",
        os.path.join(output_dir, "container_write_performance.png"),
        2,
        "Write Throughput (KB/s)"
    )
    
    create_3d_plot(
        container_data['read_data'],
        "Container Read Performance",
        os.path.join(output_dir, "container_read_performance.png"),
        2,
        "Read Throughput (KB/s)"
    )
    
    create_3d_plot(
        container_data['random_data'],
        "Container Random Read Performance",
        os.path.join(output_dir, "container_random_read_performance.png"),
        2,
        "Random Read Throughput (KB/s)"
    )
    
    create_3d_plot(
        container_data['random_data'],
        "Container Random Write Performance",
        os.path.join(output_dir, "container_random_write_performance.png"),
        3,
        "Random Write Throughput (KB/s)"
    )
    
    # Create comparison plots
    create_comparison_plot(
        vm_data['write_data'],
        container_data['write_data'],
        os.path.join(output_dir, "write_comparison.png"),
        2,
        "Write Performance Comparison",
        "Write Throughput (KB/s)"
    )
    
    create_comparison_plot(
        vm_data['read_data'],
        container_data['read_data'],
        os.path.join(output_dir, "read_comparison.png"),
        2,
        "Read Performance Comparison",
        "Read Throughput (KB/s)"
    )
    
    create_comparison_plot(
        vm_data['random_data'],
        container_data['random_data'],
        os.path.join(output_dir, "random_read_comparison.png"),
        2,
        "Random Read Performance Comparison",
        "Random Read Throughput (KB/s)"
    )
    
    create_comparison_plot(
        vm_data['random_data'],
        container_data['random_data'],
        os.path.join(output_dir, "random_write_comparison.png"),
        3,
        "Random Write Performance Comparison",
        "Random Write Throughput (KB/s)"
    )
    
    # Create HTML visualization
    create_html_visualization(
        vm_data,
        container_data,
        os.path.join(output_dir, "iozone_3d_visualization.html")
    )
    
    print(f"Visualizations created in {output_dir} directory")
    print(f"Open {os.path.join(output_dir, 'iozone_3d_visualization.html')} to view the results")

if __name__ == "__main__":
    main()
