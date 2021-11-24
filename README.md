# whizard-pythia-delphes
Docker-based setup to run Whizard, Pythia and Delphes simulation.

## Run Whizard cross-section calculation for HH at Muon Collider
In order to run a simple Whizard-based cross-section calculation for HH at the muon-collider, you can execute this command:
```
docker-compose run whizard bash /files/scripts/whizard.sh -i files/whizard/mumu_HH_xs.sin -r "15TeV" -s "sqrts = 30 TeV/sqrts = 15 TeV" -o "/files/output"
```
What is this doing? The `docker-compose run whizard` part of the command says that it needs to run the whizard service described in the [docker-compose.yml](docker-compose.yml) file. This service specifies which docker image to use and also which volumes to setup. The second part of the command specifies the bash command that needs to be executed inside the docker image. In this case, this corresponds to
```
bash /files/scripts/whizard.sh -i files/whizard/mumu_HH_xs.sin -r "15TeV" -s "sqrts = 30 TeV/sqrts = 15 TeV" -o "/files/output"
```
This script and files loaded directly from the volume `/files` which corresponds to the [files/](files/) directory in this repository. This means that the script that is executed is the [files/scripts/whizard.sh](files/scripts/whizard.sh) script. The various arguments correspond to:
  
- `-i` specifies the input SINDARIN file to use to setup Whizard.
- `-r` specifies the name of the run.
- `-s` is used to substitute strings in the provided SINDARIN file. For example, ` -s "sqrts = 30 TeV/sqrts = 15 TeV"` will replace the string `sqrts = 30 TeV` with the other string `sqrts = 15 TeV`, resulting in a change to the total centre-of-mass energy of the muon collision.
- `-o` specifies the output directory where output files will be stored. After executing our program everything should appear under your `files/output` directory. ;)