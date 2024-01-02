
import os
from utils import *

fname = '/data/2022-11-Nikitin/slab4/mosaic_rec/mosaic_bin2_rec_bin/'
fnameout = '/data/2022-11-Nikitin/slab4/mosaic_rec/mosaic_bin2_rec_bin_cropped/'

os.system(f'rm -rf {fnameout}*')

files= next(os.walk(f'{fname}'))[2]
nfiles = len(files)
data = tifffile.imread(f'{fname}/{files[-1]}')

stx = 128
sty = 128
stz = 256
endx = data.shape[1]-128
endy = data.shape[0]-128
endz = 450

data = read_parallel(fname,stx,endx,sty,endy,stz,endz)
data[:] = -data

data = rotate_parallel(data,-3.5)
data = data.swapaxes(0,1)
data = rotate_parallel(data,1.5)
data = data.swapaxes(0,1)
data = data.swapaxes(0,2)
data = rotate_parallel(data,2.2)
data = data.swapaxes(0,2)

write_parallel(fnameout,data)

fname = '/data/2022-11-Nikitin/slab4/mosaic_rec/mosaic_bin2_rec_bin_cropped/'
fnameout = '/data/2022-11-Nikitin/slab4/mosaic_rec/mosaic_bin2_rec_bin_cropped_ward/'
# os.system(f'rm -rf {fnameout}/*')

nfiles = len(next(os.walk(f'{fname}'))[2])
id_tmp = nfiles//2
data = tifffile.imread(f'{fname}/recon_{id_tmp:05}.tiff')
stx = 0
sty = 0
stz = 0
endx = data.shape[1]
endy = data.shape[0]
endz = nfiles
data = read_parallel(fname,stx,endx,sty,endy,stz,endz)

data = data.swapaxes(0,1)
mmin = -0.0029269056 
mmax = 0.0068289298    
data = ward_parallel(data,-5,mmin,mmax)
data = data.swapaxes(0,1)

data=data[::-1]
write_parallel(fnameout,data)
exit()

