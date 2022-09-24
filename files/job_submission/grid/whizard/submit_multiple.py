import os

common_opts=''

#os.system(f'python3 submit_grid.py cards/mumu_bbbb.sin --energy 10 --n-events 10000 --n-jobs 10 {common_opts}')
os.system(f'python3 submit_grid.py cards/mumu_bbss.sin --energy 10 --n-events 10000 --n-jobs 50 {common_opts}')
#os.system(f'python3 submit_grid.py cards/mumu_bbuu.sin --energy 10 --n-events 10000 --n-jobs 50 {common_opts}')
#os.system(f'python3 submit_grid.py cards/mumu_bbdd.sin --energy 10 --n-events 10000 --n-jobs 50 {common_opts}')
#os.system(f'python3 submit_grid.py cards/mumu_bbcc.sin --energy 10 --n-events 10000 --n-jobs 50 {common_opts}')
#os.system(f'python3 submit_grid.py cards/mumu_bbdd.sin --energy 10 --n-events 10000 --n-jobs 50 {common_opts}')
#os.system(f'python3 submit_grid.py cards/mumu_ttbar.sin --energy 10 --n-events 10000 --n-jobs 50 {common_opts}')


#os.system(f'python3 submit_grid.py cards/MUONCOLL_hh.sin -s "gh3=1.0/gh3=1.0" -n HH_kl1 --energy 10 --n-events 10000 --n-jobs 10 {common_opts}')
#os.system(f'python3 submit_grid.py cards/MUONCOLL_hh.sin -s "gh3=1.0/gh3=0.0" -n HH_kl0 --energy 10 --n-events 10000 --n-jobs 10 {common_opts}')
#os.system(f'python3 submit_grid.py cards/MUONCOLL_hh.sin -s "gh3=1.0/gh3=-1.0" -n HH_klm1 --energy 10 --n-events 10000 --n-jobs 10 {common_opts}')
#os.system(f'python3 submit_grid.py cards/MUONCOLL_hh.sin -s "gh3=1.0/gh3=2.5" -n HH_kl2p5 --energy 10 --n-events 10000 --n-jobs 10 {common_opts}')
#os.system(f'python3 submit_grid.py cards/MUONCOLL_hh.sin -s "gh3=1.0/gh3=5.0" -n HH_kl5 --energy 10 --n-events 10000 --n-jobs 10 {common_opts}')
