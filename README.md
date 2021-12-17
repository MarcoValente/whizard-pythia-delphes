# whizard-pythia-delphes
Docker-based setup to run Whizard, Pythia and Delphes simulation.

## Installqation requirements
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

### Make a centre-of-mass energy scan
A scan of different centre-of-mass energies can be performed through the execution of the [files/scripts/xs_HH_whizard.py](files/scripts/xs_HH_whizard.py) in your terminal. 
```
python3 files/scripts/xs_HH_whizard.py
```
This will simply run a sequence of different `docker-compose` commands to scan different $\sqrt{s}$ values.

## Pythia8: Higgs decay and showering+hadronization
The previous whizard command performs the calculation of the cross-section for the processes specified in the [mumu_HH_xs.sin](files/whizard/mumu_HH_xs.sin) sindarin file. However, the previous command does not produce any output event, generally stored inside Les Houches Event (LHE) files. The [mumu_nunuHH_lhe.sin](files/whizard/mumu_nunuHH_lhe.sin) card contains an example simulating 10k events for the VBF nunuHH process. It can be run with a centre-of-mass energy of 15 TeV through the following command
```
docker-compose run whizard bash /files/scripts/whizard.sh -i files/whizard/mumu_nunuHH_lhe.sin -r "15TeV" -s "sqrts = 30 TeV/sqrts = 15 TeV" -o "/files/output_lhe"
```
You will notice that this command takes significantly longer to run, due to the additional step provided by the generation of 10k events in the LHE file. The output will be stored under the `files/output_lhe/15TeV/mumu_nunuHH.lhe` LHE file. If you explore the file using a text editor, you will see that tThe LHE file we have just produced contains the four-vectors of the neutrinos and the Higgs-bosons. At this stage, the decay of the Higgs did not happen yet.


In order to produce the decay of the Higgs, as well as the showering and hadronization of the output jets, we need to use the Pythia8 framework. Another application of our docker-compose file allows us to run these stages through the [pythia.sh](files/scripts/pythia.sh) script. You can launch Pythia8 on the lhe file we have previously generated using the command: 

```
docker-compose run pythia "/files/scripts/pythia.sh -i /files/output_lhe/15TeV/mumu_nunuHH.lhe -r 15TeV -o /files/output/test_pythia_script/ -c bbgg"
```
You will note that the script takes as input also the channel of the Higgs decays inside the `-c` option. At the moment, only the `bbbb`,`bbgg` and `bbWW` processes have been implemented. When using `bbgg` or `bbWW`, you have to be careful since the Higgs boson is allowed to decay to the WW and bb channels only, but in a double-Higgs decay **there is no forcing of having two distinct Higgs boson decays**. This means that when running `bbWW`, only 50% of the events will decay to `bbWW`. The remaining 50% of events will decay to `bbbb` and `WWWW` and will have to be skimmed at a later stage (this correction can be taken into account inside cross-section value with a scaling of a factor of 2).

The pythia8 output will be stored under the `files/output/test_pythia_script` output directory. The important output files will be
- `output.lhe`: this file is the output LHE file after decay of the Higgs bosons.
- `output.hepmc`: this is the output HEPMC2 file containing the final state hadrons after parton showering and hardonization. This file will be our input for delphes simulation.

## Delphes
Once we have the HEPMC2 file produced by Pythia 8 and containing the final state particles of the decay, it's time to simulate things with Delphes. This can be done using the following command, exploiting the `cards/delphes_card_MuonColliderDet.tcl` delphes card

```
docker-compose run delphes ./DelphesHepMC2 cards/delphes_card_MuonColliderDet.tcl /files/output/delphes_output.root /files/output/test_pythia_script/15TeV/output.hepmc
```
The output root file of Delphes will be available in the `files/output/` directory.