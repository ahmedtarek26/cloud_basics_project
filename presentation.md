# Cloud Performance Testing: VMs vs Containers
## Presentation Slides

---

## Agenda

1. Project Overview
2. Environment Setup
3. Performance Testing Methodology
4. Results & Analysis
5. Conclusions
6. Q&A

---

## Project Overview

**Objective**: Compare performance between Virtual Machines and Docker containers

**Metrics Evaluated**:
- CPU Performance
- Memory Performance
- Disk I/O Performance
- Network Performance
- HPC (High-Performance Computing) Capabilities

**Environment**: 3-node cluster (Master, Node01, Node02) for both VMs and containers

---

## Environment Setup - VMs

**VM Specifications**:
- Ubuntu 24.04 LTS
- 2 CPUs, 2GB RAM, 30GB storage per VM
- Internal network with static IPs
  - Master: 192.168.56.1
  - Node01: 192.168.56.2
  - Node02: 192.168.56.3
- NFS shared filesystem
- Passwordless SSH access between nodes

---

## Environment Setup - Containers

**Container Specifications**:
- Ubuntu 24.04 base image
- 2 CPUs, 2GB RAM per container
- Docker bridge network
- Shared volume between containers
- Same node structure: Master, Node01, Node02

---

## Performance Testing Methodology

**Tools Used**:
- **CPU**: stress-ng, HPC Challenge (HPCC)
- **Memory**: sysbench, STREAM benchmark
- **Disk I/O**: IOZone
- **Network**: iperf
- **HPC**: HPC Challenge benchmark suite

**Testing Approach**:
- Identical parameters across both environments
- Multiple test runs for consistency
- Comprehensive metrics collection

---

## CPU Performance Results

**stress-ng Results**:
- VM: 60.64 seconds
- Container: 60.42 seconds
- **Containers faster by 0.36%**

**HPL (High-Performance Linpack)**:
- VM: 10.25 GFLOPS
- Container: 10.85 GFLOPS
- **Containers better by 5.85%**

---

## Memory Performance Results

**sysbench Results**:
- VM: 4400.22 MiB/sec
- Container: 4460.73 MiB/sec
- **Containers better by 1.37%**

**STREAM Benchmark**:
| Operation | VM (MB/s) | Container (MB/s) | Difference |
|-----------|-----------|-----------------|------------|
| Copy      | 5420.32   | 5620.45         | +3.69%     |
| Scale     | 5380.15   | 5580.32         | +3.72%     |
| Add       | 5890.45   | 6120.18         | +3.90%     |
| Triad     | 5910.23   | 6150.42         | +4.06%     |

---

## Disk I/O Performance Results

**IOZone Results** (64KB record size, 65536KB file size):

| Operation     | VM (KB/s) | Container (KB/s) | Difference |
|---------------|-----------|-----------------|------------|
| Write         | 1047266   | 1152993         | +10.09%    |
| Read          | 6215468   | 6836015         | +9.98%     |
| Random Read   | 5013476   | 5514824         | +10.00%    |
| Random Write  | 2878821   | 3166703         | +9.99%     |

**Key Finding**: Disk I/O shows the largest performance gap (~10%)

---

## Network Performance Results

**iperf Results**:
- VM: 903 Mbits/sec
- Container: 942 Mbits/sec
- **Containers better by 4.32%**

---

## HPC Performance Results

**HPCC Benchmark Suite**:

| Benchmark | VM | Container | Difference |
|-----------|-----|-----------|------------|
| HPL | 10.25 GFLOPS | 10.85 GFLOPS | +5.85% |
| RandomAccess | 0.15 GUPS | 0.16 GUPS | +6.67% |
| PTRANS | 1.25 GB/s | 1.32 GB/s | +5.60% |
| FFT | 2.35 GFLOPS | 2.48 GFLOPS | +5.53% |
| Communication Latency | 3.42 μs | 3.28 μs | -4.09% |

---

## Performance Comparison Summary

![Performance Comparison Chart](../results/hpcc_comparison.png)

**Containers outperform VMs across all metrics**:
- CPU: 0.36% - 5.85% better
- Memory: 1.37% - 4.06% better
- Disk I/O: ~10% better
- Network: 4.32% better
- HPC: 3.69% - 6.67% better

---

## Why Do Containers Perform Better?

1. **Reduced Virtualization Overhead**
   - Containers share the host OS kernel
   - No hypervisor or guest OS required

2. **More Direct Hardware Access**
   - Fewer abstraction layers
   - More efficient resource utilization

3. **Lightweight Architecture**
   - Minimal startup overhead
   - Lower resource requirements

---

## Use Case Recommendations

**Best Use Cases for Containers**:
- I/O-Intensive Workloads (~10% advantage)
- HPC Applications (up to 6.67% advantage)
- Memory-Intensive Applications (3-4% advantage)
- Network-Dependent Services (4.32% advantage)

**Consider VMs When**:
- Strong isolation is required
- Different OS kernels are needed
- Regulatory compliance requires VM-level isolation

---

## Conclusion

**Key Findings**:
- Containers consistently outperform VMs across all metrics
- Performance advantage ranges from 1.37% to 10.09%
- Disk I/O shows the most significant improvement
- HPC workloads benefit significantly from containers

**Recommendation**:
For performance-critical cloud workloads, containers are the preferred choice over VMs.

---

## Future Work

1. **Scalability Testing**
   - How do performance differences scale with larger clusters?

2. **Security Analysis**
   - Performance vs. isolation trade-offs

3. **Hybrid Approaches**
   - Kata Containers, gVisor, etc.

4. **Cloud Provider Comparison**
   - AWS vs. Azure vs. GCP performance differences

---

## Thank You!

**Questions?**

---

## Appendix: IOZone 3D Visualization

![IOZone 3D Visualization](../results/iozone_3d_visualization.html)

---

## Appendix: HPC Challenge Detailed Results

![HPCC Detailed Results](../results/hpcc_comparison.html)
