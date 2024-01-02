
import os
import tifffile
import datetime
from utils import *

fname = '/data/2022-11-Nikitin/alcf/slab3_new/'
fnameout = '/data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped/'
os.system('rm -rf /data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped/*')

stx = (162-32)*8
endx = (162+1536+32)*8
sty = (404)*8
endy = (404+1056)*8
stz = 2608 
endz = 4368

print(datetime.datetime.now(),'step 1')
data = read_parallel(fname,stx,endx,sty,endy,stz,endz)
print(datetime.datetime.now(),'step 2')
data = rotate_parallel(data,7.5)
print(datetime.datetime.now(),'step 3')
data = data.swapaxes(0,1)
print(datetime.datetime.now(),'step 4')
data = rotate_parallel(data,0)
print(datetime.datetime.now(),'step 5')
data = data.swapaxes(0,1)
print(datetime.datetime.now(),'step 6')
data = data.swapaxes(0,2)
print(datetime.datetime.now(),'step 7')
data = rotate_parallel(data,1.2-5.1+2.7)
print(datetime.datetime.now(),'step 8')
data = data.swapaxes(0,2)
print(datetime.datetime.now(),'step 9')
write_parallel(fnameout,data)
exit()

fname = '/data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped/'
fnameout = '/data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped_ward/'
nfiles = len(next(os.walk('/data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped/'))[2])


id_tmp = nfiles//2
data = tifffile.imread(f'{fname}/recon_{id_tmp:05}.tiff')
mmin,mmax=find_min_max(data)
print(mmin,mmax)

os.system('rm -rf /data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped_ward/*')
data = read_parallel(fname,0,data.shape[1],0,data.shape[0],0,nfiles)
print(data.shape)
# mmin,mmax=find_min_max(data[data.shape[0]//2])
mmin = -0.043274883
mmax = 0.06554978
data = data.swapaxes(0,1)
data = ward_parallel(data,23,mmin,mmax)

data = data.swapaxes(0,1)
data = data.swapaxes(0,2).swapaxes(1,2)
data = ward_parallel(data,-40,mmin,mmax,conv=False)
data = rotate_parallel(data,1)
data = data.swapaxes(1,2).swapaxes(0,2)
data=data[::-1]
write_parallel(fnameout,data)
exit()
# # fname = '/data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped_ward/recon/r_00000.tiff'
# # fnameout = '/data/2022-11-Nikitin/alcf/slab3_new/mosaic_rec_cropped_ward2/recon'

# # data = dxchange.read_tiff_stack(fname,ind=range(0,500))[:]
# data = data.swapaxes(0,1)
# data = rotate_parallel(data,-1)
# data = data.swapaxes(0,1)
# # data = data[:,::-1]
# data = data[218:252,462:462+1012,196:196+1518]
# data=data[::-1]
# [x,y] = np.meshgrid(np.arange(-data.shape[2]//2,data.shape[2]//2),np.arange(-data.shape[1]//2,data.shape[1]//2))
# circ = x**2+(1.2*y)**2<(data.shape[2]/2)**2
# data*=circ
# dxchange.write_tiff_stack(data,f'{fnameout}/r',overwrite=True)

