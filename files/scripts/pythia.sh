basename="/"

lhe_name=""
run_name=""
output_dir=""
hh_channel="bbgg"

while getopts i:r:o:c: flag
do
    case "${flag}" in
        i) lhe_name=${OPTARG};;
        r) run_name=${OPTARG};;
        o) output_dir=${OPTARG};;
        c) hh_channel=${OPTARG};;
    esac
done

MAINDIRNAME="/tmp/tmp_$RANDOM/$run_name"
PREFIXDIR="/"
LHE_FILENAME="input.lhe"
PYTHIA_SCRIPT_DIR="/files/pythia8"
EXECUTABLE_NAME="shower_plus_hdecay"

echo "MAINDIRNAME  : $MAINDIRNAME";
echo "LHE_FILENAME : $LHE_FILENAME";
echo ""
echo "-----------------------------------------------------------"
echo "lhe file              : \"$lhe_name\"";
echo "run name              : \"$run_name\"";
echo "output directory name : \"$output_dir\"";
echo "HH channel            : \"$hh_channel\"";
echo "-----------------------------------------------------------"
echo ""

#Executing the script
sleep 2
mkdir -p $MAINDIRNAME && cd $MAINDIRNAME

#Compilation
cp "$PREFIXDIR$lhe_name" $LHE_FILENAME
echo "Starting to compile $EXECUTABLE_NAME.cc ..."

#Execution
cp $PYTHIA_SCRIPT_DIR/* . && bash compile.sh
echo "Executing $EXECUTABLE_NAME ..."
./$EXECUTABLE_NAME "$hh_channel" "$LHE_FILENAME" |& tee pythia.log
mkdir -p $output_dir && cp -r $MAINDIRNAME $output_dir
cd -;