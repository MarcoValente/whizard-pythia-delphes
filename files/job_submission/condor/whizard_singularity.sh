#!/bin/bash
echo "Starting job..."
echo "Listing content of $PWD"
ls -l *

return 0 


IMAGE="/afs/cern.ch/user/v/valentem/work/MuonCollider/Singularity/wizhard_2022-08-12.sif"
INPUT_SINFILE="$1"

RUNNAME="$(basename $INPUT_SINFILE)"
#SUBSTR="gh3=1/gh3=2.0"
SUBSTR=""

DATE="$(date +"%Y%m%d")_$(date +'%H%M')"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MAIN_DIR="/afs/cern.ch/user/v/valentem/MuonCollider/whizard-pythia-delphes"

OUTNAME="${MAIN_DIR}/files/output/${DATE}_$RUNNAME"

COMMAND="singularity exec $IMAGE \
bash ${MAIN_DIR}/files/scripts/whizard_condor.sh \
-i $INPUT_SINFILE \
-r '$RUNNAME' \
-s '$SUBSTR' \
-o '$OUTNAME' \
"

echo -----------------------------------------------------------------
echo INPUT_SINFILE= $INPUT_SINFILE
echo
echo MAIN_DIR = $MAIN_DIR
echo IMAGE    = $IMAGE
echo RUNNAME  = $RUNNAME
echo SUBSTR   = $SUBSTR
echo OUTNAME  = $OUTNAME
echo
echo COMMAND  = $COMMAND
echo -----------------------------------------------------------------

eval $COMMAND
