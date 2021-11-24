import os

run=True

sqrts_ranges= [0.1*i for i in range(4,10)] + list(range(1,31))

print(f'Looping over sqrts ranges: {sqrts_ranges}')
for sqrts in sqrts_ranges:
    print(f'Calculating xs for sqrts={sqrts:.1f}')
    command=f"docker-compose run whizard bash /files/scripts/whizard.sh \
-i files/whizard/mumu_HH_xs.sin \
-r \"{sqrts:.1f}TeV\" \
-o '/files/output/whizard/mumu_HH_xs_restr_lhe' \
-s \"sqrts = 30 TeV/sqrts = {sqrts:.1f} TeV\""
    print(f'Executing command: {command}')
    if run:
        os.system(command)