# seismo_det
Determinism by looking at seismogram attributes

# Overview

# Table of Contents

- [seismo\_det](#seismo_det)
- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Structure](#structure)
- [Use for your own data](#use-for-your-own-data)
- [Example data](#example-data)




# Installation

1. Clone this repository
```
    git clone git@github.com:RebeccaColquhoun/seismo_det.git
```
2. Open `environment.yml` and choose the name for your virtual environment
3. Create a virtual environment with all required Python packages by running the following command in terminal
```
conda env create -f environment.yml
```

# Structure

Code is provided to download data, pick waveforms and calculate the 4 parameters of interest. It then extracts relevant parameters into DataFrames which can be used for further analysis, plotting etc.

Warm colors show code files. Cool colors show data and results files which are made as the different code files are run.
Darker colors are directories, whilst lighter colors are files.

```mermaid
flowchart LR
    A[seismo_det] --> C[Data]
    C[Data] --> K[2018_2018_global_m5]
    K[2018_2018_global_m5] -->|e.g.|R[20180131_231321.a]
    R[20180131_231321.a] --> S[data]
    R[20180131_231321.a] --> T[station_xml_files]
    R[20180131_231321.a] --> U[picks.pkl]
    R[20180131_231321.a] -->V[eq_object...]
    C[Data] --> L[results_database]
    C[Data] --> M[2018_2018_global_m5_catalog.xml]
    A[seismo_det] --> B[Code]
    B[Code] --> E[setup_paths]
    B[Code] --> F[1_run_data_download.py]
    B[Code] --> G[2_picking.py]
    B[Code] --> H[3_calculations.py]
    B[Code] --> I[4_make_database.py]
    B[Code] --> J{{make figures as desired}}
    A[seismo_det] --> D[Figures]
    D[Figures] --- N[no_lines...]
    D[Figures] --- O[no_lines...grey]
    D[Figures] --- P[two_lines...]
    D[Figures] --- Q[gradt_speaman...]
    style N fill:#bfe0f5
    style O fill:#bfe0f5
    style P fill:#bfe0f5
    style Q fill:#bfe0f5
    style M fill:#bfe0f5
    style U fill:#bfe0f5
    style V fill:#bfe0f5
    style E fill:#fce492
    style F fill:#fce492
    style G fill:#fce492
    style H fill:#fce492
    style I fill:#fce492
    style J fill:#fce492
    style C fill:#4ea4d9
    style D fill:#4ea4d9
    style K fill:#4ea4d9
    style L fill:#4ea4d9
    style R fill:#4ea4d9
    style S fill:#4ea4d9
    style T fill:#4ea4d9
    style B fill:#e39f46
    style A fill:#ffffff
```


# Use for your own data
1. Set your desired filepaths for storage in setup_paths.py. Otherwise default values will be used.
2. In 1_run_data_download.py set values for min_mag, min_year and max_year. To download just one year of data set min_year and max_year to be the same. This will structure the data file correctly. If using own data, it must be structured as in [Example data](#example-data)
3. Run 1_run_data_download.py
4. Run 2_picking.py
5. Open 3_calculations.py and set parameter options as desired.
   
   ```parameters = [[calculation_window, blank_length, 'eq_object_03s_snr_20_blank_0'],]```

7. Run 3_calculations.py: calculations automatically run on 1 thread. If you want to use multithreading, set num_threads in setup_paths.py to a non-1 value.
8. Open 4_make_database.py and set filenames to those set in 3_calculations.py.
   
   ```e.g. filenames = ['eq_object_03s_snr_20_blank_0_snr20']```

10. Run 4_make_database.py
11. To make figures similar to those in the paper, run figures_2_3.py and figures_4_5.py. Set filenames as in step 7.

# Example data
A small section of example data has been provided in the data/ subdirectory. Any data you use must be structured similarly. Color coding denotes when the file is made if the code is run as in [Use for your own data](#use-for-your-own-data). 
```mermaid
flowchart LR
    AA[key] --> X[1_run_data_download]
    AA[key] --> Z[2_picking]
    AA[key] --> Y[3_calculations]
    AA[key] --> ZZ[4_make_database]
    C[Data] --> K[2018_2018_global_m5]
    K[2018_2018_global_m5] -->|e.g.|R[20180131_231321.a]
    R[20180131_231321.a] --> S[data]
    R[20180131_231321.a] --> T[station_xml_files]
    R[20180131_231321.a] --> U[picks.pkl]
    R[20180131_231321.a] -->|e.g.|V[eq_object...]
    C[Data] --> L[results_database_combined]
    C[Data] --> M[2018_2018_global_m5_catalog.xml]
    S[data] --> |e.g.|D[EC.PUYO.HHE*.mseed]
    S[data] --> |e.g.|E[EC.PUYO.HHN*.mseed]
    S[data] --> |e.g.|F[EC.PUYO.HHZ*.mseed]
    T[station_xml_files] --> |e.g.|G[EC.PUYO.xml]
    K[2018_2018_global_m5] --> B[results_database]
    B[results_database] --> |e.g.|H[results_eq_object...]
    L[results_database_combined] --> |e.g.|I[results_eq_object...]

    style M fill:#bfe0f5
    style S fill:#bfe0f5
    style D fill:#bfe0f5
    style E fill:#bfe0f5
    style F fill:#bfe0f5
    style G fill:#bfe0f5
    style T fill:#bfe0f5
    style R fill:#bfe0f5
    style K fill:#bfe0f5
    style X fill:#bfe0f5
    style AA fill:#ffffff
    style L fill:#c3caf5
    style B fill:#c3caf5
    style H fill:#c3caf5
    style I fill:#c3caf5
    style ZZ fill:#c3caf5
    style V fill:#bff5ce
    style Y fill:#bff5ce
    style Z fill:#86ab90
    style U fill:#86ab90
```





