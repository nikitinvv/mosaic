import dxchange
import numpy as np

from tile import log
from tile import fileio
import h5py

__all__ = ['extract_borders']

def extract_borders(args):
    """Extract borders from projections for further search of shifts"""

    # read files grid and retrieve data sizes
    meta_dict, grid, data_shape, data_type, x_shift, y_shift = fileio.tile(args)

    log.info('image   size (x, y) in pixels: (%d, %d)' % (data_shape[2], data_shape[1]))
    log.info('stitch shift (x, y) in pixels: (%d, %d)' % (x_shift, y_shift))
    log.warning('tile overlap (x, y) in pixels: (%d, %d)' % (data_shape[2]-x_shift, data_shape[1]-y_shift))

    # check if flip is needed for having tile[0,0] as the left one and at sample_x=0
    sample_x = args.sample_x
    x0 = meta_dict[grid[0,0]][sample_x][0]
    x1 = meta_dict[grid[0,-1]][sample_x][0]
    # if(x0+x1>0):
        # step = -1
    # else:
    step = 1
    
    # ids for slice and projection for shifts testing
    idproj = int((data_shape[0]-1)*args.nprojection)
    # idproj = np.arange(0,2000,100)
    for jtile in range(grid.shape[1]):              
        with h5py.File(grid[0,::-step][jtile],'r') as fid:
            data = fid['/exchange/data'][idproj,:,:data_shape[2]-x_shift]
            dark = fid['/exchange/data_dark'][:,:,:data_shape[2]-x_shift]
            flat = fid['/exchange/data_white'][:,:,:data_shape[2]-x_shift]
            data = (data-np.mean(dark,axis=0))/np.maximum(1e-3,(np.mean(flat,axis=0)-np.mean(dark,axis=0)))
            dxchange.write_tiff(data.astype('float32'),f'{args.folder_name}/tile_rec/tile_proj/p{jtile}0',overwrite=True)       
            data = fid['/exchange/data'][idproj,:,-(data_shape[2]-x_shift):]
            dark = fid['/exchange/data_dark'][:,:,-(data_shape[2]-x_shift):]
            flat = fid['/exchange/data_white'][:,:,-(data_shape[2]-x_shift):]
            data = (data-np.mean(dark,axis=0))/np.maximum(1e-3,(np.mean(flat,axis=0)-np.mean(dark,axis=0)))
            dxchange.write_tiff(data.astype('float32'),f'{args.folder_name}/tile_rec/tile_proj/p{jtile}1',overwrite=True)       
            
            
        
        
            