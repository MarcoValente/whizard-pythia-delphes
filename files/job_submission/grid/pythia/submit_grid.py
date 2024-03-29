from subprocess import Popen
import os
from datetime import datetime as dt
from optparse import OptionParser
from pprint import pprint as p

parser = OptionParser('submit_grid [OPTIONS] [inDS]')
parser.add_option("-d", "--dry-run",    action='store_true', default=False, help="Enable dry-run")
parser.add_option("-c", "--hh-channel", default='NONE', choices=['NONE','bbbb','bbgg'], type='choice', help="Output channel")

(options, args) = parser.parse_args()
p('Options:')
p(vars(options))
p('Arguments:')
p(args)

applyFilter=(options.hh_channel!='NONE')


for inDS in args:
    proc_string='.'.join(inDS.split('.')[3:5])
    info=f'{proc_string}.{options.hh_channel}'
    
    docker_image="docker://matthewfeickert/pythia-python"
    outputs = {
               'lhe':'*pythia.lhe',
               'hepmc':'*pythia.hepmc',
               #'out':'*',
              }
    singularity_exec = f"bash pythia.sh -i %IN -c {options.hh_channel}"
    if applyFilter: singularity_exec+=" -f true"
    
    username=os.environ.get('USER')
    assert username!='', "Username variable $USER is empty"
    
    outDS=f"user.{username}.pythia.{info}.{dt.now().strftime('%y%m%d_%H%M')}"
    
    command=["prun", "--forceStaged", 
             "--exec", singularity_exec,
             "--containerImage", docker_image,
             "--outputs", ",".join([f'{name}:{out}' for name,out in outputs.items()]),
             "--outDS", outDS,
             "--inDS", inDS,
             "--nFilesPerJob", "1",
             #"--site", "BNLLAKE"
             #"--wrapExecInContainer",
            ]
    
    print(' '.join(command))
    if not options.dry_run:
        process=Popen(command)
        process.wait()
