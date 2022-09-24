from subprocess import Popen
import os
from datetime import datetime as dt
from optparse import OptionParser
from pprint import pprint as p

parser = OptionParser('submit_grid [OPTIONS] [inDS]')
parser.add_option("-d", "--dry-run",    action='store_true', default=False, help="Enable dry-run")

(options, args) = parser.parse_args()
p('Options:')
p(vars(options))
p('Arguments:')
p(args)

for inDS in args:
    proc_string='.'.join(inDS.split('.')[3:6])
    info=f'{proc_string}'
    
    docker_image="docker://valentem1992/delphes:3.5.0"
    outputs = {
               'root':'*.root',
               'out':'*',
              }
    singularity_exec = f"bash delphes.sh -i %IN"
    
    username=os.environ.get('USER')
    assert username!='', "Username variable $USER is empty"
    
    outDS=f"user.{username}.delphes.{info}.{dt.now().strftime('%y%m%d_%H%M')}"
    
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
