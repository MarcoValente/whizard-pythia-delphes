# whizard-pythia-delphes
Docker-based setup to run Whizard, Pythia and Delphes simulation.

## Install requirements
First, ensure you have installed some useful packages
```
pip install -r requirements.txt
```
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

### Make a $\sqrt{s}$ energy scan
A scan of different centre-of-mass energies can be performed through the execution of the [files/scripts/xs_HH_whizard.py](files/scripts/xs_HH_whizard.py) in your terminal. 
```
python3 files/scripts/xs_HH_whizard.py
```
This will simply run a sequence of different `docker-compose` commands to scan different $\sqrt{s}$ values.

## Pythia8

```
docker-compose run pythia "/files/scripts/pythia.sh -i /files/output/whizard/mumu_HH_xs_restr_lhe/0.9TeV/mumu_nunuHH.lhe -r 0.9TeV -o /files/output/test_pythia_script/0.9TeV -c bbbb"
```

## Delphes

```
docker-compose run delphes ./DelphesHepMC2 cards/delphes_card_MuonColliderDet.tcl delphes_output.root /files/output/test_pythia_script/30.0TeV/output.hepmc
```

```
docker-compose run delphes make display && root -l "examples/EventDisplay.C(\"cards/delphes_card_ATLAS.tcl\",\"/files/output/delphes/30.0TeV/delphes_output_ATLAS.root\")"
```