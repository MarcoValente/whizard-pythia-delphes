import numpy as np
import re
from copy import deepcopy

default_lumi=100 #fb-1

sample_dict = { #10 TeV
    'kl0.bbbb':   {'xs': 5.627956910000001,  'xs_err': 0.000823,               'br': 0.34, 'mc_eff' : 1.0},
    'kl1.bbbb':   {'xs': 3.38126891,         'xs_err': 0.0006586999999999999,  'br': 0.34, 'mc_eff' : 1.0},
    'kl2p5.bbbb': {'xs': 3.41438458,         'xs_err': 0.0006220999999999999,  'br': 0.34, 'mc_eff' : 1.0},
    'kl5.bbbb':   {'xs': 12.546061300000002, 'xs_err': 0.0016919999999999997,  'br': 0.34, 'mc_eff' : 1.0},
    'klm1.bbbb':  {'xs': 9.69042831,         'xs_err': 0.001233,               'br': 0.34, 'mc_eff' : 1.0},
    'bbbb':       {'xs': 0.214579739,        'xs_err': 0.0005937000000000001,  'br': 1.0, 'mc_eff' : 1.0},
    'bbcc':       {'xs': 0.5642611098,       'xs_err': 0.0014242000000000002,  'br': 1.0, 'mc_eff' : 1.0},
    'bbdd':       {'xs': 1.335695481632653,  'xs_err': 0.054885714285714295,   'br': 1.0, 'mc_eff' : 1.0},
    'bbuu':       {'xs': 1.4934416640000001, 'xs_err': 0.062472,               'br': 1.0, 'mc_eff' : 1.0},
    'ttbar':      {'xs': 1.7288218499999999, 'xs_err': 0.00010659999999999999, 'br': 1.0, 'mc_eff' : 1.0}
}

_new_dict = {}
for sn,sd in sample_dict.items():
    if re.match(r'kl.*bbbb',sn):
        #Create bbgg dictionaries
        newname=sn.replace('bbbb','bbgg')
        _new_dict[newname] = deepcopy(sd)
        _new_dict[newname]['br'] = 0.1
sample_dict.update(_new_dict)

def getXsWeight(sample_name,nsim,lumi=default_lumi):
    assert sample_name in sample_dict, f'Impossible to find sample \'{sample_name}\' inside xs_dict ({sample_dict})'
    xs     = sample_dict[sample_name]['xs']
    br     = sample_dict[sample_name]['br']
    mc_eff = sample_dict[sample_name]['mc_eff']
    w=(xs*lumi*br)/(nsim*mc_eff)
    return w

def xsweight_like(var,sample_name,lumi=default_lumi,nsim=None):
    if nsim is None: nsim = len(var)
    return np.ones_like(var)*getXsWeight(sample_name,nsim,lumi=lumi)

def lin_comb(kl,d_kl_zero,d_kl_one,d_kl_five):
    '''
    Function which provides the linear combination of mumu -> HH nunu using as base kl=0,1,5
    '''
    f0=(kl**2-6*kl)/5. +1
    f1=(-kl**2+5*kl)/4.
    f5=(kl**2-kl)/20.
    return f0*d_kl_zero+f1*d_kl_one+f5*d_kl_five