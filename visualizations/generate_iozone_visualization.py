#!/usr/bin/env python3

import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

def parse_iozone_results(file_path):
    """
    Parse IOZone results file and extract performance data
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract the write and read tables
    write_pattern = r"[\s\d]+\s+reclen\s+write\s+rewrite[\s\d]+"
    read_pattern = r"[\s\d]+\s+reclen\s+read\s+reread[\s\d]+"
    random_pattern = r"[\s\d]+\s+reclen\s+.*random\s+random[\s\d]+"
    
    write_match = re.search(write_pattern, content)
    read_match = re.search(read_pattern, content)
    random_match = re.search(random_pattern, content)
    
    results = {}
    
    # Process write data
    if write_match:
        write_data = write_match.group(0)
        lines = write_data.strip().split('\n')
        
        # Extract headers and data
        headers = lines[0].split()
        data_rows = [line.split() for line in lines[1:]]
        
        # Create DataFrame
        write_df = pd.DataFrame(data_rows, columns=headers)
        write_df = write_df.apply(pd.to_numeric, errors='ignore')
        
        # Reshape for 3D visualization
        file_sizes = write_df['kB'].unique()
        record_sizes = []
        write_values = []
        rewrite_values = []
        
        for file_size in file_sizes:
            file_df = write_df[write_df['kB'] == file_size]
            record_sizes = file_df['reclen'].tolist()
            write_values.append(file_df['write'].tolist())
            rewrite_values.append(file_df['rewrite'].tolist())
        
        results['write'] = {
            'file_sizes': file_sizes,
            'record_sizes': record_sizes,
            'write_values': write_values,
            'rewrite_values': rewrite_values
        }
    
    # Process read data
    if read_match:
        read_data = read_match.group(0)
        lines = read_data.strip().split('\n')
        
        # Extract headers and data
        headers = lines[0].split()
        data_rows = [line.split() for line in lines[1:]]
        
        # Create DataFrame
        read_df = pd.DataFrame(data_rows, columns=headers)
        read_df = read_df.apply(pd.to_numeric, errors='ignore')
        
        # Reshape for 3D visualization
        file_sizes = read_df['kB'].unique()
        record_sizes = []
        read_values = []
        reread_values = []
        
        for file_size in file_sizes:
            file_df = read_df[read_df['kB'] == file_size]
            record_sizes = file_df['reclen'].tolist()
            read_values.append(file_df['read'].tolist())
            reread_values.append(file_df['reread'].tolist())
        
        results['read'] = {
            'file_sizes': file_sizes,
            'record_sizes': record_sizes,
            'read_values': read_values,
            'reread_values': reread_values
        }
    
    # Process random data
    if random_match:
        random_data = random_match.group(0)
        lines = random_data.strip().split('\n')
        
        # Extract headers and data
        headers = lines[0].split()
        data_rows = [line.split() for line in lines[1:]]
        
        # Create DataFrame
        random_df = pd.DataFrame(data_rows, columns=headers)
        random_df = random_df.apply(pd.to_numeric, errors='ignore')
        
        # Reshape for 3D visualization
        file_sizes = random_df['kB'].unique()
        record_sizes = []
        random_read_values = []
        random_write_values = []
        
        for file_size in file_sizes:
            file_df = random_df[random_df['kB'] == file_size]
            record_sizes = file_df['reclen'].tolist()
            random_read_values.append(file_df['read'].tolist())
            random_write_values.append(file_df['write'].tolist())
        
        results['random'] = {
            'file_sizes': file_sizes,
            'record_sizes': record_sizes,
            'random_read_values': random_read_values,
            'random_write_values': random_write_values
        }
    
    return results

def create_3d_visualization(vm_results, container_results, output_file):
    """
    Create 3D visualization of IOZone results
    """
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=4,
        specs=[
            [{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}],
            [{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]
        ],
        subplot_titles=(
            'VM Write Performance', 'VM Read Performance', 'VM Random Read Performance', 'VM Random Write Performance',
            'Container Write Performance', 'Container Read Performance', 'Container Random Read Performance', 'Container Random Write Performance'
        ),
        horizontal_spacing=0.05,
        vertical_spacing=0.1
    )
    
    # Add VM write performance
    fig.add_trace(
        go.Surface(
            z=vm_results['write']['write_values'],
            x=vm_results['write']['record_sizes'],
            y=vm_results['write']['file_sizes'],
            colorscale='Viridis',
            name='VM Write'
        ),
        row=1, col=1
    )
    
    # Add VM read performance
    fig.add_trace(
        go.Surface(
            z=vm_results['read']['read_values'],
            x=vm_results['read']['record_sizes'],
            y=vm_results['read']['file_sizes'],
            colorscale='Viridis',
            name='VM Read'
        ),
        row=1, col=2
    )
    
    # Add VM random read performance
    fig.add_trace(
        go.Surface(
            z=vm_results['random']['random_read_values'],
            x=vm_results['random']['record_sizes'],
            y=vm_results['random']['file_sizes'],
            colorscale='Viridis',
            name='VM Random Read'
        ),
        row=1, col=3
    )
    
    # Add VM random write performance
    fig.add_trace(
        go.Surface(
            z=vm_results['random']['random_write_values'],
            x=vm_results['random']['record_sizes'],
            y=vm_results['random']['file_sizes'],
            colorscale='Viridis',
            name='VM Random Write'
        ),
        row=1, col=4
    )
    
    # Add Container write performance
    fig.add_trace(
        go.Surface(
            z=container_results['write']['write_values'],
            x=container_results['write']['record_sizes'],
            y=container_results['write']['file_sizes'],
            colorscale='Plasma',
            name='Container Write'
        ),
        row=2, col=1
    )
    
    # Add Container read performance
    fig.add_trace(
        go.Surface(
            z=container_results['read']['read_values'],
            x=container_results['read']['record_sizes'],
            y=container_results['read']['file_sizes'],
            colorscale='Plasma',
            name='Container Read'
        ),
        row=2, col=2
    )
    
    # Add Container random read performance
    fig.add_trace(
        go.Surface(
            z=container_results['random']['random_read_values'],
            x=container_results['random']['record_sizes'],
            y=container_results['random']['file_sizes'],
            colorscale='Plasma',
            name='Container Random Read'
        ),
        row=2, col=3
    )
    
    # Add Container random write performance
    fig.add_trace(
        go.Surface(
            z=container_results['random']['random_write_values'],
            x=container_results['random']['record_sizes'],
            y=container_results['random']['file_sizes'],
            colorscale='Plasma',
            name='Container Random Write'
        ),
        row=2, col=4
    )
    
    # Update layout
    fig.update_layout(
        title_text="IOZone Performance Comparison: VMs vs Containers",
        height=1200,
        width=1800,
        scene1=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene2=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene3=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene4=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene5=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene6=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene7=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        ),
        scene8=dict(
            xaxis_title='Record Size (KB)',
            yaxis_title='File Size (KB)',
            zaxis_title='Throughput (KB/s)'
        )
    )
    
    # Save as HTML
    fig.write_html(output_file)
    print(f"Visualization saved to {output_file}")

def create_comparison_visualization(vm_results, container_results, output_file):
    """
    Create a comparison visualization showing performance differences
    """
    # Create figure with subplots for comparison
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'bar'}, {'type': 'bar'}]
        ],
        subplot_titles=(
            'Write Performance Comparison', 'Read Performance Comparison',
            'Random Read Performance Comparison', 'Random Write Performance Comparison'
        ),
        horizontal_spacing=0.1,
        vertical_spacing=0.2
    )
    
    # Calculate average performance for each operation
    vm_write_avg = np.mean(vm_results['write']['write_values'])
    container_write_avg = np.mean(container_results['write']['write_values'])
    
    vm_read_avg = np.mean(vm_results['read']['read_values'])
    container_read_avg = np.mean(container_results['read']['read_values'])
    
    vm_random_read_avg = np.mean(vm_results['random']['random_read_values'])
    container_random_read_avg = np.mean(container_results['random']['random_read_values'])
    
    vm_random_write_avg = np.mean(vm_results['random']['random_write_values'])
    container_random_write_avg = np.mean(container_results['random']['random_write_values'])
    
    # Add comparison bars
    fig.add_trace(
        go.Bar(
            x=['VM', 'Container'],
            y=[vm_write_avg, container_write_avg],
            name='Write Performance',
            marker_color=['blue', 'red']
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=['VM', 'Container'],
            y=[vm_read_avg, container_read_avg],
            name='Read Performance',
            marker_color=['blue', 'red']
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=['VM', 'Container'],
            y=[vm_random_read_avg, container_random_read_avg],
            name='Random Read Performance',
            marker_color=['blue', 'red']
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=['VM', 'Container'],
            y=[vm_random_write_avg, container_random_write_avg],
            name='Random Write Performance',
            marker_color=['blue', 'red']
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text="Performance Comparison: VMs vs Containers (Average Throughput)",
        height=800,
        width=1200
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Throughput (KB/s)", row=1, col=1)
    fig.update_yaxes(title_text="Throughput (KB/s)", row=1, col=2)
    fig.update_yaxes(title_text="Throughput (KB/s)", row=2, col=1)
    fig.update_yaxes(title_text="Throughput (KB/s)", row=2, col=2)
    
    # Save as HTML
    fig.write_html(output_file)
    print(f"Comparison visualization saved to {output_file}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_iozone_visualization.py <vm_results_file> <container_results_file>")
        sys.exit(1)
    
    vm_results_file = sys.argv[1]
    container_results_file = sys.argv[2]
    
    # Parse results
    vm_results = parse_iozone_results(vm_results_file)
    container_results = parse_iozone_results(container_results_file)
    
    # Create visualizations
    create_3d_visualization(vm_results, container_results, "iozone_3d_visualization.html")
    create_comparison_visualization(vm_results, container_results, "iozone_comparison.html")
    
    print("IOZone visualizations have been generated successfully.")

if __name__ == "__main__":
    main()
