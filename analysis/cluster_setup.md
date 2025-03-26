# Cluster Setup for Cloud Performance Testing

This document outlines the setup process for creating a cluster of three virtual machines (Master, Node01, and Node02) for cloud performance testing.

## VM Specifications
- **OS**: Ubuntu 24.04 LTS
- **Resources per VM**: 2 CPUs, 2GB RAM, 30GB storage
- **Network**: Internal network with static IPs
  - Master: 192.168.56.1
  - Node01: 192.168.56.2
  - Node02: 192.168.56.3

## Setup Process

### 1. Create Template VM
First, we create a template VM with the following specifications:
- Ubuntu 24.04 LTS Server
- 2 CPUs
- 2GB RAM
- 30GB storage

Initial setup commands:
```bash
sudo apt update 
sudo apt upgrade 
sudo apt install -y openssh-server 
sudo systemctl start ssh 
sudo systemctl enable ssh 
sudo apt install -y net-tools gcc make 
```

### 2. Clone Template to Create Master, Node01, and Node02

After creating the template VM, clone it to create:
- Master VM
- Node01 VM
- Node02 VM

### 3. Configure Port Forwarding for SSH Access

For the Master VM:
- Host IP: 127.0.0.1
- Host Port: 3022
- Guest Port: 22

For Node01 VM:
- Host IP: 127.0.0.1
- Host Port: 4022
- Guest Port: 22

For Node02 VM:
- Host IP: 127.0.0.1
- Host Port: 5022
- Guest Port: 22

This allows SSH access using:
```bash
ssh localhost -p 3022 -l user@127.0.0.1  # For Master
ssh localhost -p 4022 -l user@127.0.0.1  # For Node01
ssh localhost -p 5022 -l user@127.0.0.1  # For Node02
```

### 4. Configure Internal Network

Add a second network adapter to each VM:
- Adapter 2: Internal Network named "CloudBasicNet"

### 5. Configure Network Settings

#### Master Node Configuration
Edit network configuration:
```bash
sudo vim /etc/netplan/50-cloud-init.yaml
```

Configure with:
```yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: false
      addresses: [192.168.56.1/24]
  version: 2
```

Apply changes:
```bash
sudo netplan apply
```

#### Change Hostname
```bash
sudo vim /etc/hostname
# Change to "master"
sudo reboot
```

#### Configure Hosts File
```bash
sudo vim /etc/hosts
```

Add:
```
127.0.0.1 localhost
127.0.1.1 Master
192.168.56.1 Master
192.168.56.2 Node01
192.168.56.3 Node02
```

### 6. Configure Master as DNS and DHCP Server

Install dnsmasq:
```bash
sudo apt update
sudo apt upgrade
sudo apt install dnsmasq -y
```

Configure dnsmasq:
```bash
sudo vim /etc/dnsmasq.conf
```

Uncomment and modify:
```
bogus-priv
resolv-file=/etc/resolv.dnsmasq
listen-address=127.0.0.1, 192.168.56.1
bind-interfaces
dhcp-range=192.168.56.2,192.168.56.254,12h
dhcp-option=option:router,192.168.56.1
dhcp-option=option:dns-server,192.168.56.1
cache-size=1000
log-queries
```

Configure DNS:
```bash
sudo unlink /etc/resolv.conf
sudo vim /etc/resolv.conf
```

Add:
```
nameserver 127.0.0.1
options edns0 trust-ad
search .
```

Link and restart services:
```bash
sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.dnsmasq
sudo systemctl enable dnsmasq
sudo systemctl restart dnsmasq systemd-resolved
sudo systemctl restart dnsmasq
```

### 7. Configure Master as NAT

Enable IP forwarding:
```bash
sudo vim /etc/sysctl.conf
```

Uncomment:
```
net.ipv4.ip_forward=1
```

Apply changes:
```bash
sudo sysctl -p
```

Configure iptables:
```bash
sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
sudo apt install iptables-persistent -y
sudo netfilter-persistent save
```

### 8. Configure Shared Filesystem

Install NFS server:
```bash
sudo apt install nfs-kernel-server -y
```

Create shared directory:
```bash
sudo mkdir -p /shared
sudo chmod 777 /shared
```

Configure exports:
```bash
sudo vim /etc/exports
```

Add:
```
/shared 192.168.56.0/24(rw,sync,no_subtree_check)
```

Apply changes:
```bash
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
```

### 9. Configure Worker Nodes (Node01 and Node02)

#### Change Hostname
For Node01:
```bash
sudo vim /etc/hostname
# Change to "node01"
```

For Node02:
```bash
sudo vim /etc/hostname
# Change to "node02"
```

#### Configure Network Settings
For both nodes:
```bash
sudo vim /etc/netplan/50-cloud-init.yaml
```

Configure with:
```yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: true
  version: 2
```

Apply changes:
```bash
sudo netplan apply
```

#### Configure Hosts File
```bash
sudo vim /etc/hosts
```

Add:
```
127.0.0.1 localhost
127.0.1.1 Node01  # or Node02
192.168.56.1 Master
192.168.56.2 Node01
192.168.56.3 Node02
```

#### Configure NFS Client
```bash
sudo apt install nfs-common -y
sudo mkdir -p /shared
sudo mount Master:/shared /shared
```

Add to fstab for persistence:
```bash
sudo vim /etc/fstab
```

Add:
```
Master:/shared /shared nfs defaults 0 0
```

### 10. Configure SSH Keys for Passwordless Access

On Master:
```bash
ssh-keygen
# Accept defaults
```

Copy keys to worker nodes:
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub user@Node01
ssh-copy-id -i ~/.ssh/id_rsa.pub user@Node02
```

### 11. Verify Connectivity

Test connectivity from Master:
```bash
ping Node01
ping Node02
ssh Node01
ssh Node02
```

Test connectivity from worker nodes:
```bash
ping Master
ping google.com  # Test internet access through NAT
```

### 12. Install Performance Testing Tools

On all nodes:
```bash
sudo apt update
sudo apt upgrade
sudo apt install iperf3 stress-ng iozone3 sysbench hpcc mpich
```

This completes the setup of a three-node cluster for cloud performance testing.
