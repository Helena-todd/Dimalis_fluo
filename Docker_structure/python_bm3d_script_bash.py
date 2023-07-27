from skimage import io, img_as_float
import bm3d
import cv2
import os # to move between directories
import sys # to recover variables from the system environment

# Get variables from system env
origName = sys.argv[1]
denoisedName = sys.argv[2]
directoryPath = sys.argv[3]

sigmaValue = sys.argv[4]

# Change the current directory to the specified directory
os.chdir(directoryPath)
#print("I'm in directory ",directoryPath)

# Read the image, as float
noisy_img = img_as_float(io.imread(origName, as_gray=True))
#print("I read the image ", origName)

# Denoise image
BM3D_denoised = bm3d.bm3d(noisy_img, sigma_psd=float(sigmaValue), stage_arg=bm3d.BM3DStages.ALL_STAGES)
#print("I denoised the image using the sigma value ", sigmaValue)

# export image
cv2.imwrite(denoisedName, BM3D_denoised)
