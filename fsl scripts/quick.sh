OUTPUT_DIR=$'/home/mrinalmanu/Documents/control_conflic_jc/raw_data'

filename=$'quick.txt'
out_dir=$"set fmri(outputdir) "$OUTPUT_DIR""


#sed -i -e "s#HERE#$out_dir#g" $OUTPUT_DIR/$filename

sed -i 's#.nii.gz##g' $OUTPUT_DIR/$filename
#sed "s#$var#replace#g" 

