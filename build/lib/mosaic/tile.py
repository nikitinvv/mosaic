from mosaic import fileio
from mosaic import log
import pandas as pd
__all__ = ['tiling']

def tiling(args):
    #tile_dict, grid, data_shape, x_shift, y_shift = fileio.tile(args)
    meta_dict, grid, data_shape, data_type, x_shift, y_shift = fileio.tile(args)
    log.info('image   size (x, y) in pixels: (%d, %d)' % (data_shape[2], data_shape[1]))
    log.info('mosaic shift (x, y) in pixels: (%d, %d)' % (x_shift, y_shift))
    log.warning('tile overlap (x, y) in pixels: (%d, %d)' % (data_shape[2]-x_shift, data_shape[1]-y_shift))

    index = [f'x_{num}' for num in range(grid.shape[0])]
    columns = [f'y_{num}' for num in range(grid.shape[1])]
    log.info('mosaic file name grid:\n%s' % pd.DataFrame(grid, columns=columns, index=index))
