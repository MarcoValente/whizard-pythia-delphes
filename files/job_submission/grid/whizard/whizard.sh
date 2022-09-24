basename="/"

sin_name="MUONCOLL_hh.sin"
substitute_str=""
execute_cmd=""

while getopts i:o:s:e: flag
do
    case "${flag}" in
        i) sin_name=${OPTARG};;
        o) output_dir=${OPTARG};;
        s) substitute_str=${OPTARG};;
        e) execute_cmd=${OPTARG};;
    esac
done

echo ""
echo "-----------------------------------------------------------"
echo "sin file              : \"$sin_name\"";
echo "substitute_str        : \"$substitute_str\"";
echo "execute_cmd           : \"$execute_cmd\"";
echo "-----------------------------------------------------------"
echo ""

#Executing the script
if [ ! -z "${substitute_str}" ]; 
    then 
    echo "Replacing string $substitute_str" 
    sed -i "s/$substitute_str/g" $sin_name
fi
whizard -r "$sin_name" -e "$execute_cmd"
