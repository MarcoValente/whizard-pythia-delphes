
def lin_comb(kl,d_kl_zero,d_kl_one,d_kl_five):
    '''
    Function which provides the linear combination of mumu -> HH nunu using as base kl=0,1,5
    '''
    f0=(kl**2-6*kl)/5. +1
    f1=(-kl**2+5*kl)/4.
    f5=(kl**2-kl)/20.
    return f0*d_kl_zero+f1*d_kl_one+f5*d_kl_five