import numpy as np

default_lumi=100 #fb-1

sample_dict = {
    'kl0'   : {'xs' : 1.7886309E+00, 'xs_err' : 2.36E-04, 'br': 1.0, 'mc_eff' : 1.0}, #fb
    'kl1'   : {'xs' : 8.4135252E-01, 'xs_err' : 1.59E-04, 'br': 1.0, 'mc_eff' : 1.0}, #fb
    'kl2p5' : {'xs' : 9.4704270E-01, 'xs_err' : 1.60E-04, 'br': 1.0, 'mc_eff' : 1.0}, #fb
    'kl5'   : {'xs' : 5.1948298E+00, 'xs_err' : 5.91E-04, 'br': 1.0, 'mc_eff' : 1.0}, #fb
    'klm1'  : {'xs' : 3.5504185E+00, 'xs_err' : 3.76E-04, 'br': 1.0, 'mc_eff' : 1.0}, #fb
}

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