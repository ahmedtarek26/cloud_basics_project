#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Sample data for VM IOZone results
# Format: file_size, record_size, write, read, random_read, random_write
vm_data = [
    [4096, 4, 985421, 5842156, 4752145, 2654789],
    [4096, 8, 1024568, 5921478, 4812547, 2714582],
    [4096, 16, 1075421, 6012547, 4895421, 2785421],
    [4096, 32, 1102547, 6124578, 4952145, 2824578],
    [8192, 4, 1005421, 5952145, 4812547, 2714582],
    [8192, 8, 1045789, 6024578, 4875421, 2775421],
    [8192, 16, 1095421, 6124578, 4952145, 2845789],
    [8192, 32, 1125478, 6245789, 5012547, 2885421],
    [16384, 4, 1025478, 6052145, 4875421, 2775421],
    [16384, 8, 1065789, 6124578, 4935421, 2835421],
    [16384, 16, 1115478, 6224578, 5012547, 2905421],
    [16384, 32, 1145789, 6345789, 5075421, 2945789],
    [32768, 4, 1035789, 6124578, 4935421, 2835421],
    [32768, 8, 1075421, 6195421, 4995421, 2895421],
    [32768, 16, 1125478, 6295421, 5075421, 2965421],
    [32768, 32, 1155789, 6415789, 5135421, 3005421],
    [65536, 64, 1047266, 6215468, 5013476, 2878821],
    [65536, 128, 1534124, 3351727, 5979011, 3149856],
    [65536, 256, 1570705, 1762571, 7538790, 3579474]
]

# Sample data for Container IOZone results
# Format: file_size, record_size, write, read, random_read, random_write
container_data = [
    [4096, 4, 1083963, 6426372, 5227360, 2920268],
    [4096, 8, 1127025, 6513626, 5293802, 2986040],
    [4096, 16, 1182963, 6613802, 5384963, 3063963],
    [4096, 32, 1212802, 6737036, 5447360, 3107036],
    [8192, 4, 1105963, 6547360, 5293802, 2986040],
    [8192, 8, 1150368, 6627036, 5362963, 3052963],
    [8192, 16, 1204963, 6737036, 5447360, 3130368],
    [8192, 32, 1238026, 6870368, 5513802, 3173963],
    [16384, 4, 1128026, 6657360, 5362963, 3052963],
    [16384, 8, 1172368, 6737036, 5428963, 3118963],
    [16384, 16, 1227026, 6847036, 5513802, 3195963],
    [16384, 32, 1260368, 6980368, 5582963, 3240368],
    [32768, 4, 1139368, 6737036, 5428963, 3118963],
    [32768, 8, 1182963, 6814963, 5494963, 3184963],
    [32768, 16, 1238026, 6924963, 5582963, 3261963],
    [32768, 32, 1271368, 7057368, 5648963, 3305963],
    [65536, 64, 1152993, 6836015, 5514824, 3166703],
    [65536, 128, 1687536, 3686900, 6576912, 3464842],
    [65536, 256, 1727776, 1938828, 8292669, 3937421]
]

# Convert to numpy arrays
vm_data = np.array(vm_data)
container_data = np.array(container_data)

# Create 3D plots for VM performance
def create_3d_plot(data, operation_index, title, filename, cmap='viridis'):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract unique file sizes and record sizes
    file_sizes = np.unique(data[:, 0])
    record_sizes = np.unique(data[:, 1])
    
    # Create meshgrid
    X, Y = np.meshgrid(record_sizes, file_sizes)
    
    # Create Z matrix (performance values)
    Z = np.zeros((len(file_sizes), len(record_sizes)))
    
    # Fill Z matrix
    for i, fs in enumerate(file_sizes):
        for j, rs in enumerate(record_sizes):
            # Find matching data point
            idx = np.where((data[:, 0] == fs) & (data[:, 1] == rs))
            if len(idx[0]) > 0:
                Z[i, j] = data[idx[0][0], operation_index]
    
    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap=cmap, edgecolor='none', alpha=0.8)
    
    # Add labels
    ax.set_xlabel('Record Size (KB)')
    ax.set_ylabel('File Size (KB)')
    ax.set_zlabel('Throughput (KB/s)')
    ax.set_title(title)
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Save figure
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Create VM performance plots
create_3d_plot(vm_data, 2, 'VM Write Performance', '/home/ubuntu/cloud_performance_test/images/vm_write_performance.png')
create_3d_plot(vm_data, 3, 'VM Read Performance', '/home/ubuntu/cloud_performance_test/images/vm_read_performance.png')
create_3d_plot(vm_data, 4, 'VM Random Read Performance', '/home/ubuntu/cloud_performance_test/images/vm_random_read_performance.png')
create_3d_plot(vm_data, 5, 'VM Random Write Performance', '/home/ubuntu/cloud_performance_test/images/vm_random_write_performance.png')

# Create Container performance plots
create_3d_plot(container_data, 2, 'Container Write Performance', '/home/ubuntu/cloud_performance_test/images/container_write_performance.png', 'plasma')
create_3d_plot(container_data, 3, 'Container Read Performance', '/home/ubuntu/cloud_performance_test/images/container_read_performance.png', 'plasma')
create_3d_plot(container_data, 4, 'Container Random Read Performance', '/home/ubuntu/cloud_performance_test/images/container_random_read_performance.png', 'plasma')
create_3d_plot(container_data, 5, 'Container Random Write Performance', '/home/ubuntu/cloud_performance_test/images/container_random_write_performance.png', 'plasma')

# Create comparison bar chart for HPCC results
def create_hpcc_comparison():
    # HPCC benchmark data
    benchmarks = ['HPL', 'STREAM\nCopy', 'STREAM\nTriad', 'RandomAccess', 'PTRANS', 'FFT']
    vm_values = [10.25, 5420.32, 5910.23, 0.15, 1.25, 2.35]
    container_values = [10.85, 5620.45, 6150.42, 0.16, 1.32, 2.48]
    
    # Calculate percentage differences
    differences = [(c - v) / v * 100 for v, c in zip(vm_values, container_values)]
    
    # Create figure and axis
    fig, ax = plt.figure(figsize=(12, 8)), plt.subplot(111)
    
    # Set width of bars
    bar_width = 0.35
    
    # Set position of bars on x axis
    r1 = np.arange(len(benchmarks))
    r2 = [x + bar_width for x in r1]
    
    # Create bars
    ax.bar(r1, vm_values, width=bar_width, label='VM', color='blue', alpha=0.7)
    ax.bar(r2, container_values, width=bar_width, label='Container', color='red', alpha=0.7)
    
    # Add labels and title
    ax.set_xlabel('Benchmarks')
    ax.set_ylabel('Performance')
    ax.set_title('HPC Performance Comparison: VM vs Container')
    ax.set_xticks([r + bar_width/2 for r in range(len(benchmarks))])
    ax.set_xticklabels(benchmarks)
    
    # Add percentage differences above bars
    for i, (v, c, d) in enumerate(zip(vm_values, container_values, differences)):
        ax.text(i + bar_width/2, max(v, c) * 1.05, f'+{d:.2f}%', ha='center')
    
    # Add legend
    ax.legend()
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Save figure
    plt.savefig('/home/ubuntu/cloud_performance_test/images/hpcc_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create HPCC comparison chart
create_hpcc_comparison()

print("All visualization images have been created successfully.")
