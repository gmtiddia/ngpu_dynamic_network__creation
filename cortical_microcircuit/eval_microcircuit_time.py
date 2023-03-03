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
#import nestgpu as ngpu
import numpy as np
from time import perf_counter
time_start = perf_counter()

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
time_network = perf_counter()

net.create()
time_create = perf_counter()

net.connect()
time_connect = perf_counter()

net.simulate(sim_dict['t_presim'])
time_presimulate = perf_counter()

net.simulate(sim_dict['t_sim'])
time_simulate = perf_counter()


###############################################################################
# Summarize time measurements. Rank 0 usually takes longest because of the
# data evaluation and print calls.

print(
    '\nTimes:\n' + # of Rank {}:\n'.format( .Rank()) +
    '  Total time:          {:.3f} ms\n'.format(
        (time_simulate -
        time_start)*1000.0) +
    '  Time to initialize:  {:.3f} ms\n'.format(
        (time_network -
        time_start)*1000.0) +
    '  Time to create:      {:.3f} ms\n'.format(
        (time_create -
        time_network)*1000.0) +
    '  Time to connect:     {:.3f} ms\n'.format(
        (time_connect -
        time_create)*1000.0) +
    '  Time to pre simulate: {:.3f} ms\n'.format(
        (time_presimulate -
        time_connect)*1000.0) +
    '  Time to simulate:    {:.3f} ms\n'.format(
        (time_simulate -
        time_presimulate)*1000.0) )