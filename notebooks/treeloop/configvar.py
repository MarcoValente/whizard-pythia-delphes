import numpy as np
from treeloop import helpers as h
import logging as log

dict_vars = {}


#Common variables
var      = lambda event,varname,sel_name=None: event[varname][event[sel_name]] if not sel_name is None else event[varname]
varsum   = lambda event,varnames,sel_name=None: np.vstack([event[varname][event[sel_name]] if not sel_name is None else event[varname] for varname in varnames]).sum(axis=0)
