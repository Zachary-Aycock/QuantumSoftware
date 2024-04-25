import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

# needed diff import format to access the functions in the package
from .BitString import *
from .energy import *

def compute_average_values(bs:BitString, G: nx.Graph, T: float):
    """
    Compute the average value of Energy, Magnetization, 
    Heat Capacity, and Magnetic Susceptibility 

        .. math::
            E = \\left<\\hat{H}\\right>

    Parameters
    ----------
    bs   : Bitstring
        input configuration
    G    : Graph
        input graph defining the Hamiltonian
    T    : float
        temperature of the system
    Returns
    -------
    energy  : float
    magnetization  : float
    heat capacity  : float
    magnetic susceptibility  : float
    """
    # The average value can be found by computing the configuratoin, times the probability
    # Find the expecation values

    # All initilialized variables
    con_en = 0 #the energy of the given configuation
    magn = 0 # The magnetization of the configuration, up - down spins
    kb = 1 # Boltzman constant simplified, 1.38064e-23 J/K actual
    factor = 0 # e^-B*E(a), factor in probability function
    Z = 0.0 # The normalization factor of probability
    prob = 0 # The probability function for the given configuration

    E = 0 # The average energy
    M = 0 # The average magnetization
    HC = 0.0 # The average heat capacity
    HC_var = 0.0 # Variable to calculate HC
    MS = 0.0 # The average magnetic susceptibility
    MS_var = 0.0 # Variable to calculate MS

    # Calculate Z before main loop
    for i in range(2 ** bs.N): #from 0 to 2^N, where N is derived from bs function
        bs.set_int_config(i) # Set the current bitstring to the given loop
        con_en = energy(bs, G)
        Z += np.exp(-con_en/((kb) * T))

    for i in range(2 ** bs.N): # big for loop for all possible calculations
        # Set variables for the given configuration
        bs.set_int_config(i) # Set the current bitstring to the given loop
        con_en = energy(bs, G)
        factor = np.exp(-con_en/((kb) * T))

        # Calculate probability for the given config
        prob = factor / Z

        # Magnetization calculations, using built in 1/0 count in bitstring class
        magn = bs.on() - bs.off()

        # Calculate Energy & M
        E += con_en * prob
        M += magn * prob

        # The other factors to calculate HC and MS
        HC_var += (con_en ** 2) * prob
        MS_var += (magn ** 2) * prob

    # Calculate HC and MS using the expectation values from the loop
    HC = ((HC_var - (E ** 2)) / (T ** 2))
    MS = ((MS_var - (M ** 2)) / (T ** 1))

    # idk why these lines are here, probably for some test somewhere
    # bs.set_int_config(1)
    # print(str(bs.on()) + str(bs.off()))

    return E, M, HC, MS