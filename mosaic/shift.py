import cv2
import numpy as np
from mosaic import log
from mosaic import util
from mosaic import fileio
import dxchange
import tomopy

__all__ = ['shift_manual']

def register_shift_sift(datap1, datap2, threshold):
    """Find shifts via SIFT detecting features"""

    mmin1,mmax1 = util.find_min_max(datap1)
    mmin2,mmax2 = util.find_min_max(datap2)
    #print('min *************', mmin)
    #print('max *************', mmax)
    # sift = cv2.xfeatures2d.SIFT_create()
    sift = cv2.SIFT_create()
    shifts = np.zeros([datap1.shape[0],2],dtype='float32')
    for id in range(datap1.shape[0]):       
        tmp1 = ((datap1[id]-mmin1[id]) / (mmax1[id]-mmin1[id])*255.)
        tmp1[tmp1 > 255] = 255
        tmp1[tmp1 < 0] = 0
        tmp2 = ((datap2[id]-mmin2[id]) /
                (mmax2[id]-mmin2[id])*255)
        tmp2[tmp2 > 255] = 255
        tmp2[tmp2 < 0] = 0
        # find key points
        tmp1 = tmp1.astype('uint8')
        tmp2 = tmp2.astype('uint8')
        kp1, des1 = sift.detectAndCompute(tmp1,None)
        kp2, des2 = sift.detectAndCompute(tmp2,None)
        if(len(kp1)==0 or len(kp2)==0):
            shifts[id] = np.nan  
            continue
        
        # cv2.imwrite('original_image_right_keypoints.png',cv2.drawKeypoints(tmp1,kp1,None))
        # cv2.imwrite('original_image_left_keypoints.png',cv2.drawKeypoints(tmp2,kp2,None))
        match = cv2.BFMatcher()
        matches = match.knnMatch(des1,des2,k=2)
        good = []
        #VN: temporarily solution, knnMatch returns strange shape sometimes
        if(len(matches)==0):
            shifts[id] = np.nan  
            continue
        if(len(matches[0])!=2):
            shifts[id] = np.nan  
            continue
        for m,n in matches:
            if m.distance < threshold*n.distance:
                good.append(m)
        log.info('Number of matched features %d',len(good))
        draw_params = dict(matchColor=(0,255,0),
                            singlePointColor=None,
                            flags=2)
        if(len(good)==0):
            log.warning("No features found for projection %d, set shifts to nan", id)
            shifts[id] = np.nan   
            continue
        # tmp3 = cv2.drawMatches(tmp1,kp1,tmp2,kp2,good,None,**draw_params)
        # cv2.imwrite("original_image_drawMatches.jpg", tmp3)
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        shift = (src_pts-dst_pts)[:,0,:]
        shifts[id] = np.median(shift,axis=0)[::-1]        
        shifts=-shifts
        
        # cv2.imwrite("/data/2022-10/Nikitin/tmp/test1.jpg",np.roll(np.roll(tmp2,int(np.round(-shifts[id][1])),axis=1),int(np.round(-shifts[id][0])),axis=0))
        # cv2.imwrite("/data/2022-10/Nikitin/tmp/test2.jpg",tmp1)                
    return shifts


def shift_manual(args):

    print(args.mosaic_fname)
    # read files grid and retrieve data sizes
    meta_dict, grid, data_shape, data_type, x_shift, y_shift = fileio.tile(args)

    log.info('image   size (x, y) in pixels: (%d, %d)' % (data_shape[2], data_shape[1]))
    log.info('mosaic shift (x, y) in pixels: (%d, %d)' % (x_shift, y_shift))
    log.warning('tile overlap (x, y) in pixels: (%d, %d)' % (data_shape[2]-x_shift, data_shape[1]-y_shift))

    columns = [f'x_{num}' for num in range(grid.shape[0])]
    index = [f'y_{num}' for num in range(grid.shape[0])]
    
    [ntiles_v,ntiles_h] = grid.shape
    # ids for slice and projection for shifts testing
    idproj = int((data_shape[0]-1)*args.nprojection)
    
    # find shifts in horizontal direction
    shifts_h = np.zeros([ntiles_v,ntiles_h,2], dtype=np.float32)    
    for iy in range(ntiles_v):    
        for ix in range(ntiles_h-1):
            proj0, flat0, dark0, _ = dxchange.read_aps_tomoscan_hdf5(grid[iy,ix], proj=(idproj,idproj+1))
            proj1, flat1, dark1, _ = dxchange.read_aps_tomoscan_hdf5(grid[iy,ix+1], proj=(idproj,idproj+1))
            print(grid[iy,ix],grid[iy,ix+1])
            norm0 = tomopy.normalize(proj0, flat0, dark0)
            norm1 = tomopy.normalize(proj1, flat1, dark1)
            wx = int((norm0.shape[2] - x_shift)*1)
            shift = register_shift_sift(norm1[:,:,-wx:], norm0[:,:,:wx],args.threshold)
            print(shift)
            shift = shift[~np.isnan(shift[:,0])]
            if (len(shift)==0):
                shift = np.array([[0,0]])
            shifts_h[iy,ix+1] = [np.median(shift[:,0]),np.median(wx-shift[:,1])]                        
            
    # find shifts in vertical direction    
    shifts_v = np.zeros([ntiles_v,ntiles_h,2], dtype=np.float32)    
    for ix in range(ntiles_h):
        for iy in range(ntiles_v-1):            
            proj0, flat0, dark0, _ = dxchange.read_aps_tomoscan_hdf5(grid[iy,ix], proj=(0, data_shape[0]))
            proj1, flat1, dark1, _ = dxchange.read_aps_tomoscan_hdf5(grid[iy+1,ix], proj=(0, data_shape[0]))
            norm0 = tomopy.normalize(proj0, flat0, dark0)
            norm1 = tomopy.normalize(proj1, flat1, dark1)
            wy = int((norm0.shape[1] - y_shift)*1)
            shift = register_shift_sift(norm0[:,-wy:,:], norm1[:,:wy,:],args.threshold)
            shift = shift[~np.isnan(shift[:,0])]
            if (len(shift)==0):
                shift = np.array([[0,0]])
            shifts_v[iy+1,ix] = [np.median(wy-shift[:,0]),np.median(shift[:,1])]            
    log.info('Horizontal shifts')
    log.info(shifts_h)
    log.info('Vertical shifts')
    log.info(shifts_v)

    shifts_h_fname = 'shift_h.txt'
    shifts_v_fname = 'shift_v.txt'
    # fileio.service_fnames(args.mosaic_fname)
    # reshaping the array from 3D matrice to 2D matrice.
    fileio.write_array(shifts_h_fname, shifts_h)
    fileio.write_array(shifts_v_fname, shifts_v)
    
    return shifts_h, shifts_v

