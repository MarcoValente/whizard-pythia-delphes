in_tar=""

EXECUTABLE_NAME="/app/DelphesHepMC2"
cardname="delphes_card_MuonColliderDet.tcl"

while getopts i:c: flag
do
    case "${flag}" in
        i) in_tar=${OPTARG};;
        c) cardname=${OPTARG};;
    esac
done


IFS=',' read -r -a tararray <<< "$in_tar"

for index in "${!tararray[@]}"
do
    fname="${tararray[index]}"
    echo "Looping on file $index: ${fname}"
 
    output_root="delphes_output${index}.root"

    #Extracting input
    echo "Extracting $fname"
    in_hepmc=$(tar -xvf $fname | xargs)
    
    echo ""
    echo "-----------------------------------------------------------"
    echo "in_tar       : \"$fname\"";
    echo "in_hepmc     : \"$in_hepmc\"";
    echo "cardname     : \"$cardname\""
    echo "output_root  : \"$output_root\"";
    echo "-----------------------------------------------------------"
    echo ""
    
    #Running the script
    
    echo "Executing $EXECUTABLE_NAME ..."
    $EXECUTABLE_NAME "$cardname" "$output_root" $in_hepmc

done

ls *

