import os

#common_ops='-d'
common_ops=''

inputs=[
    #'user.valentem.pythia.HH_klm1.10TeV.bbgg.220903_1638_hepmc',
    #'user.valentem.pythia.HH_klm1.10TeV.bbbb.220903_1637_hepmc',
    #'user.valentem.pythia.HH_kl0.10TeV.bbgg.220903_1637_hepmc',
    #'user.valentem.pythia.HH_kl0.10TeV.bbbb.220903_1637_hepmc',
    #'user.valentem.pythia.HH_kl1.10TeV.bbgg.220903_1637_hepmc',
    #'user.valentem.pythia.HH_kl1.10TeV.bbbb.220903_1637_hepmc',
    #'user.valentem.pythia.HH_kl2p5.10TeV.bbgg.220903_1636_hepmc',
    #'user.valentem.pythia.HH_kl2p5.10TeV.bbbb.220903_1636_hepmc',
    #'user.valentem.pythia.HH_kl5.10TeV.bbgg.220903_1636_hepmc',
    #'user.valentem.pythia.HH_kl5.10TeV.bbbb.220903_1636_hepmc',
    #'user.valentem.pythia.mumu_bbbb.10TeV.NONE.220903_1635_hepmc',
    #'user.valentem.pythia.mumu_bbcc.10TeV.NONE.220905_0254_hepmc',
    #'user.valentem.pythia.mumu_bbdd.10TeV.NONE.220905_1632_hepmc',
    #'user.valentem.pythia.mumu_bbuu.10TeV.NONE.220905_0255_hepmc',
    #'user.valentem.pythia.mumu_ttbar.10TeV.NONE.220905_0255_hepmc',
    'user.valentem.pythia.mumu_bbss.10TeV.NONE.220905_2006_hepmc',
]

for inDS in inputs:
    os.system(f'python3 submit_grid.py {inDS} {common_ops}')
