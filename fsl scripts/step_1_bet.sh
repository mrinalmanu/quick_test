# the fsldir path has to be specified in order to use fsl
# i find it kind of strange to do this everytime

FSLDIR=/usr/local/fsl
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH


# cd to raw_data folder
cd /home/mrinalmanu/Documents/control_conflic_jc/raw_data

BET=$'/usr/local/fsl/bin/bet'
WR=$'/home/mrinalmanu/Documents/control_conflic_jc/raw_data/'

# It reads like this: list all the files, then extract the basename with .nii.gz prefix, and out of all extracted prefixes remove ':' character, then remove multiple endlines with single endline character, finally store the variable as tags

TAGS=$(ls $PWD/sub-*/anat/ | xargs -n 1 basename | sed 's/.nii.gz//' | sed 's/://g' | tr -s '\n' '\n')

#####################################
echo "Step 1: Brain Extraction"

for TAG in $TAGS; do
  echo 'Running BET for' $TAG
  OUTDIR="/home/mrinalmanu/Documents/control_conflic_jc/raw_data/extracted_brains/$TAG"; mkdir -p "$OUTDIR" 
  # create a variable TEMP which will remove '_T1w' prefix, since our folder names are in this format sub-***
  TEMP=$(echo $TAG | xargs -n 1 basename | sed 's/_T1w//')
  $BET $WR$TEMP/anat/$TAG $OUTDIR/$TEMP.extracted_brain.nii.gz -f 0.5 -g 0 |& tee "$OUTDIR/$TAG.fastqc.log"
done


#####################################





