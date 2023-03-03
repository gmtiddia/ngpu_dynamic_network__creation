#
#  eval_microcircuit_time.py
#
#  This file is part of NEST GPU.
#
#  Copyright (C) 2021 The NEST Initiative
#
#  NEST GPU is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  NEST GPU is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NEST GPU. If not, see <http://www.gnu.org/licenses/>.
#
#
#
#
"""PyNEST Microcircuit: Run Simulation
-----------------------------------------

This is an example script for running the microcircuit model and generating
basic plots of the network activity.

"""

###############################################################################
# Import the necessary modules and start the time measurements.

from stimulus_params import stim_dict
from network_params import net_dict
from sim_params_norec import sim_dict
import network

from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
from json import dump, dumps

# Get and check file path
parser = ArgumentParser()
parser.add_argument("-o", type=str)
parser.add_argument("--algo", type=int, default=0)
parser.add_argument("--seed", type=int, default=12345)
args = parser.parse_args()
out_path = Path(args.o)
assert 0 <= args.algo and args.algo < 9 and not out_path.exists()
sim_dict["master_seed"] = args.seed

nl_dict = {
        0: "BlockStep",
        1: "CumulSum",
        2: "Simple",
        3: "ParallelInner",
        4: "ParallelOuter",
        5: "Frame1D",
        6: "Frame2D",
        7: "Smart1D",
        8: "Smart2D",
    }

time_start = perf_counter_ns()

###############################################################################
# Initialize the network with simulation, network and stimulation parameters,
# then create and connect all nodes, and finally simulate.
# The times for a presimulation and the main simulation are taken
# independently. A presimulation is useful because the spike activity typically
# exhibits a startup transient. In benchmark simulations, this transient should
# be excluded from a time measurement of the state propagation phase. Besides,
# statistical measures of the spike activity should only be computed after the
# transient has passed.

net = network.Network(sim_dict, net_dict, stim_dict)
net.set_algo(args.algo)
time_network = perf_counter_ns()

net.create()
time_create = perf_counter_ns()

net.connect()
time_connect = perf_counter_ns()

net.simulate(sim_dict['t_presim'])
time_presimulate = perf_counter_ns()

net.simulate(sim_dict['t_sim'])
time_simulate = perf_counter_ns()

time_dict = {
        "time_network": time_network - time_start,
        "time_create": time_create - time_network,
        "time_connect": time_connect - time_create,
        "time_presimulate": time_presimulate - time_connect,
        "time_simulate": time_simulate - time_presimulate,
        "time_total": time_simulate - time_start,
        }

info_dict = {
        "nested_loop_algo": nl_dict[args.algo],
        "timers": time_dict
    }

with out_path.open("w") as f:
    dump(info_dict, f, indent=4)

print(dumps(info_dict, indent=4))