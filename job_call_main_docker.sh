#Call script arguments: /home/test_images/  0.0001  29.5  50    30    skip_denoising
#                       ${1}                ${2}    ${3}  ${4}  ${5}  ${6}

# Move to the folder containing the Raw images
cd ${1}/exported/

# List image files
imgNames="$(ls |grep .tif)"

# Create folder that will contain the denoised images
mkdir -p ${1}/BM3D/${2}

# Loop over the files, create export name, pass those names to the python bm3d script
for MYIMG in ${imgNames}
do
export MYIMG
# create export image name, to give to the python script
MYDENOISEDIMG="denoised_$MYIMG"
export MYDENOISEDIMG

############################
#####       BM3D       #####
############################

if [[ ${6} -eq 0 ]]
then
    # Copy paste raw images to the BM3D directory #, adding a denoised_ prefix
    echo "Skipping cell denoising"
    bm3ddir="${1}/BM3D/${2}"
    cp * ${bm3ddir}
    #cd ${bm3ddir}
    #ls | xargs -I {} mv {} denoised_{}
    #rename '' 'denoised_' *
    #mv denoised* ${1}/BM3D/${2}
elif [[ ${6} -eq 1 ]]
then
    echo "Denoising cells using the BM3D algorithm "
    # call bm3d python script
    python3 /home/scripts/python_bm3d_script_bash.py $MYIMG $MYDENOISEDIMG ${1}/exported ${2}
    # Move images to the directory where they should be
    bm3ddir="${1}/BM3D/${2}"
    mv denoised* ${1}/BM3D/${2}
else
    echo "Please use one of the two denoising options, either 0 (skip denoising) or 1 (denoise) "
fi

done # ends image loop

############################
#####     Omnipose     #####
############################
echo "Segmenting cells in images using the Omnipose algorithm "
# Launch omnipose on the denoised bm3d images
python3 -m cellpose --dir ${bm3ddir} --pretrained_model /home/scripts/bact_omnitorch_0 --diameter ${3} --mask_threshold 2.1 --save_tif --verbose

# Create folder for Omnipose outputs, corrsponding to the selected sigma value
mkdir -p ${1}/Omnipose/${3}

# Move segmented images to the Omnipose directory
cd ${1}/BM3D/${2}
mv *cp_masks.tif ${1}/Omnipose/${3}

##################################
#####    extract features    #####
##################################
echo "Extracting features from the cell masks into tables "

cd ${1}/Omnipose/${3}

# Create folder for feature table outputs
mkdir -p ${1}/feature_tables/
ft_dir="${1}/feature_tables/"

# Launch script to extract features
python3 /home/scripts/extract_features_regionprops.py ${ft_dir}

######################################
#####    extract fluorescence    #####
######################################

# Launch script to extract fluorescence features in each cell
python3 /home/scripts/extract_fluo_features_v3.py ${1}

######################################
#####    STrack cell tracking    #####
######################################

echo "Tracking cells using STrack "

cd ${1}/Omnipose/${3}

# Create folder for STrack outputs
mkdir -p ${1}/STrack/
strack_dir="${1}/STrack/"

# Launch script to extract features
python3 /home/scripts/strack_script_v4.py ${4} ${5} ${strack_dir}

cd ${1}/STrack/

# Launch script to merge STrack results into 2 excel tables
python3 -W ignore /home/scripts/strack_merge_tables.py ${strack_dir}

# Launch script to merge all results (STrack, features, fluo features) into one table
python3 -W ignore /home/scripts/merge_all_tables.py ${1}
