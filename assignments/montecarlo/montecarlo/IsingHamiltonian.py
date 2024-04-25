# Simplified Hamiltonian for package
# Individual files from a package are not run seperately
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

# needed this import format to access the functions in the package
from .BitString import *
from .compute_average_values import *


# look at 'style guide' in mossli workshop
class IsingHamiltonian:
    """Class for an Ising Hamiltonian of arbitrary dimensionality

    Ising Hamiltonian: a hamiltonian represented without superpositions (i.e bitstrings)
    
    defining a hamiltonian of a system, where local contributions (mu's) are factored into the calculations

    .. math::
        H = \\sum_{\\left<ij\\right>} J_{ij}\\sigma_i\\sigma_j + \\sum_i\\mu_i\\sigma_i

    """

    def __init__(self, J=[[()]], mu=np.zeros(1)):
        """Constructor

        Parameters
        ----------
        J: list of lists of tuples, optional
            Strength of coupling, e.g,
            [(4, -1.1), (6, -.1)]
            [(5, -1.1), (7, -.1)]
        mu: vector, optional
            local fields
        """
        self.J = J
        self.mu = mu

        self.nodes = []
        self.js = []

        for i in range(len(self.J)):
            self.nodes.append(np.zeros(len(self.J[i]), dtype=int))
            self.js.append(np.zeros(len(self.J[i])))
            for jidx, j in enumerate(self.J[i]):
                self.nodes[i][jidx] = j[0]
                self.js[i][jidx] = j[1]
        self.mu = np.array([i for i in self.mu])
        self.N = len(self.J)

    def energy(self, config):
        """Compute energy of configuration, `config`

            .. math::
                E = \\left<\\hat{H}\\right>

        Parameters
        ----------
        config   : BitString
            input configuration

        Returns
        -------
        energy  : float
            Energy of the input configuration
        """
        if len(config.config) != len(self.J):
            error("wrong dimension")

        e = 0.0
        for i in range(config.N): # for every possible configuration?
            # print()
            # print(i)
            for j in self.J[i]: # for every sub-entry(?) for the current i'th J entry
                # j is a tuple (basically array), with some entries
                if j[0] < i:
                    continue
                # print(j)
                if config.config[i] == config.config[j[0]]: # if the current configuration entry is equal
                    e += j[1] # add the site weight
                else:
                    e -= j[1] # subtract the site weight

        e += np.dot(self.mu, 2 * config.config - 1)
        return e

    def delta_e_for_flip(self, i, config):
        """Compute the energy change incurred if one were to flip the spin at site i

        Parameters
        ----------
        i        : int
            Index of site to flip
        config   : :class:`BitString`
            input configuration

        Returns
        -------
        energy  : list[BitString, float]
            Returns both the flipped config and the energy change
        """
        dif_e = 0.0 # energy change for the bit flip
        site = self.J[i] # the entry that may have the spin flip
        flipped = config.flip_site(i) # the new bitstring with the flipped site

        if flipped[i] == flipped[site[0]]: # 'undo' the energy from the old config, then add new config
            dif_e += 2 * site[1]
        else:
            dif_e -= 2 * site[1]

        del_e = [flipped, del_e]
        return del_e


    def metropolis_sweep(self, conf, T=1.0):
        """Perform a single sweep through all the sites and return updated configuration

        Parameters
        ----------
        conf   : :class:`BitString`
            input configuration
        T      : int
            Temperature

        Returns
        -------
        conf  : :class:`BitString`
            Returns updated config
        """

    def compute_average_values(self, T):
        """Compute Average values exactly

        Parameters
        ----------
        T      : int
            Temperature

        Returns
        -------
        E  : float
            Energy
        M  : float
            Magnetization
        HC : float
            Heat Capacity
        MS : float
            Magnetic Susceptability
        """
        E = 0.0
        M = 0.0
        Z = 0.0
        EE = 0.0
        MM = 0.0

        conf = BitString(self.N)

        for i in range(2 ** conf.N):
            conf.set_int_config(i)
            Ei = self.energy(conf)
            Zi = np.exp(-Ei / T)
            E += Ei * Zi
            EE += Ei * Ei * Zi
            Mi = np.sum(2 * conf.config - 1)
            M += Mi * Zi
            MM += Mi * Mi * Zi
            Z += Zi

        E = E / Z
        M = M / Z
        EE = EE / Z
        MM = MM / Z

        HC = (EE - E * E) / (T * T)
        MS = (MM - M * M) / T
        return E, M, HC, MS