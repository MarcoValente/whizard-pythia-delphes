from subprocess import Popen
import os
from datetime import datetime as dt
from optparse import OptionParser
from pprint import pprint as p

parser = OptionParser('submit_grid [OPTIONS] [inDS]')
parser.add_option("-d", "--dry-run",  action='store_true', default=False, help="Enable dry-run")
parser.add_option("-n", "--info",     default='',      help="Info for GRID job output name")
parser.add_option("-s", "--subs-str", default='',      help="Substitution string")
parser.add_option("-N", "--n-events", default=1000,    help="Number of events per job")
parser.add_option("-j", "--n-jobs",   default=1,       help="Number of jobs")
parser.add_option("-e", "--energy",   default=3,       help="Centre of mass energy (TeV)")

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
    singularity_exec = f"./whizard.sh -i {sin_file} -e \"seed=%RNDM:1234 n_events={options.n_events} sqrts={options.energy}TeV\""
    if options.subs_str!='': singularity_exec+=f' -s {options.subs_str}'

    username=os.environ.get('USER')
    assert username!='', "Username variable $USER is empty"

    info=options.info
    if info=='':
        process_name=os.path.basename(sin_file).split('.')[0]
        info=f'{process_name}'
    info+=f'.{options.energy}TeV'

    outDS=f"user.{username}.whizard.{info}.{dt.now().strftime('%y%m%d_%H%M')}"

    command=["prun",
            "--exec", singularity_exec,
            "--containerImage", docker_image,
            "--outputs", ",".join([f'{name}:{out}' for name,out in outputs.items()]),
            "--outDS", f"{outDS}",
            "--nJobs", f'{options.n_jobs}',
            ]

    print(' '.join(command))
    if not options.dry_run:
        process=Popen(command)
        process.wait()
