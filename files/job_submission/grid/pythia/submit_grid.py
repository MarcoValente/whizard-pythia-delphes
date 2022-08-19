from subprocess import Popen
import os
from datetime import datetime as dt

dry_run=False
hh_channel='bbgg'

inDS="user.valentem.singularity_whizard.HH_klm1.220817_0741_lhe"
kl_string=inDS.split('.')[3]
info=f'{kl_string}.{hh_channel}'

docker_image="docker://matthewfeickert/pythia-python"
outputs = {
           'lhe':'output.lhe',
           'hepmc':'*.hepmc',
           'out':'*',
          }
singularity_exec = f"bash pythia.sh -i %IN -c {hh_channel}"
username=os.environ.get('USER')
assert username!='', "Username variable $USER is empty"

outDS=f"user.{username}.singularity_pythia.{info}.{dt.now().strftime('%y%m%d_%H%M')}"

command=["prun",
         "--exec", singularity_exec,
         "--containerImage", docker_image,
         "--outputs", ",".join([f'{name}:{out}' for name,out in outputs.items()]),
         "--outDS", outDS,
         "--inDS", inDS,
        ]

print(' '.join(command))
if not dry_run:
    process=Popen(command)
    process.wait()
