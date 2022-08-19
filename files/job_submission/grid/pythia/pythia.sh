in_tar=""

EXECUTABLE_NAME="shower_plus_hdecay"
hh_channel=""

while getopts i:c: flag
do
    case "${flag}" in
        i) in_tar=${OPTARG};;
        c) hh_channel=${OPTARG};;
    esac
done

#Extracting input
lhe_file=$(tar -xvf $in_tar)

echo ""
echo "-----------------------------------------------------------"
echo "in_tar     : \"$in_tar\"";
echo "lhe_file   : \"$lhe_file\"";
echo "hh_channel : \"$hh_channel\"";
echo "-----------------------------------------------------------"
echo ""

#Compiling the script
bash compile.sh

#Running the script

echo "Executing $EXECUTABLE_NAME ..."
./$EXECUTABLE_NAME "$hh_channel" "$lhe_file" |& tee pythia.log

ls *

