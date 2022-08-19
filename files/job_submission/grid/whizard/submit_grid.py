from subprocess import Popen
import os
from datetime import datetime as dt
from optparse import OptionParser
from pprint import pprint as p

parser = OptionParser('submit_grid [OPTIONS] [inDS]')
parser.add_option("-d", "--dry-run",  action='store_true', default=False, help="Enable dry-run")
parser.add_option("-n", "--info",     default='', help="Info for GRID job output name")
parser.add_option("-s", "--subs-str", default='', help="Substitution string")

(options, args) = parser.parse_args()
p('Options:')
p(vars(options))
p('Arguments:')
p(args)

docker_image="docker://whizard/whizard-weekly:master"
outputs = {
           'lhe':'*.lhe',
        #    'out':'*',
          }

for sin_file in args:
    singularity_exec = f"./whizard.sh -i {sin_file}"
    if options.subs_str!='': singularity_exec+=f' -s {options.subs_str}'

    username=os.environ.get('USER')
    assert username!='', "Username variable $USER is empty"

    outDS=f"user.{username}.singularity_whizard.{options.info}.{dt.now().strftime('%y%m%d_%H%M')}"

    command=["prun",
            "--exec", singularity_exec,
            "--containerImage", docker_image,
            "--outputs", ",".join([f'{name}:{out}' for name,out in outputs.items()]),
            "--outDS", f"{outDS}"]

    print(' '.join(command))
    if not options.dry_run:
        process=Popen(command)
        process.wait()
