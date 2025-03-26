# Cloud Performance Testing Project Todo List

## Analysis and Setup
- [x] Analyze requirements from user's repository (ahmedtarek26/cloud_performance_test)
- [x] Analyze reference repository for commands (CapraCampa/Cloud-Final-Project)
- [ ] Set up project environment and directory structure

## Cluster Setup
- [ ] Create Master VM configuration
- [ ] Create Node01 VM configuration
- [ ] Create Node02 VM configuration
- [ ] Configure network between VMs
- [ ] Set up SSH connections between nodes
- [ ] Configure shared filesystem

## Performance Testing
- [ ] Install required testing tools (stress-ng, sysbench, iozone, iperf, hpcc)
- [ ] Run CPU tests using stress-ng
- [ ] Run memory tests using sysbench
- [ ] Run disk I/O tests using IOZone
- [ ] Run network tests using iperf
- [ ] Run HPC Challenge (HPCC) tests

## Container Setup and Testing
- [ ] Create Docker container configuration
- [ ] Set up container network
- [ ] Run performance tests on containers
- [ ] Compare VM and container performance

## Visualization and Analysis
- [ ] Update IOZone visualization using the command `iozone -a -R -O | tee iozone_results.txt`
- [ ] Create 3D visualization for IOZone results
- [ ] Analyze and compare VM vs container performance
- [ ] Document findings and insights

## Documentation and Reporting
- [ ] Compile comprehensive report following user's repository structure
- [ ] Create presentation for project
- [ ] Update GitHub repository with new files and changes
- [ ] Prepare pull requests for repository updates

## Final Deliverables
- [ ] Complete report document
- [ ] Presentation slides
- [ ] Updated GitHub repository
- [ ] IOZone visualization updates
- [ ] HPC testing results and analysis
