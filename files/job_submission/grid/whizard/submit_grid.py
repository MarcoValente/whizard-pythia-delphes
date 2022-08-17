from subprocess import Popen
import os
from datetime import datetime as dt

dry_run=False

info='HH_kl2p5'
docker_image="docker://whizard/whizard-weekly:master"
outputs = {
           'lhe':'*.lhe',
           'out':'*',
          }
singularity_exec = "./whizard.sh -s gh3=1.0/gh3=2.5"
username=os.environ.get('USER')
assert username!='', "Username variable $USER is empty"

outDS=f"user.{username}.singularity_whizard.{info}.{dt.now().strftime('%y%m%d_%H%M')}"

command=["prun",
         "--exec", singularity_exec,
         "--containerImage", docker_image,
         "--outputs", ",".join([f'{name}:{out}' for name,out in outputs.items()]),
         "--outDS", f"{outDS}"]

print(' '.join(command))
if not dry_run:
    process=Popen(command)
    process.wait()
