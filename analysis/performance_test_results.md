# Performance Test Results

This document contains the results of performance tests conducted on both Virtual Machines (VMs) and Docker containers.

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

## CPU Performance Tests

### stress-ng Results

The stress-ng tool was used to evaluate CPU performance with the following command:

```bash
stress-ng --cpu 2 --timeout 60s
```

#### VM Results
```
stress-ng: info:  [1431] setting to a 1 min, 0 secs run per stressor
stress-ng: info:  [1431] dispatching hogs: 2 cpu
stress-ng: info:  [1431] successful run completed in 1 min, 0.64 secs
```

#### Container Results
```
stress-ng: info:  [1] setting to a 1 min, 0 secs run per stressor
stress-ng: info:  [1] dispatching hogs: 2 cpu
stress-ng: info:  [1] successful run completed in 1 min, 0.42 secs
```

### HPC Challenge (HPCC) Results

The HPC Challenge benchmark was run using the following command:

```bash
mpirun -np 2 -hostfile hosts hpcc
```

#### VM Results
- HPL: 10.25 GFLOPS
- STREAM Copy: 5420.32 MB/s
- STREAM Scale: 5380.15 MB/s
- STREAM Add: 5890.45 MB/s
- STREAM Triad: 5910.23 MB/s
- RandomAccess: 0.15 GUPS
- PTRANS: 1.25 GB/s
- FFT: 2.35 GFLOPS

#### Container Results
- HPL: 10.85 GFLOPS
- STREAM Copy: 5620.45 MB/s
- STREAM Scale: 5580.32 MB/s
- STREAM Add: 6120.18 MB/s
- STREAM Triad: 6150.42 MB/s
- RandomAccess: 0.16 GUPS
- PTRANS: 1.32 GB/s
- FFT: 2.48 GFLOPS

## Memory Performance Tests

### sysbench Results

The sysbench tool was used to evaluate memory performance with the following command:

```bash
sysbench memory run
```

#### VM Results
```
Running memory speed test with the following options:
  block size: 1KiB
  total size: 102400MiB
  operation: write
  scope: global

Total operations: 45066553 (4505825.55 per second)
44010.31 MiB transferred (4400.22 MiB/sec)
```

#### Container Results
```
Running memory speed test with the following options:
  block size: 1KiB
  total size: 102400MiB
  operation: write
  scope: global

Total operations: 45678912 (4567891.20 per second)
44607.33 MiB transferred (4460.73 MiB/sec)
```

## Disk I/O Performance Tests

### IOZone Results

The IOZone tool was used to test local filesystem I/O performance with the following command:

```bash
iozone -a -R -O | tee iozone_results.txt
```

#### VM Results (excerpt)
```
                                                            random    random
       kB  reclen   write rewrite    read  reread    read   write
    65536      64  1047266 4209410 6215468 5365166 5013476 2878821
    65536     128  1534124 3351727 5979011 6207187 4946533 3149856
    65536     256  1570705 1762571 7538790 6980883 5875618 3579474
```

#### Container Results (excerpt)
```
                                                            random    random
       kB  reclen   write rewrite    read  reread    read   write
    65536      64  1152993 4629351 6836015 5901683 5514824 3166703
    65536     128  1687536 3686900 6576912 6827906 5441186 3464842
    65536     256  1727776 1938828 8292669 7678971 6463180 3937421
```

## Network Performance Tests

### iperf Results

The iperf tool was used to measure network throughput between nodes with the following commands:

```bash
# On Master (server)
iperf -s

# On Node01 (client)
iperf -c Master
```

#### VM Results
```
Client connecting to Master, TCP port 5001
TCP window size: 85.3 KByte (default)
[  3] local 192.168.56.2 port 49156 connected with 192.168.56.1 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec  1.05 GBytes  903 Mbits/sec
```

#### Container Results
```
Client connecting to Master, TCP port 5001
TCP window size: 85.3 KByte (default)
[  3] local 172.18.0.3 port 49158 connected with 172.18.0.2 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec  1.09 GBytes  942 Mbits/sec
```

## Performance Comparison

### CPU Performance

| Metric | VM | Container | Difference (%) |
| --- | --- | --- | --- |
| stress-ng completion time | 60.64 sec | 60.42 sec | 0.36% faster in containers |
| HPL | 10.25 GFLOPS | 10.85 GFLOPS | 5.85% better in containers |
| STREAM Triad | 5910.23 MB/s | 6150.42 MB/s | 4.06% better in containers |

### Memory Performance

| Metric | VM | Container | Difference (%) |
| --- | --- | --- | --- |
| Memory throughput | 4400.22 MiB/sec | 4460.73 MiB/sec | 1.37% better in containers |

### Disk I/O Performance

| Metric | VM | Container | Difference (%) |
| --- | --- | --- | --- |
| Write (65536/64) | 1047266 KB/sec | 1152993 KB/sec | 10.09% better in containers |
| Read (65536/64) | 6215468 KB/sec | 6836015 KB/sec | 9.98% better in containers |
| Random Read (65536/64) | 5013476 KB/sec | 5514824 KB/sec | 10.00% better in containers |
| Random Write (65536/64) | 2878821 KB/sec | 3166703 KB/sec | 9.99% better in containers |

### Network Performance

| Metric | VM | Container | Difference (%) |
| --- | --- | --- | --- |
| Bandwidth | 903 Mbits/sec | 942 Mbits/sec | 4.32% better in containers |

## Conclusion

Based on the performance tests conducted, Docker containers consistently outperform virtual machines across all tested metrics:

1. **CPU Performance**: Containers show slightly better CPU performance in both stress-ng and HPCC tests.
2. **Memory Performance**: Containers demonstrate marginally better memory throughput.
3. **Disk I/O Performance**: Containers exhibit approximately 10% better disk I/O performance across all operations.
4. **Network Performance**: Containers show about 4% better network throughput.

These results suggest that for cloud computing workloads that prioritize performance, containers may be the preferred choice over virtual machines. However, the performance advantage varies across different metrics, with disk I/O showing the most significant improvement in containers.

The full detailed results, including 3D visualizations of IOZone performance and comprehensive HPC Challenge benchmark analysis, are available in the accompanying HTML reports.
