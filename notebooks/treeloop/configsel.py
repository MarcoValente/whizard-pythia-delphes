import numpy as np
from treeloop import helpers as h
from treeloop import configvar as cv
import logging as log

dict_sel = {}

baseline = lambda event, trig_expr='': True
h.addToDict("baseline",baseline,dict_sel)
