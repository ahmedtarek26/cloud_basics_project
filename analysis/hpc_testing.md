# HPC Testing for Cloud Performance Comparison

This document outlines the process for conducting High-Performance Computing (HPC) tests on both VMs and Docker containers using the HPC Challenge (HPCC) benchmark suite.

## Overview of HPC Challenge (HPCC)

The HPC Challenge benchmark consists of 7 benchmarks:

1. **HPL (High Performance Linpack)** - Measures the floating point rate of execution for solving a linear system of equations.
2. **DGEMM** - Measures the floating point rate of execution of double precision real matrix-matrix multiplication.
3. **STREAM** - Measures sustainable memory bandwidth and the corresponding computation rate for simple vector kernels.
4. **PTRANS (Parallel Matrix Transpose)** - Exercises the communications where pairs of processors communicate with each other simultaneously.
5. **RandomAccess** - Measures the rate of integer random updates of memory (GUPS).
6. **FFT** - Measures the floating point rate of execution of double precision complex one-dimensional Discrete Fourier Transform (DFT).
7. **Communication bandwidth and latency** - Tests to measure latency and bandwidth of a number of simultaneous communication patterns.

## Prerequisites

- Cluster setup with Master, Node01, and Node02 (either VMs or containers)
- HPCC and MPI installed on all nodes
- Shared filesystem configured between nodes

## Setup for HPC Testing

### 1. Install Required Packages

On all nodes (VMs or containers):

```bash
sudo apt update
sudo apt install -y hpcc mpich
```

### 2. Configure HPCC Input File

On the Master node:

```bash
sudo mkdir -p /shared
cd /shared
sudo vim hpccinf.txt
```

Add the following configuration:

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
20352        Ns
1            # of NBs
192          NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
1            Ps
2            Qs
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterion
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
##### This line (no. 32) is ignored (it serves as a separator). ######
0            Number of additional problem sizes for PTRANS
1200 10000 30000        values of N
0            number of additional blocking sizes for PTRANS
40 9 8 13 13 20 16 32 64       values of NB
```

### 3. Configure Hosts File for MPI

On the Master node:

```bash
sudo vim /etc/hosts
```

Add entries for all nodes:

```
127.0.0.1 localhost
192.168.56.1 Master
192.168.56.2 Node01
192.168.56.3 Node02
```

Create a hostfile for MPI:

```bash
sudo vim hosts
```

Add:

```
Node01 slots=1
Node02 slots=1
```

### 4. Configure SSH for Passwordless Access

Ensure SSH keys are set up for passwordless access between nodes:

```bash
ssh-keygen -t rsa
ssh-copy-id user@Node01
ssh-copy-id user@Node02
```

## Running HPC Tests

### 1. Run HPCC Benchmark

On the Master node:

```bash
cd /shared
mpirun -np 2 -hostfile hosts hpcc
```

This command runs the HPCC benchmark using 2 processes distributed across the nodes specified in the hostfile.

### 2. Collect Results

The results will be stored in the `hpccoutf.txt` file in the same directory:

```bash
cat hpccoutf.txt
```

### 3. Run HPCC on Containers

For Docker containers, the process is similar:

```bash
docker exec -it Master bash
cd /shared
mpirun -np 2 -hostfile hosts hpcc
```

## Analyzing HPCC Results

The HPCC results provide performance metrics for various aspects of HPC:

### 1. HPL Performance

Extract the HPL performance (in GFLOPS) from the results:

```bash
grep -A 2 "Gflop/s" hpccoutf.txt
```

### 2. STREAM Benchmark Results

Extract the STREAM benchmark results:

```bash
grep -A 4 "STREAM:" hpccoutf.txt
```

This shows memory bandwidth for Copy, Scale, Add, and Triad operations.

### 3. RandomAccess Performance

Extract the RandomAccess performance:

```bash
grep -A 2 "Random Access" hpccoutf.txt
```

This shows the GUPS (Giga Updates Per Second) rate.

### 4. PTRANS Performance

Extract the PTRANS performance:

```bash
grep -A 2 "PTRANS" hpccoutf.txt
```

### 5. FFT Performance

Extract the FFT performance:

```bash
grep -A 2 "FFT" hpccoutf.txt
```

## Comparing VM and Container Performance

Create a comparison table of the key metrics:

| Benchmark | Metric | VM Performance | Container Performance | Difference (%) |
|-----------|--------|---------------|----------------------|----------------|
| HPL | GFLOPS | [VM_HPL] | [Container_HPL] | [Diff_HPL] |
| STREAM Copy | MB/s | [VM_Copy] | [Container_Copy] | [Diff_Copy] |
| STREAM Scale | MB/s | [VM_Scale] | [Container_Scale] | [Diff_Scale] |
| STREAM Add | MB/s | [VM_Add] | [Container_Add] | [Diff_Add] |
| STREAM Triad | MB/s | [VM_Triad] | [Container_Triad] | [Diff_Triad] |
| RandomAccess | GUPS | [VM_RA] | [Container_RA] | [Diff_RA] |
| PTRANS | GB/s | [VM_PT] | [Container_PT] | [Diff_PT] |
| FFT | GFLOPS | [VM_FFT] | [Container_FFT] | [Diff_FFT] |

## Python Script for HPCC Results Analysis

Create a Python script to parse and analyze HPCC results:

```python
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
    
    print("Results saved to hpcc_comparison.csv and hpcc_comparison.png")

if __name__ == "__main__":
    main()
```

## Conclusion

HPC testing using the HPCC benchmark suite provides a comprehensive evaluation of the performance characteristics of both VMs and containers. By comparing the results, we can determine which environment provides better performance for high-performance computing workloads.

The key metrics to focus on are:

1. **HPL Performance (GFLOPS)** - Higher is better, indicates raw computational power
2. **STREAM Bandwidth (MB/s)** - Higher is better, indicates memory bandwidth
3. **RandomAccess (GUPS)** - Higher is better, indicates memory random access performance
4. **PTRANS (GB/s)** - Higher is better, indicates network communication performance
5. **FFT (GFLOPS)** - Higher is better, indicates performance for spectral methods

These metrics provide a comprehensive view of the system's performance for HPC workloads, allowing for a detailed comparison between VMs and containers.
