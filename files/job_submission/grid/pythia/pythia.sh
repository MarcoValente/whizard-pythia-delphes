in_tar=""

EXECUTABLE_NAME="shower_plus_hdecay"
hh_channel=""
applyFilter="false"

while getopts i:c:f: flag
do
    case "${flag}" in
        i) in_tar=${OPTARG};;
        c) hh_channel=${OPTARG};;
        f) applyFilter="true";;
    esac
done

#Compiling the script
bash compile.sh

echo "Library path = $LD_LIBRARY_PATH"

IFS=',' read -r -a tararray <<< "$in_tar"

for index in "${!tararray[@]}"
do
    fname="${tararray[index]}"
    echo "Looping on file $index: ${fname}"
    
    #Extracting input
    lhe_file=$(tar -xvf $fname)
    head $lhe_file

    #Creating output lhe hepmc
    output_lhe="output${index}_pythia.lhe"
    output_hepmc="output${index}_pythia.hepmc"

    echo ""
    echo "-----------------------------------------------------------"
    echo "in_tar       : \"$fname\"";
    echo "lhe_file     : \"$lhe_file\"";
    echo "hh_channel   : \"$hh_channel\"";
    echo "output_lhe   : \"$output_lhe\"";
    echo "output_hepmc : \"$output_hepmc\"";
    echo "applyFilter  : \"$applyFilter\"";
    echo "-----------------------------------------------------------"
    echo ""
          
    #Running the script
    echo "Executing $EXECUTABLE_NAME ..."
    ./$EXECUTABLE_NAME "$hh_channel" "$lhe_file" "$output_hepmc" "$output_lhe" "$applyFilter" 

done

ls *

