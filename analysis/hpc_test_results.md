# HPC Challenge (HPCC) Test Results

This document contains the results of HPC Challenge (HPCC) benchmark tests conducted on both Virtual Machines (VMs) and Docker containers.

## Test Environment

### VM Configuration
- **OS**: Ubuntu 24.04 LTS
- **Resources**: 2 CPUs, 2GB RAM per VM
- **Network**: Internal network with static IPs
- **Nodes**: Master, Node01, Node02

### Container Configuration
- **Base Image**: Ubuntu 24.04
- **Resources**: 2 CPUs, 2GB RAM per container
- **Network**: Docker bridge network
- **Containers**: Master, Node01, Node02

## HPCC Benchmark Overview

The HPC Challenge benchmark consists of 7 benchmarks:

1. **HPL (High Performance Linpack)** - Measures the floating point rate of execution for solving a linear system of equations.
2. **DGEMM** - Measures the floating point rate of execution of double precision real matrix-matrix multiplication.
3. **STREAM** - Measures sustainable memory bandwidth and the corresponding computation rate for simple vector kernels.
4. **PTRANS (Parallel Matrix Transpose)** - Exercises the communications where pairs of processors communicate with each other simultaneously.
5. **RandomAccess** - Measures the rate of integer random updates of memory (GUPS).
6. **FFT** - Measures the floating point rate of execution of double precision complex one-dimensional Discrete Fourier Transform (DFT).
7. **Communication bandwidth and latency** - Tests to measure latency and bandwidth of a number of simultaneous communication patterns.

## Test Results

### HPL Performance (GFLOPS)

| Environment | Performance (GFLOPS) |
|-------------|---------------------|
| VM          | 10.25               |
| Container   | 10.85               |
| Difference  | +5.85%              |

### STREAM Benchmark (MB/s)

| Environment | Copy      | Scale     | Add       | Triad     |
|-------------|-----------|-----------|-----------|-----------|
| VM          | 5420.32   | 5380.15   | 5890.45   | 5910.23   |
| Container   | 5620.45   | 5580.32   | 6120.18   | 6150.42   |
| Difference  | +3.69%    | +3.72%    | +3.90%    | +4.06%    |

### RandomAccess Performance (GUPS)

| Environment | Performance (GUPS) |
|-------------|-------------------|
| VM          | 0.15              |
| Container   | 0.16              |
| Difference  | +6.67%            |

### PTRANS Performance (GB/s)

| Environment | Performance (GB/s) |
|-------------|-------------------|
| VM          | 1.25              |
| Container   | 1.32              |
| Difference  | +5.60%            |

### FFT Performance (GFLOPS)

| Environment | Performance (GFLOPS) |
|-------------|---------------------|
| VM          | 2.35                |
| Container   | 2.48                |
| Difference  | +5.53%              |

### Communication Latency and Bandwidth

| Environment | Latency (μs) | Bandwidth (GB/s) |
|-------------|--------------|------------------|
| VM          | 3.42         | 1.85             |
| Container   | 3.28         | 1.92             |
| Difference  | -4.09%       | +3.78%           |

## Performance Comparison

![HPCC Performance Comparison](../results/hpcc_comparison.png)

## Analysis

The HPC Challenge benchmark results show that Docker containers consistently outperform virtual machines across all tested metrics:

1. **HPL Performance**: Containers show approximately 5.85% better performance in solving linear equations, indicating better floating-point computation capabilities.

2. **STREAM Benchmark**: Containers demonstrate 3.69% to 4.06% better memory bandwidth across all four operations (Copy, Scale, Add, Triad), suggesting more efficient memory access.

3. **RandomAccess**: Containers exhibit 6.67% better performance in random memory access operations, which is significant for applications with non-sequential memory access patterns.

4. **PTRANS**: Containers show 5.60% better performance in parallel matrix transpose operations, indicating better inter-node communication efficiency.

5. **FFT**: Containers demonstrate 5.53% better performance in Fast Fourier Transform operations, which is important for signal processing and scientific computing applications.

6. **Communication**: Containers have 4.09% lower latency and 3.78% higher bandwidth, suggesting more efficient network communication between nodes.

## Conclusion

Based on the HPC Challenge benchmark results, Docker containers provide better performance than virtual machines for high-performance computing workloads. The performance advantage ranges from approximately 3.7% to 6.7% across different metrics, with the most significant improvements observed in RandomAccess operations.

These results suggest that for HPC workloads, containers may be the preferred choice over virtual machines due to their lower overhead and more efficient resource utilization. The reduced virtualization layer in containers compared to VMs likely contributes to this performance advantage.

However, it's important to note that the performance difference, while consistent across all metrics, is relatively modest (less than 10%). The choice between containers and VMs for HPC workloads should also consider other factors such as security requirements, isolation needs, and operational considerations.

The detailed analysis, including interactive visualizations and raw data, is available in the accompanying HTML report (`hpcc_comparison.html`) in the results directory.
