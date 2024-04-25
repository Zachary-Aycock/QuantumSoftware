import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
from .BitString import *

def energy(bs: BitString, G: nx.Graph):
    """Compute energy of configuration, `bs`

        .. math::
            E = \\left<\\hat{H}\\right>

    Parameters
    ----------
    bs   : Bitstring
        input configuration
    G    : Graph
        input graph defining the Hamiltonian
    Returns
    -------
    energy  : float
        Energy of the input configuration
    """
    # Using bitstring to represent up or down spin of each of the given points. Connected points (points w/edges) add/subtract energy depednign on their relative spin
    energy_value = float(0) #float value to save energy
    for (i,j,k) in G.edges(data = True): #for all points with a connecting edge
        if bs.config[i] == bs.config[j]:
            energy_value += k['weight'] #increase energy from matching spin
        else:
            energy_value -= k['weight'] #decrease energy from matching spin
        #G.edges has three indexes, the third is dictionary. By calling the string 'weight' in the dictionary, I pull the assigned weight value that is 1.0
            
    return energy_value