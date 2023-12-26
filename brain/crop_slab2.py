
import numpy as np
import os
import tifffile
import dxchange
from scipy.ndimage import rotate
from threading import Thread


def find_min_max(data):
    """Find min and max values according to histogram"""

    h, e = np.histogram(data[:], 1000)
    stend = np.where(h > np.max(h)*0.005)
    st = stend[0][0]
    end = stend[0][-1]
    mmin = e[st]
    mmax = e[end+1]
    
    # print(mmin,mmax)
    return mmin, mmax

def rotate0(data,st,end,ang):
    print(st,end)
    data[st:end]=rotate(data[st:end],ang,order=3,axes=(2,1),reshape=False)

def rotate_parallel(data,ang,nthreads=16):
    lchunk = int(np.ceil(data.shape[0]/nthreads))
    procs = []
    for k in range(nthreads):
        st = k*lchunk
        end = min((k+1)*lchunk,data.shape[0])        
        read_thread = Thread(
            target=rotate0, args=(data, st, end, ang))
        procs.append(read_thread)
        read_thread.start()
    for proc in procs:
        proc.join()
    return data

def ward0(data,res,st,end,ang, mmin, mmax):
    for k in range(st,end):
        data0 = touint8(data[k],mmin,mmax)
        # data0 = data0[::-1]
        
        data0=Image.from_array(data0)
        
        data0.distort('arc', (ang,))
        res[k] = np.float32(data0)[:,:,0]
        
def ward_parallel(data,shape,ang,mmin,mmax,nthreads=16):
    res = np.zeros([data.shape[0],*shape],dtype='float32')
    lchunk = int(np.ceil(data.shape[0]/nthreads))
    procs = []
    for k in range(nthreads):
        st = k*lchunk
        end = min((k+1)*lchunk,data.shape[0])        
        read_thread = Thread(
            target=ward0, args=(data,res, st, end, ang,mmin,mmax))
        procs.append(read_thread)
        read_thread.start()
    for proc in procs:
        proc.join()
    return res
def touint8(psi, mmin, mmax):
    """Find optical flow for one projection by using opencv library on CPU"""
    psi[:] = ((psi-mmin) /
            (mmax-mmin)*255)
    psi[psi > 255] = 255
    psi[psi < 0] = 0
    psi = psi.astype('uint8')
    return psi
fname = '/data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin/recon_00000.tiff'
fnameout = '/data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin_cropped/recon'

data = dxchange.read_tiff_stack(fname,ind=range(200,540))[:]
data[:] = -data

data = rotate_parallel(data,-2.6)
os.system('rm -rf /data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin_cropped/*')
data = data.swapaxes(0,1)
data = rotate_parallel(data,-0.5+0.9)
data = data.swapaxes(0,1)
data = data.swapaxes(0,2)
data = rotate_parallel(data,5.7-11.3)
data = data.swapaxes(0,2)
dxchange.write_tiff_stack(data,fnameout,overwrite=True)


from wand.image import Image

fname = '/data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin_cropped/recon_00000.tiff'
fnameout = '/data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin_cropped_ward/recon'

data = dxchange.read_tiff_stack(fname,ind=range(0,340))[:]

data = data.swapaxes(0,1)
os.system('rm -rf /data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin_cropped_ward/*')
# mmin,mmax=find_min_max(data[data.shape[0]//2])
mmin = -0.0029269056 
mmax = 0.0068289298
data0 = touint8(data[0],mmin,mmax)

# data0 = data0[::-1]
data0=Image.from_array(data0)

data0.distort('arc', (10,))
shape = np.float32(data0).shape[:2]
print(shape)
    
data = ward_parallel(data,shape,10,mmin,mmax)

data = data.swapaxes(0,1)
data = data[132:191,472:472+1022,172:172+1546]

data = data[:,::-1,::-1]
[x,y] = np.meshgrid(np.arange(-data.shape[2]//2,data.shape[2]//2),np.arange(-data.shape[1]//2,data.shape[1]//2))
circ = x**2+(1.2*y)**2<(data.shape[2]/2)**2
dxchange.write_tiff_stack(data*circ,f'{fnameout}/r',overwrite=True)

