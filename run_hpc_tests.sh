#!/bin/bash

# This script runs HPC Challenge (HPCC) tests on both VMs and containers
# and collects the results for analysis

# Create results directory
mkdir -p /shared/results

# ===== Create HPCC input file =====

echo "Creating HPCC input file..."

cat > /shared/hpccinf.txt << 'EOF'
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
EOF

# ===== Create hosts file =====

echo "Creating hosts file for MPI..."

cat > /shared/hosts << 'EOF'
Node01 slots=1
Node02 slots=1
EOF

# ===== Run HPCC on VMs =====

echo "Running HPCC test on VMs..."
cd /shared
mpirun -np 2 -hostfile hosts hpcc | tee /shared/results/vm_hpcc_results.txt

# Check if hpccoutf.txt was created
if [ -f hpccoutf.txt ]; then
    cp hpccoutf.txt /shared/results/vm_hpccoutf.txt
    echo "VM HPCC output file saved to /shared/results/vm_hpccoutf.txt"
fi

# ===== Run HPCC on Containers =====

echo "Running HPCC test on containers..."
docker exec Master bash -c "cd /shared && mpirun -np 2 -hostfile hosts hpcc" | tee /shared/results/container_hpcc_results.txt

# Check if hpccoutf.txt was created in the container
docker exec Master bash -c "if [ -f /shared/hpccoutf.txt ]; then cp /shared/hpccoutf.txt /shared/results/container_hpccoutf.txt; fi"
if [ -f /shared/results/container_hpccoutf.txt ]; then
    echo "Container HPCC output file saved to /shared/results/container_hpccoutf.txt"
fi

# ===== Extract and analyze results =====

echo "Analyzing HPCC results..."

# Extract HPL performance
echo "HPL Performance (GFLOPS):" > /shared/results/hpcc_summary.txt
echo -n "VM: " >> /shared/results/hpcc_summary.txt
grep -A 2 "Gflop/s" /shared/results/vm_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt
echo -n "Container: " >> /shared/results/hpcc_summary.txt
grep -A 2 "Gflop/s" /shared/results/container_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt

# Extract STREAM benchmark results
echo -e "\nSTREAM Benchmark (MB/s):" >> /shared/results/hpcc_summary.txt
echo -n "VM: " >> /shared/results/hpcc_summary.txt
grep -A 4 "STREAM:" /shared/results/vm_hpcc_results.txt | tail -n 1 >> /shared/results/hpcc_summary.txt
echo -n "Container: " >> /shared/results/hpcc_summary.txt
grep -A 4 "STREAM:" /shared/results/container_hpcc_results.txt | tail -n 1 >> /shared/results/hpcc_summary.txt

# Extract RandomAccess performance
echo -e "\nRandomAccess Performance (GUPS):" >> /shared/results/hpcc_summary.txt
echo -n "VM: " >> /shared/results/hpcc_summary.txt
grep -A 2 "Random Access" /shared/results/vm_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt
echo -n "Container: " >> /shared/results/hpcc_summary.txt
grep -A 2 "Random Access" /shared/results/container_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt

# Extract PTRANS performance
echo -e "\nPTRANS Performance (GB/s):" >> /shared/results/hpcc_summary.txt
echo -n "VM: " >> /shared/results/hpcc_summary.txt
grep -A 2 "PTRANS" /shared/results/vm_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt
echo -n "Container: " >> /shared/results/hpcc_summary.txt
grep -A 2 "PTRANS" /shared/results/container_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt

# Extract FFT performance
echo -e "\nFFT Performance (GFLOPS):" >> /shared/results/hpcc_summary.txt
echo -n "VM: " >> /shared/results/hpcc_summary.txt
grep -A 2 "FFT" /shared/results/vm_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt
echo -n "Container: " >> /shared/results/hpcc_summary.txt
grep -A 2 "FFT" /shared/results/container_hpcc_results.txt | tail -n 1 | awk '{print $1}' >> /shared/results/hpcc_summary.txt

# ===== Generate detailed analysis =====

echo "Generating detailed HPCC analysis..."
python3 /home/ubuntu/cloud_performance_test/analysis/analyze_hpcc.py /shared/results/vm_hpcc_results.txt /shared/results/container_hpcc_results.txt

# Move generated files to results directory
mv hpcc_comparison.csv /shared/results/
mv hpcc_comparison.png /shared/results/
mv hpcc_comparison.html /shared/results/

echo "HPC testing completed. Results are available in /shared/results/"
echo "Summary: /shared/results/hpcc_summary.txt"
echo "Detailed analysis: /shared/results/hpcc_comparison.html"
