import os

#common_ops='-d'
common_ops=''

backgrounds_inDS=[
    #'user.valentem.whizard.mumu_bbbb.10TeV.220903_0037_lhe',
    #'user.valentem.whizard.mumu_bbcc.10TeV.220903_0021_lhe',
    #'user.valentem.whizard.mumu_bbdd.10TeV.220903_0021_lhe',
    'user.valentem.whizard.mumu_bbss.10TeV.220905_1912_lhe',
    #'user.valentem.whizard.mumu_bbuu.10TeV.220903_0021_lhe',
    #'user.valentem.whizard.mumu_ttbar.10TeV.220903_0022_lhe',
]

signal_inDS=[
    #'user.valentem.whizard.HH_kl5.10TeV.220903_0038_lhe',
    #'user.valentem.whizard.HH_kl2p5.10TeV.220903_0038_lhe',
    #'user.valentem.whizard.HH_kl1.10TeV.220903_0037_lhe/',
    #'user.valentem.whizard.HH_kl0.10TeV.220903_0038_lhe',
    #'user.valentem.whizard.HH_klm1.10TeV.220903_0038_lhe',
]

hh_channels=['bbbb','bbgg']

for inDS in backgrounds_inDS:
    os.system(f'python3 submit_grid.py {inDS} {common_ops}')


for inDS in signal_inDS:
    for hh_channel in hh_channels:
        os.system(f'python3 submit_grid.py {inDS} -c {hh_channel} {common_ops}')
