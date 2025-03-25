# Cloud Computing Performance Testing Todo List

## Environment Setup
- [x] Create project directory structure
- [x] Check VirtualBox installation
- [x] Check Docker installation
- [x] Install necessary dependencies
- [x] Investigate sandbox limitations

## Simulation Environment Setup
- [x] Create simulated VM and container directories
- [x] Install benchmarking tools:
  - [x] HPC Challenge Benchmark
  - [x] stress-ng
  - [x] sysbench
  - [x] IOZone
  - [x] iperf/netcat

## Simulated VM Performance Testing
- [x] Configure resource constraints for VM simulation (2 CPUs, 2GB RAM)
- [x] Run performance tests in VM environment:
  - [x] CPU tests with HPC Challenge
  - [x] System tests with stress-ng and sysbench
  - [x] Disk I/O tests with IOZone
  - [x] Network tests with iperf/netcat
- [x] Collect and save VM test results

## Simulated Container Performance Testing
- [x] Configure resource constraints for container simulation (2 CPUs, 2GB RAM)
- [x] Run performance tests in container environment:
  - [x] CPU tests with HPC Challenge
  - [x] System tests with stress-ng and sysbench
  - [x] Disk I/O tests with IOZone
  - [x] Network tests with iperf/netcat
- [x] Collect and save container test results

## Analysis and Documentation
- [x] Compare VM and container performance results
- [x] Create visualizations for performance data
- [x] Write comprehensive report
- [x] Create presentation with results
- [ ] Deliver final documentation
