#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:47:57 2019

@author: willian
"""


from ortools.linear_solver import pywraplp
import numpy as np

try:
    T = np.arange(0, 24, 1)
    N = np.arange(0, 10, 1)
    
    Pr = np.arange(0, 10, 10)
    E = np.arange(0, 10, 10)
    
    
    
    
    
    # Create a new model
    m = Model("iot")

    # Create variables
    dsa = m.addVars(T.size, N.size, vtype=GRB.BINARY, name='DSA')
    
    
    # Set objective
    m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

    # Add constraint: x + y >= 1
    m.addConstr(x + y >= 1, "c1")

    # Optimize model
    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')

