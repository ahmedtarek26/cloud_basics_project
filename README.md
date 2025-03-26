# Cloud Performance Testing

This repository contains the implementation and results of a comprehensive cloud performance testing project comparing Virtual Machines (VMs) and Docker containers.

## Project Overview

The objective of this project is to evaluate and compare the performance of virtual machines and Docker containers using various performance testing tools. The test environment consists of three nodes (master, node01, and node02) connected via a host-only network, alongside Docker containers for containerized performance testing.

## Environment Setup

- **Linux distribution**: Ubuntu 24.04 LTS
- **Virtualization**: VirtualBox for VMs, Docker for containers
- **Resource allocation**: 2 CPUs and 2GB RAM for both VMs and containers
- **Performance testing tools**: stress-ng, sysbench, IOZone, iperf, and HPCC (HPC Challenge)

## Repository Structure

- **analysis/**: Documentation and analysis scripts
  - `cluster_setup.md`: Detailed instructions for setting up the VM cluster
  - `docker_setup.md`: Instructions for setting up Docker containers
  - `performance_tests.md`: Commands for running performance tests
  - `hpc_testing.md`: Guide for HPC testing with HPCC
  - `analyze_hpcc.py`: Script for analyzing HPCC results
  
- **visualizations/**: Scripts for visualizing test results
  - `iozone_visualize.py`: Plotly-based script for IOZone visualization
  - `iozone_visualize_matplotlib.py`: Matplotlib-based script for IOZone visualization

## Performance Tests

The following performance tests are conducted on both VMs and containers:

1. **CPU Test**: HPC Challenge (HPCC) and stress-ng
2. **Memory Test**: sysbench and stress-ng
3. **Disk I/O Test**: IOZone
4. **Network Test**: iperf

## Results and Analysis

The results of the performance tests are analyzed and visualized to compare the performance of VMs and containers. The analysis includes:

- 3D visualization of IOZone results
- Comparison of HPC Challenge benchmark results
- Performance metrics for CPU, memory, disk I/O, and network

## Usage

1. Set up the VM cluster following the instructions in `analysis/cluster_setup.md`
2. Set up Docker containers following the instructions in `analysis/docker_setup.md`
3. Run performance tests using the commands in `analysis/performance_tests.md`
4. Analyze the results using the provided visualization scripts

## HPC Testing

HPC testing is performed using the HPC Challenge (HPCC) benchmark suite, which includes:

- HPL (High Performance Linpack)
- DGEMM (Double-precision General Matrix Multiply)
- STREAM (Sustainable Memory Bandwidth)
- PTRANS (Parallel Matrix Transpose)
- RandomAccess
- FFT (Fast Fourier Transform)
- Communication bandwidth and latency tests

## IOZone Visualization

IOZone results are visualized using 3D plots to show the relationship between file size, record size, and throughput for various operations:

- Write
- Read
- Random Read
- Random Write

## License

This project is licensed under the MIT License - see the LICENSE file for details.
