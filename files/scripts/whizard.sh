basename="/"

sin_name="files/whizard/mumu_HH.sin"
run_name=""
output_dir="/files/output"
substitute_str=""

while getopts i:r:o:s: flag
do
    case "${flag}" in
        i) sin_name=${OPTARG};;
        r) run_name=${OPTARG};;
        o) output_dir=${OPTARG};;
        s) substitute_str=${OPTARG};;
    esac
done

MAINDIRNAME="/tmp/tmp_$RANDOM/$run_name"
PREFIXDIR="/"
STEERINGSIN_NAME="streering.sin"

echo "MAINDIRNAME      : $MAINDIRNAME";
echo "STEERINGSIN_NAME : $STEERINGSIN_NAME";
echo ""
echo "-----------------------------------------------------------"
echo "sin file              : \"$sin_name\"";
echo "run name              : \"$run_name\"";
echo "output directory name : \"$output_dir\"";
echo "-----------------------------------------------------------"
echo ""

#Executing the script
sleep 2
mkdir -p $MAINDIRNAME && cd $MAINDIRNAME
cp "$PREFIXDIR$sin_name" $STEERINGSIN_NAME
if [ ! -z "${substitute_str}" ]; 
    then 
    echo "Replacing string $substitute_str" 
    sed -i "s/$substitute_str/g" $STEERINGSIN_NAME
fi
whizard -r $STEERINGSIN_NAME
mkdir -p $output_dir && cp -r $MAINDIRNAME $output_dir
cd -;