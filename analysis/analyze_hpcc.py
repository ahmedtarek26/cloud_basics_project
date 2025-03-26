#!/usr/bin/env python3

import re
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_hpcc_results(file_path):
    """Parse HPCC results file and extract key metrics"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    results = {}
    
    # Extract HPL performance
    hpl_match = re.search(r"Gflop/s\s+=\s+(\d+\.\d+)", content)
    if hpl_match:
        results['HPL_GFLOPS'] = float(hpl_match.group(1))
    
    # Extract STREAM performance
    stream_match = re.search(r"STREAM: Copy\s+(\d+\.\d+)\s+Scale\s+(\d+\.\d+)\s+Add\s+(\d+\.\d+)\s+Triad\s+(\d+\.\d+)", content)
    if stream_match:
        results['STREAM_Copy'] = float(stream_match.group(1))
        results['STREAM_Scale'] = float(stream_match.group(2))
        results['STREAM_Add'] = float(stream_match.group(3))
        results['STREAM_Triad'] = float(stream_match.group(4))
    
    # Extract RandomAccess performance
    ra_match = re.search(r"Random Access\s+(\d+\.\d+)", content)
    if ra_match:
        results['RandomAccess_GUPS'] = float(ra_match.group(1))
    
    # Extract PTRANS performance
    ptrans_match = re.search(r"PTRANS\s+(\d+\.\d+)", content)
    if ptrans_match:
        results['PTRANS_GBs'] = float(ptrans_match.group(1))
    
    # Extract FFT performance
    fft_match = re.search(r"FFT\s+(\d+\.\d+)", content)
    if fft_match:
        results['FFT_GFLOPS'] = float(fft_match.group(1))
    
    return results

def compare_results(vm_results, container_results):
    """Compare VM and container results and calculate differences"""
    comparison = {}
    
    for key in vm_results:
        if key in container_results:
            vm_val = vm_results[key]
            container_val = container_results[key]
            diff_pct = (container_val - vm_val) / vm_val * 100
            comparison[key] = {
                'VM': vm_val,
                'Container': container_val,
                'Difference (%)': diff_pct
            }
    
    return comparison

def create_comparison_chart(comparison, output_file):
    """Create a bar chart comparing VM and container performance"""
    metrics = list(comparison.keys())
    vm_values = [comparison[m]['VM'] for m in metrics]
    container_values = [comparison[m]['Container'] for m in metrics]
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set width of bars
    bar_width = 0.35
    
    # Set position of bars on x axis
    r1 = np.arange(len(metrics))
    r2 = [x + bar_width for x in r1]
    
    # Create bars
    ax.bar(r1, vm_values, width=bar_width, label='VM', color='blue', alpha=0.7)
    ax.bar(r2, container_values, width=bar_width, label='Container', color='red', alpha=0.7)
    
    # Add labels and title
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Performance')
    ax.set_title('HPC Performance Comparison: VM vs Container')
    ax.set_xticks([r + bar_width/2 for r in range(len(metrics))])
    ax.set_xticklabels(metrics, rotation=45, ha='right')
    
    # Add legend
    ax.legend()
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=300)
    plt.close()

def create_html_report(comparison, output_file):
    """Create an HTML report with the comparison results"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HPC Performance Comparison: VMs vs Containers</title>
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
            .chart-container {
                max-width: 800px;
                margin: 30px auto;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-radius: 5px;
                padding: 10px;
                background: white;
            }
            .chart-container img {
                width: 100%;
                height: auto;
            }
            .positive {
                color: green;
            }
            .negative {
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>HPC Performance Comparison: VMs vs Containers</h1>
        
        <h2>Performance Metrics Comparison</h2>
        
        <table>
            <tr>
                <th>Benchmark</th>
                <th>Metric</th>
                <th>VM Performance</th>
                <th>Container Performance</th>
                <th>Difference (%)</th>
            </tr>
    """
    
    # Add rows for each metric
    for metric, values in comparison.items():
        vm_val = values['VM']
        container_val = values['Container']
        diff_pct = values['Difference (%)']
        
        # Determine if difference is positive or negative
        diff_class = "positive" if diff_pct > 0 else "negative"
        
        # Extract benchmark and metric name
        parts = metric.split('_')
        benchmark = parts[0]
        metric_name = '_'.join(parts[1:])
        
        html_content += f"""
            <tr>
                <td>{benchmark}</td>
                <td>{metric_name}</td>
                <td>{vm_val:.2f}</td>
                <td>{container_val:.2f}</td>
                <td class="{diff_class}">{diff_pct:.2f}%</td>
            </tr>
        """
    
    html_content += """
        </table>
        
        <h2>Performance Comparison Chart</h2>
        
        <div class="chart-container">
            <img src="hpcc_comparison.png" alt="HPC Performance Comparison Chart">
        </div>
        
        <h2>Analysis</h2>
        
        <p>
            This comparison shows the performance differences between Virtual Machines (VMs) and Containers
            for High-Performance Computing (HPC) workloads using the HPC Challenge benchmark suite.
        </p>
        
        <p>
            <strong>Key observations:</strong>
        </p>
        
        <ul>
    """
    
    # Add observations based on the results
    better_in_container = []
    better_in_vm = []
    
    for metric, values in comparison.items():
        diff_pct = values['Difference (%)']
        if diff_pct > 5:  # Container is significantly better
            better_in_container.append(f"{metric} ({diff_pct:.2f}% better)")
        elif diff_pct < -5:  # VM is significantly better
            better_in_vm.append(f"{metric} ({-diff_pct:.2f}% better)")
    
    if better_in_container:
        html_content += "            <li>Containers performed better in: " + ", ".join(better_in_container) + "</li>\n"
    
    if better_in_vm:
        html_content += "            <li>VMs performed better in: " + ", ".join(better_in_vm) + "</li>\n"
    
    # Add overall conclusion
    avg_diff = sum(values['Difference (%)'] for values in comparison.values()) / len(comparison)
    if avg_diff > 5:
        conclusion = "Overall, containers show better performance for HPC workloads."
    elif avg_diff < -5:
        conclusion = "Overall, VMs show better performance for HPC workloads."
    else:
        conclusion = "Overall, the performance difference between containers and VMs is minimal for HPC workloads."
    
    html_content += f"""
            <li>{conclusion}</li>
        </ul>
        
        <p>
            The results indicate that the choice between VMs and containers for HPC workloads should be based on
            specific requirements and the particular benchmarks that are most relevant to the intended application.
        </p>
    </body>
    </html>
    """
    
    # Write the HTML file
    with open(output_file, 'w') as f:
        f.write(html_content)

def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_hpcc.py <vm_results_file> <container_results_file>")
        sys.exit(1)
    
    vm_results_file = sys.argv[1]
    container_results_file = sys.argv[2]
    
    # Parse results
    vm_results = parse_hpcc_results(vm_results_file)
    container_results = parse_hpcc_results(container_results_file)
    
    # Compare results
    comparison = compare_results(vm_results, container_results)
    
    # Create comparison table
    df = pd.DataFrame(comparison).T
    print(df)
    
    # Save comparison table to CSV
    df.to_csv('hpcc_comparison.csv')
    
    # Create comparison chart
    create_comparison_chart(comparison, 'hpcc_comparison.png')
    
    # Create HTML report
    create_html_report(comparison, 'hpcc_comparison.html')
    
    print("Results saved to hpcc_comparison.csv, hpcc_comparison.png, and hpcc_comparison.html")

if __name__ == "__main__":
    main()
