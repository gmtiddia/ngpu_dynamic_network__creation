# Cortical microcircuit model for NEST

Taken from https://github.com/nest/nest-simulator/tree/master/pynest/examples/Potjans_2014
<br>
Time of writing: 11.03.2023, last update to model: 01.02.2023

## Contents

### Original files

These files did not change with respect to the source at time of writing:
 - run_microcircuit.py
 - helpers.py
 - sim_params.py
 - network_params.py
 - stimulus_params.py


### Modified files

These files were modified for benchmarking purposes:
 - network.py:
   - Fixed MPI related bug at __setup_nest function (l263): At time of writing, accessing kernel values inside a Python print statement when using multiple MPI processes causes an MPI library crash. For this, the access of kernel values was moved before the print.
   - Disabled Prepare and Cleanup call from connect function (l98): To properly measure calibration time, Prepare and Cleanup functions were commented.

### Additional files

These files were added for benchmarking purposes:
 - run_benchmark.py: Python script based on the original simulation script of the model with additional adaptations for benchmarking, notably the addition of command line argument handling, simulation timers (cf Models sub-section in #INSERT PAPER REF#), and data exporting to json files.
  - Added handling of number of threads and processes passed as arguments.
  - Added computing of mean firing rate of neurons using the local_spike_counter kernel attribute.
 - merge_data.py: Python script to merge output of multiple MPI processes during a single simulation.
 - gather_data.py: Python script designed to collect the data from all of the simulation runs of a benchmark and compute the mean values and the standard deviation of the simulation timers.
 - benchmark.sh: Bash script to automatically benchmark the model with 10 different random generation seeds and collect the data.
 