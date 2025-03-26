#!/bin/bash

# This script runs all performance tests on both VMs and containers
# and collects the results for analysis

# Create results directory
mkdir -p /shared/results

# ===== CPU Tests =====

echo "Running CPU tests..."

# stress-ng test
echo "Running stress-ng CPU test on VMs..."
mpirun -np 2 -hostfile hosts stress-ng --cpu 2 --timeout 60s --metrics-brief | tee /shared/results/vm_stress_ng_cpu.txt

echo "Running stress-ng CPU test on containers..."
docker exec Master mpirun -np 2 -hostfile hosts stress-ng --cpu 2 --timeout 60s --metrics-brief | tee /shared/results/container_stress_ng_cpu.txt

# HPC Challenge test
echo "Running HPCC test on VMs..."
cd /shared
mpirun -np 2 -hostfile hosts hpcc | tee /shared/results/vm_hpcc_results.txt

echo "Running HPCC test on containers..."
docker exec Master bash -c "cd /shared && mpirun -np 2 -hostfile hosts hpcc" | tee /shared/results/container_hpcc_results.txt

# ===== Memory Tests =====

echo "Running memory tests..."

# sysbench memory test
echo "Running sysbench memory test on VMs..."
mpirun -np 2 -hostfile hosts sysbench memory run | tee /shared/results/vm_sysbench_memory.txt

echo "Running sysbench memory test on containers..."
docker exec Master mpirun -np 2 -hostfile hosts sysbench memory run | tee /shared/results/container_sysbench_memory.txt

# stress-ng memory test
echo "Running stress-ng memory test on VMs..."
mpirun -np 2 -hostfile hosts stress-ng --vm 2 --vm-bytes 1G --timeout 60s --metrics-brief | tee /shared/results/vm_stress_ng_memory.txt

echo "Running stress-ng memory test on containers..."
docker exec Master mpirun -np 2 -hostfile hosts stress-ng --vm 2 --vm-bytes 1G --timeout 60s --metrics-brief | tee /shared/results/container_stress_ng_memory.txt

# ===== Disk I/O Tests =====

echo "Running disk I/O tests..."

# IOZone test on VMs
echo "Running IOZone test on VMs..."
iozone -a -R -O | tee /shared/results/vm_iozone_results.txt

# IOZone test on containers
echo "Running IOZone test on containers..."
docker exec Master iozone -a -R -O | tee /shared/results/container_iozone_results.txt

# IOZone test on shared filesystem
echo "Running IOZone test on shared filesystem for VMs..."
export ssh=rsh
iozone -Rm machines.txt -f /shared/testfile -a -R -O | tee /shared/results/vm_iozone_shared_results.txt

echo "Running IOZone test on shared filesystem for containers..."
docker exec Master bash -c "export ssh=rsh && iozone -Rm machines.txt -f /shared/testfile -a -R -O" | tee /shared/results/container_iozone_shared_results.txt

# ===== Network Tests =====

echo "Running network tests..."

# Start iperf server on Master
echo "Starting iperf server on VM Master..."
iperf -s &
VM_SERVER_PID=$!

# Run iperf client on Node01
echo "Running iperf client on VM Node01..."
ssh Node01 "iperf -c Master -t 10" | tee /shared/results/vm_iperf_results.txt

# Kill iperf server on Master
kill $VM_SERVER_PID

# Start iperf server on container Master
echo "Starting iperf server on container Master..."
docker exec -d Master iperf -s

# Run iperf client on container Node01
echo "Running iperf client on container Node01..."
docker exec Node01 iperf -c Master -t 10 | tee /shared/results/container_iperf_results.txt

# Kill iperf server on container Master
docker exec Master pkill iperf

# ===== Generate Visualizations =====

echo "Generating visualizations..."

# Generate IOZone visualizations
python3 /home/ubuntu/cloud_performance_test/visualizations/generate_iozone_visualization.py /shared/results/vm_iozone_results.txt /shared/results/container_iozone_results.txt

# Generate HPCC analysis
python3 /home/ubuntu/cloud_performance_test/analysis/analyze_hpcc.py /shared/results/vm_hpcc_results.txt /shared/results/container_hpcc_results.txt

echo "All performance tests completed. Results are available in /shared/results/"
