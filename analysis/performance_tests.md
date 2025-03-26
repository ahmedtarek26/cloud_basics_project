# Performance Testing Commands for Cloud Performance Comparison

This document outlines the commands used for performance testing on both VMs and Docker containers.

## Prerequisites
- Cluster setup with Master, Node01, and Node02 (either VMs or containers)
- All required tools installed: stress-ng, sysbench, iozone, iperf, hpcc, mpich
- Shared filesystem configured between nodes

## 1. CPU Test: HPC Challenge (HPCC)

The HPC Challenge benchmark consists of 7 benchmarks: HPL, STREAM, RandomAccess, PTRANS, FFTE, DGEMM, and b_eff Latency/Bandwidth.

### Setup on Master Node
```bash
sudo mkdir /shared
cd /shared
sudo vim hpccinf.txt
```

Configure the input file with:
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

### Run HPCC Test
```bash
# On Master node
sudo vim /etc/hosts
# Add Node01 and Node02 entries

# Create hostfile for MPI
sudo vim hosts
# Add:
# Node01 slots=1
# Node02 slots=1

# Run HPCC test
mpirun -np 2 -hostfile hosts hpcc
```

The results will be in `hpccoutf.txt` in the same directory.

## 2. Memory/CPU Test: stress-ng

stress-ng is designed to exercise various physical subsystems of a computer as well as the various operating system kernel interfaces.

### Run stress-ng Tests
```bash
# CPU stress test
mpirun -np 2 -hostfile hosts stress-ng --cpu 2 --timeout 60s --metrics-brief | tee stress_ng_cpu.txt

# VM (memory) stress test
mpirun -np 2 -hostfile hosts stress-ng --vm 2 --vm-bytes 1G --timeout 60s --metrics-brief | tee stress_ng_vm.txt

# HDD stress test
mpirun -np 2 -hostfile hosts stress-ng --hdd 1 --timeout 60s --metrics-brief | tee stress_ng_hdd.txt
```

## 3. General System Test: sysbench

Sysbench is a multi-threaded benchmark tool that tests the system under complex workloads.

### Run sysbench Tests
```bash
# CPU test
mpirun -np 2 -hostfile hosts sysbench --test=cpu --cpu-max-prime=20000 run | tee sysbench_cpu_results.txt

# Memory test
mpirun -np 2 -hostfile hosts sysbench --test=memory --memory-total-size=10G run | tee sysbench_memory_results.txt
```

## 4. Disk I/O Test: IOZone

IOZone performs 13 types of tests: Read, Write, Re-read, Re-write, Random Read, Random Write, Backward Read, Record Re-Write, Stride Read, Fread, Fwrite, Freread, Frewrite.

### Run IOZone Tests on Local Filesystem
```bash
# On Master node
iozone -a -R -O | tee iozone_results.txt
```

### Run IOZone Tests on Shared Filesystem
```bash
# Create a machines file
touch /shared/testfile
vim machines.txt
# Add:
# Node01 /shared /usr/bin/iozone
# Node02 /shared /usr/bin/iozone

# Run distributed IOZone test
export ssh=rsh
iozone -Rm machines.txt -f /shared/testfile -a -R -O | tee iozone_shared_results.txt
```

## 5. Network Test: iperf

Iperf is a tool for active measurements of the maximum achievable bandwidth on IP networks.

### Run iperf Tests
```bash
# On Master node (server mode)
iperf -s

# On Node01 (client mode)
iperf -c Master

# On Node02 (client mode)
iperf -c Master
```

## Data Collection and Analysis

All test results should be collected in the shared directory for analysis:

```bash
# Create results directory
mkdir -p /shared/results

# Copy all results
cp *.txt /shared/results/
cp hpccoutf.txt /shared/results/
```

## Visualization for IOZone Results

For IOZone results visualization, follow these steps:

1. Extract the IOZone results to a CSV format
2. Create a 3D visualization using HTML/JavaScript
3. Compare VM and container performance

The IOZone results can be visualized using Excel by:
- Importing the results file with "delimited" format
- Selecting "space delimited"
- Highlighting the region containing file size and record size
- Using the "Surface" chart type with "Columns" option

Alternatively, a custom HTML/JavaScript visualization can be created to display the 3D performance graph.

This completes the performance testing commands for cloud performance comparison between VMs and containers.
