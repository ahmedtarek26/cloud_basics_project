# IOZone Visualization for Cloud Performance Testing

This document outlines the process for creating 3D visualizations of IOZone test results for both VMs and containers.

## IOZone Test Command

As specified in the requirements, we'll use the following command to run IOZone tests:

```bash
iozone -a -R -O | tee iozone_results.txt
```

Where:
- `-a`: Full automatic mode (tests all record and file sizes)
- `-R`: Generate Excel compatible report
- `-O`: Give results in operations per second
- `tee`: Save output to a file while also displaying it

## Data Processing for Visualization

### 1. Extract Data from IOZone Results

The IOZone results contain multiple tables with different metrics. We need to extract the relevant data for visualization:

```python
import pandas as pd
import numpy as np
import re
import json

def parse_iozone_results(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract the write and read tables
    write_pattern = r"([\s\d]+)\s+reclen\s+write\s+rewrite([\s\d]+)"
    read_pattern = r"([\s\d]+)\s+reclen\s+read\s+reread([\s\d]+)"
    random_pattern = r"([\s\d]+)\s+reclen\s+.*random\s+random([\s\d]+)"
    
    write_match = re.search(write_pattern, content)
    read_match = re.search(read_pattern, content)
    random_match = re.search(random_pattern, content)
    
    # Process write data
    if write_match:
        write_data = write_match.group(0)
        # Parse into DataFrame
        # ...
    
    # Process read data
    if read_match:
        read_data = read_match.group(0)
        # Parse into DataFrame
        # ...
    
    # Process random data
    if random_match:
        random_data = random_match.group(0)
        # Parse into DataFrame
        # ...
    
    # Return processed data
    return {
        'write': write_df,
        'read': read_df,
        'random': random_df
    }
```

### 2. Create CSV Files for Visualization

Convert the parsed data to CSV format for easier visualization:

```python
def create_csv_files(data_dict, output_prefix):
    for test_type, df in data_dict.items():
        df.to_csv(f"{output_prefix}_{test_type}.csv", index=False)
```

## 3D Visualization with HTML/JavaScript

Create an HTML file with JavaScript for 3D visualization using Plotly.js:

```html
<!DOCTYPE html>
<html>
<head>
    <title>IOZone 3D Visualization</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        .plot-container {
            width: 100%;
            height: 600px;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <h1>IOZone Performance Visualization</h1>
    
    <div class="container">
        <h2>VM Performance</h2>
        <div id="vm-write-plot" class="plot-container"></div>
        <div id="vm-read-plot" class="plot-container"></div>
        <div id="vm-random-read-plot" class="plot-container"></div>
        <div id="vm-random-write-plot" class="plot-container"></div>
        
        <h2>Container Performance</h2>
        <div id="container-write-plot" class="plot-container"></div>
        <div id="container-read-plot" class="plot-container"></div>
        <div id="container-random-read-plot" class="plot-container"></div>
        <div id="container-random-write-plot" class="plot-container"></div>
        
        <h2>Performance Comparison</h2>
        <div id="comparison-plot" class="plot-container"></div>
    </div>

    <script>
        // Load data and create visualizations
        function loadData() {
            // Load VM data
            Promise.all([
                fetch('vm_write.csv').then(response => response.text()),
                fetch('vm_read.csv').then(response => response.text()),
                fetch('vm_random.csv').then(response => response.text()),
                fetch('container_write.csv').then(response => response.text()),
                fetch('container_read.csv').then(response => response.text()),
                fetch('container_random.csv').then(response => response.text())
            ]).then(([vmWrite, vmRead, vmRandom, containerWrite, containerRead, containerRandom]) => {
                // Parse CSV data
                const vmWriteData = parseCSV(vmWrite);
                const vmReadData = parseCSV(vmRead);
                const vmRandomData = parseCSV(vmRandom);
                const containerWriteData = parseCSV(containerWrite);
                const containerReadData = parseCSV(containerRead);
                const containerRandomData = parseCSV(containerRandom);
                
                // Create 3D plots
                createPlot('vm-write-plot', vmWriteData, 'VM Write Performance');
                createPlot('vm-read-plot', vmReadData, 'VM Read Performance');
                createPlot('vm-random-read-plot', vmRandomData.randomRead, 'VM Random Read Performance');
                createPlot('vm-random-write-plot', vmRandomData.randomWrite, 'VM Random Write Performance');
                
                createPlot('container-write-plot', containerWriteData, 'Container Write Performance');
                createPlot('container-read-plot', containerReadData, 'Container Read Performance');
                createPlot('container-random-read-plot', containerRandomData.randomRead, 'Container Random Read Performance');
                createPlot('container-random-write-plot', containerRandomData.randomWrite, 'Container Random Write Performance');
                
                // Create comparison plot
                createComparisonPlot('comparison-plot', vmWriteData, containerWriteData, vmReadData, containerReadData);
            });
        }
        
        function parseCSV(csvText) {
            // Parse CSV data
            // ...
        }
        
        function createPlot(elementId, data, title) {
            const layout = {
                title: title,
                autosize: true,
                scene: {
                    xaxis: {title: 'File Size (KB)'},
                    yaxis: {title: 'Record Size (KB)'},
                    zaxis: {title: 'Throughput (KB/s)'}
                }
            };
            
            const plotData = [{
                type: 'surface',
                x: data.fileSizes,
                y: data.recordSizes,
                z: data.throughput,
                colorscale: 'Viridis'
            }];
            
            Plotly.newPlot(elementId, plotData, layout);
        }
        
        function createComparisonPlot(elementId, vmWrite, containerWrite, vmRead, containerRead) {
            // Create comparison visualization
            // ...
        }
        
        // Initialize visualization
        window.onload = loadData;
    </script>
</body>
</html>
```

## Python Script for Automated Visualization

Create a Python script to automate the entire process:

```python
#!/usr/bin/env python3

import pandas as pd
import numpy as np
import re
import json
import os
import sys

def parse_iozone_results(file_path):
    # Implementation as described above
    pass

def create_csv_files(data_dict, output_prefix):
    # Implementation as described above
    pass

def generate_html(vm_data_path, container_data_path, output_html_path):
    # Generate the HTML file with the template above
    # Replace placeholders with actual data file paths
    pass

def main():
    if len(sys.argv) < 4:
        print("Usage: python iozone_visualize.py <vm_results_file> <container_results_file> <output_html>")
        sys.exit(1)
    
    vm_results_file = sys.argv[1]
    container_results_file = sys.argv[2]
    output_html = sys.argv[3]
    
    # Parse VM results
    vm_data = parse_iozone_results(vm_results_file)
    create_csv_files(vm_data, "vm")
    
    # Parse container results
    container_data = parse_iozone_results(container_results_file)
    create_csv_files(container_data, "container")
    
    # Generate HTML visualization
    generate_html("vm", "container", output_html)
    
    print(f"Visualization created at {output_html}")

if __name__ == "__main__":
    main()
```

## Usage Instructions

1. Run IOZone tests on both VMs and containers:
   ```bash
   # On VM
   iozone -a -R -O | tee vm_iozone_results.txt
   
   # On container
   iozone -a -R -O | tee container_iozone_results.txt
   ```

2. Run the visualization script:
   ```bash
   python iozone_visualize.py vm_iozone_results.txt container_iozone_results.txt iozone_3d_visualization.html
   ```

3. Open the HTML file in a web browser to view the 3D visualizations.

This approach provides a comprehensive visualization of IOZone performance metrics, allowing for easy comparison between VM and container performance across different file and record sizes.
