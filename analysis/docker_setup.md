# Docker Container Setup for Cloud Performance Testing

This document outlines the setup process for creating Docker containers for cloud performance testing and comparison with VMs.

## Container Specifications
- **Base Image**: Ubuntu 24.04
- **Resources per Container**: 2 CPUs, 2GB RAM
- **Network**: Internal Docker bridge network
- **Containers**: Master, Node01, Node02 (matching VM setup)

## Setup Process

### 1. Create Dockerfile

Create a Dockerfile with the following content:

```dockerfile
# Start from the base Ubuntu image
FROM ubuntu:latest

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    openssh-server rsync iputils-ping \
    sysbench stress-ng iozone3 iperf3 \
    netcat-openbsd wget unzip hpcc \
    mpich vim \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create SSH folder and set correct permissions
RUN mkdir -p /var/run/sshd /home/user/.ssh /shared/results \
    && chmod 700 /home/user/.ssh /shared/results

# Create a new user 'user' with a home directory
RUN useradd -m -s /bin/bash user \
    && echo "user:cloud" | chpasswd \
    && echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Generate SSH keys for user (only if they do not already exist)
RUN if [ ! -f /home/user/.ssh/id_rsa ]; then \
    ssh-keygen -t rsa -N '' -f /home/user/.ssh/id_rsa; \
    fi && \
    cat /home/user/.ssh/id_rsa.pub >> /home/user/.ssh/authorized_keys && \
    chmod 600 /home/user/.ssh/authorized_keys && \
    chown -R user:user /home/user/.ssh /shared

# Expose SSH port
EXPOSE 22

# Switch to user
USER user
WORKDIR /home/user

# Start SSH service correctly with host key generation
CMD sudo /usr/sbin/sshd -D -e
```

### 2. Create Docker Compose File

Create a docker-compose.yaml file with the following content:

```yaml
version: '3'
services:
  master:
    build: .
    container_name: Master
    hostname: Master
    networks:
      - my_network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    ports:
      - "2220:22"
    volumes:
      - shared_volume:/shared:mode=777

  node01:
    build: .
    container_name: Node01
    hostname: Node01
    networks:
      - my_network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    ports:
      - "2221:22"
    volumes:
      - shared_volume:/shared:mode=777

  node02:
    build: .
    container_name: Node02
    hostname: Node02
    networks:
      - my_network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    ports:
      - "2222:22"
    volumes:
      - shared_volume:/shared:mode=777

networks:
  my_network:
    driver: bridge

volumes:
  shared_volume:
    driver: local
```

### 3. Build and Start Containers

```bash
docker-compose build -d
docker-compose up -d
```

### 4. Configure Hosts File in Each Container

Access the master container:
```bash
docker exec -it Master bash
```

Edit the hosts file:
```bash
sudo vim /etc/hosts
```

Add the following entries:
```
127.0.0.1 localhost
172.x.x.x Master  # Use actual IP from docker network
172.x.x.x Node01  # Use actual IP from docker network
172.x.x.x Node02  # Use actual IP from docker network
```

Repeat for Node01 and Node02 containers.

### 5. Configure SSH for Passwordless Access

From the Master container, test SSH connections to all nodes:
```bash
ssh Node01
ssh Node02
ssh Master
```

### 6. Verify Shared Volume

Create a test file in the shared volume from Master:
```bash
echo "Test file" > /shared/testfile
```

Verify it's accessible from Node01 and Node02:
```bash
cat /shared/testfile
```

### 7. Prepare for Performance Testing

Create a machines.txt file for IOZone testing:
```bash
echo "Node01 /shared /usr/bin/iozone" > /shared/machines.txt
echo "Node02 /shared /usr/bin/iozone" >> /shared/machines.txt
```

Create a hosts file for MPI/HPCC testing:
```bash
echo "Node01 slots=1" > /home/user/hosts
echo "Node02 slots=1" >> /home/user/hosts
```

This completes the setup of Docker containers for cloud performance testing, mirroring the VM setup for fair comparison.
