import cv2
import numpy as np
import pandas as pd
from skimage import io
import sys
import glob

# scipy package to compute distance between matrices of cell centroid coordinates
from scipy.spatial.distance import cdist
# skimage package to identify objects, export region properties
from skimage.measure import label, regionprops, regionprops_table

# List files in current folder
files_list = sorted(glob.glob("*.tif"))

# Get variables from system env
output_dir = sys.argv[1]

for tp in range(0,len(files_list)):
    #print('Processing file ', files_list[tp])
    img1 = io.imread(files_list[tp])
    
    # See how many cells were identified in the images (ranged in the "unique" vectors)
    unique1, counts1 = np.unique(img1, return_counts=True)
    # In registered images, it can happen that one cell gets skipped in the unique1 array, which leads to number of cells in unique1 and counts1 NOT MATCHING the unique1 indices. I thus create a unique11 array with continuous cell indices, to be used to track daughters that are still unmatched.
    #unique11 = np.array(range(0, len(unique1)))
    #unique0, counts0 = np.unique(img0, return_counts=True)
    #unique01 = np.array(range(0, len(unique0)))
    
    ###################################################
    # compute the mask centroids of all cells in img1 #
    ###################################################
    my_array1 = np.empty((0,2), int)
    for mask_tmp in unique1[1:]: # [:1] because I'm not interested in pixels with a value of 0: the background
        # Keep only current mask, replace all other values by 0
        img_tmp = np.where(img1 != mask_tmp, 0, img1)
    
        # compute cell centroid
        M = cv2.moments(img_tmp)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        my_array1=np.append(my_array1,[[cx,cy]], axis=0)
    
    ###################################################################################
    # Compute distances between cells (in a similar way to R's pdist::pdist function) #
    ###################################################################################
    dist_mat = cdist(my_array1, my_array1)
    
    if (dist_mat.shape[0] <= 3):
        first_closest = np.repeat(0, dist_mat.shape[0])
        second_closest = np.repeat(0, dist_mat.shape[0])
    else:
        # extract 1st and 2nd closest distance of each cell's neighbours
        first_closest = [sorted(i)[1] for i in zip(*dist_mat)]
        second_closest = [sorted(i)[2] for i in zip(*dist_mat)]
    
    ###############################################################################
    # extract features for all cells using the skimage regionprops table function #
    ###############################################################################
    
    props = regionprops_table(img1, properties=['area', 'bbox', 'centroid', 'eccentricity', 'euler_number', 'extent', 'axis_minor_length', 'axis_major_length', 'feret_diameter_max', 'orientation', 'perimeter', 'solidity'])
    
    # turn props into a panda data.frame
    data_tmp = pd.DataFrame(props)
    
    # add closest neighbour distance columns
    data_tmp['Neighbors_FirstClosestDistance'] = first_closest
    data_tmp['Neighbors_SecondClosestDistance'] = second_closest
    
    #########################################################
    # Export feature cell information for the current image #
    #########################################################
    data_tmp.to_csv(output_dir + f"feature_table_time{tp}.csv")

