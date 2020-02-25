
FSLDIR=/usr/local/fsl
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH

echo "Step 2: FEAT, particularly Motion correction, slice timing correction and spatial smoothing FWHM"

# We will use the design.fsf file to construct all the parameters, a lot of editing, particularly for input and output has to be done

FILES=$(ls $PWD/sub-*/func/*.nii.gz | xargs -n 1 basename)
INFILES=($FILES)
# pop last element of this array
# unset 'INFILES[${#INFILES[@]}-1]'

NAMES=$(ls $PWD/sub-*/func/*.nii.gz | xargs -n 1 basename | sed 's/.nii.gz//')
NAME=($NAMES)

len=${#INFILES[@]}
# it's better to check the length and minus one from it
vals=$(seq 0 1 218)

# I have to create a file called sample_load.txt, this is done to correctly count the number of sample prefixes
# Following commands were used to create this file
#
# tree sub*/func/*.nii.gz > sample_load.txt
# 
# now grepping all the sample prefixes with correct counts
#
# grep -oh 'sub-.../' sample_load.txt | sed 's/\///g' > DIRS.txt
#
# This was just to highlight the process how I came up with the following one liner

DIRS=$(tree sub*/func/*.nii.gz | grep -oh 'sub-.../' | sed 's/\///g')

DIR=($DIRS)

OUTPUT_DIR=$PWD/feat

# once again more complicated bit, I wanted the matching images for the subject tags, the reason I did this was because, some subjects may have unequal number of .nii.gz images

for i in $vals; do
 echo $PWD/extracted_brains/${DIR[i]}_T1w/${DIR[i]}.extracted_brain.nii.gz >> arr.txt
done

IMAGE_FILES=$(cat  arr.txt |tr "\n" " ")
rm arr.txt
IMAGE=($IMAGE_FILES)

# path to design.fsf
FSF=$PWD/design.fsf

mkdir -p "$OUTPUT_DIR"

  # We need to edit the following entries in design.fsf
# Output directory
# set fmri(outputdir) "SET_OUT_DIR_HERE"

# 4D AVW data or FEAT directory (1)
# set feat_files(1) "SET_INFILE_HERE"

# Subject's structural image for analysis 1
# set highres_files(1) "SET_IMAGE_FILE_HERE"
#

# In the upcoming control statement I am going to create individual
# FSF file and then call feat upon them for all the given samples

for i in $vals; do
  TEMP_DIR=$"$OUTPUT_DIR/${NAME[i]}"
  mkdir -p $TEMP_DIR

  cp "$FSF" "$TEMP_DIR/${NAME[i]}.fsf"
  out_dir=$"set fmri(outputdir) '"$TEMP_DIR"'"
  image_file=$"set highres_files(1) '"${IMAGE[i]}"'"
  feat_file=$"set feat_files(1) '"$PWD/${DIR[i]}/func/${INFILES[i]}"'"

  # I realised later that we need a fourth variable called vols
  # feat goes haywire if the number of vols don't match, we can use
  # fslnvols to do that  
  vols=$(fslnvols $PWD/${DIR[i]}/func/${INFILES[i]})

  # append all these options to the end of FSF file
 
  # I had to use octothrope (hash #) character in sed expression because
  # our variables contain a '/' (slash) character

  sed -i "s#"SET_OUTPUT_DIR_HERE"#$out_dir#g" "$TEMP_DIR/${NAME[i]}.fsf"
  sed -i "s#"SET_INFILE_HER"E#$feat_file#g" "$TEMP_DIR/${NAME[i]}.fsf"
  sed -i "s#"SET_IMAGE_FILE_HERE"#$image_file#g" "$TEMP_DIR/${NAME[i]}.fsf"
  sed -i "s#"NTPS"#$vols#g" "$TEMP_DIR/${NAME[i]}.fsf"
  # replace .nii.gz with nothing, it is giving problem in input names
  sed -i 's#.nii.gz##g' "$TEMP_DIR/${NAME[i]}.fsf"
  # globally replacing single quotes with double quotes
  sed -i "y/'/\"/" "$TEMP_DIR/${NAME[i]}.fsf"

done

###
# execute FEAT for the given FSF files in parallel!
###

FSF_FILES=$(ls feat/*/*.fsf)
IN_FSF=($FSF_FILES)

# semaphores and parallel execution, I choose 6 cores, out of 8 cores
# sudo apt-get install parallel

seq 219 | parallel -j6 feat ::: ${IN_FSF[@]}

echo "Done!"

# end of script


