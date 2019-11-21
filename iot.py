#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:47:57 2019

@author: willian
"""


import pyomo.environ as pyomo
import numpy as np

model = pyomo.ConcreteModel()

T = 24
N = 9

price = np.array([0.13, 0.13, 0.15, 0.14, 0.14, 0.16, 0.17, 0.17, 0.16, 0.16, 0.2, 0.22, 0.22, 0.22, 0.17, 0.17, 0.17, 0.2, 0.2, 0.2, 0.19, 0.19, 0.18, 0.17])

model.T = pyomo.RangeSet(0, T)
model.N = pyomo.RangeSet(0, N)

model.A1 = pyomo.RangeSet(0, N)
model.A2 = pyomo.Set(initialize=[0, 1, 2])
model.A3 = pyomo.Set(initialize=[0, 1, 2])

model.E = pyomo.Param(model.N, default=0.1)
model.Pr = pyomo.Param(model.T, default=0.1)
model.P = pyomo.Param(model.N, default=0.1)


ET = {0: 2,
      1: 3,
      2: 4}

ST = {0: 1,
      1: 2,
      2: 3}
model.ET = pyomo.Param(range(3), initialize=ET)
model.ST = pyomo.Param(range(3), initialize=ST)


def req_init(model, i):
    return i + 1
model.Req = pyomo.Param(model.N, initialize=req_init)


model.dmax = pyomo.Param(initialize=3)
model.dmin = pyomo.Param(initialize=0)
model.rd = pyomo.Param(initialize=1)
model.ru = pyomo.Param(initialize=1)
model.mdc = pyomo.Param(initialize=10)


model.DSA = pyomo.Var(model.T, model.N, within=pyomo.Binary)
  

def obj_rule(model):
    return sum(model.E[n] * sum((model.Pr[t] * model.DSA[t, n]) * (model.Pr[t] * model.DSA[t, n]) for t in model.T) for n in model.N)
model.obj = pyomo.Objective(rule=obj_rule, sense=pyomo.minimize)

def loadMax_rule(model, t):
    return sum(model.DSA[t, n] * model.P[n] for n in model.N) <= model.dmax
model.loadMax = pyomo.Constraint(model.T, rule=loadMax_rule)    


def loadMin_rule(model, t):
    return sum(model.DSA[t, n] * model.P[n] for n in model.N) >= model.dmin
model.loadMin = pyomo.Constraint(model.T, rule=loadMin_rule)    


def rampIndex(model):
    for t in model.T:
        if t < len(model.T) - 1:
            yield t
            
def rampMin_rule(model, t):
    return sum((model.DSA[t, n] - model.DSA[t + 1, n]) * model.P[n] for n in model.N) <= model.rd
model.rampMin = pyomo.Constraint(rampIndex, rule=rampMin_rule)


def rampMax_rule(model, t):
    return sum((model.DSA[t + 1, n] - model.DSA[t, n]) * model.P[n] for n in model.N) <= model.ru
model.rampMax = pyomo.Constraint(rampIndex, rule=rampMax_rule)


def minimumConsumption_rule(model):
    return sum(sum(model.DSA[t, n] * model.E[n] for t in model.T) for n in model.N) >= model.mdc
model.minimumConsumption = pyomo.Constraint(rule=minimumConsumption_rule)


def a1Category_rule(model, n):
    return sum(model.DSA[t, n] for t in model.T) >= model.Req[n]
model.a1Category = pyomo.Constraint(model.A1, rule=a1Category_rule)

def a2Category_rule(model, n):
    return sum(pyomo.prod([model.DSA[t, n] for t in range(q, model.Req[n] + q)]) for q in range(len(model.T) - model.Req[n])) >= 1
model.a2Category = pyomo.Constraint(model.A2, rule=a2Category_rule)

def a3Category_rule(model, n):
    return sum(model.DSA[t, n] for t in range(model.ST[n], model.ET[n])) >= model.Req[n]
model.a3Category = pyomo.Constraint(model.A3, rule=a3Category_rule)

   

