import numpy as np
import cv2

def count_cells(imgtmp):
    # See how many cells were identified in the images (ranged in the "unique" vectors)
    uniquetmp, countstmp = np.unique(imgtmp, return_counts=True)
    # In registered images, it can happen that one cell gets skipped in the unique1 array, which leads to number of cells in unique1 and counts1 NOT MATCHING the unique1 indices. I thus create a unique11 array with continuous cell indices, to be used to track daughters that are still unmatched.
    uniquecorrected = np.array(range(0, len(uniquetmp)))
    return uniquetmp, countstmp, uniquecorrected

def compute_centroids(uniquetmp, imgtmp):
    my_arraytmp = np.empty((0,2), int)
    for mask_tmp in uniquetmp[1:]:
        # Keep only current mask, replace all other values by 0
        img_mask = np.where(imgtmp != mask_tmp, 0, imgtmp)
        
        # compute cell centroid
        M = cv2.moments(img_mask)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        my_arraytmp=np.append(my_arraytmp,[[cx,cy]], axis=0)
    return(my_arraytmp)
