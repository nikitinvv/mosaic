import numpy as np
import tifffile
from scipy.ndimage import rotate
from threading import Thread
from wand.image import Image

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

def read0(data,fname,stx, endx, sty, endy, stz, endz, st, end):
    
    for k in range(st,end):
        data[k-stz] = tifffile.imread(f'{fname}/recon_{k:05}.tiff')[sty:endy,stx:endx]    
    
def read_parallel(fname,stx,endx,sty,endy,stz,endz,nthreads=32):
    print('read_parallel')
    data = np.empty([endz-stz,endy-sty,endx-stx],dtype='float32')
    lchunk = int(np.ceil((endz-stz)/nthreads))
    procs = []
    for k in range(nthreads):
        st = stz+k*lchunk
        end = min(stz+(k+1)*lchunk,endz)        
        if st>=end:
            continue
        read_thread = Thread(
            target=read0, args=(data,fname, stx, endx, sty, endy, stz, endz, st, end))
        procs.append(read_thread)
        read_thread.start()
    for proc in procs:
        proc.join()
    return data

def write0(fnameout,data,st, end):
    
    for k in range(st,end):
        tifffile.imwrite(f'{fnameout}/recon_{k:05}.tiff',data[k])#[sty:endy,stx:endx]    
    #dxchange.write_tiff_stack(data[st:end],fnameout,start=st,overwrite=True)
    
def write_parallel(fnameout,data,nthreads=32):
    print('write_parallel')
    lchunk = int(np.ceil(data.shape[0]/nthreads))
    procs = []
    for k in range(nthreads):
        st = k*lchunk
        end = min((k+1)*lchunk,data.shape[0])        
        if st>=end:
            continue
        read_thread = Thread(
            target=write0, args=(fnameout,data, st, end))
        procs.append(read_thread)
        read_thread.start()
    for proc in procs:
        proc.join()
    return data

def rotate0(data,st,end,ang):
    
    for k in range(st,end):
        data[k]=rotate(data[k],ang,order=3,reshape=False)

def rotate_parallel(data,ang,nthreads=32):
    print('rotate_parallel')
    lchunk = int(np.ceil(data.shape[0]/nthreads))
    procs = []
    for k in range(nthreads):
        st = k*lchunk
        end = min((k+1)*lchunk,data.shape[0])        
        if st>=end:
            continue
        read_thread = Thread(
            target=rotate0, args=(data, st, end, ang))
        procs.append(read_thread)
        read_thread.start()
    for proc in procs:
        proc.join()
    return data

def ward0(data,res,st,end,ang, mmin, mmax,conv):
    for k in range(st,end):
        # print(conv)        
        if conv:
            data0 = touint8(data[k],mmin,mmax)
        else:
            data0 = data[k].astype('uint8')
        data0=Image.from_array(data0)
        
        data0.distort('arc', (ang,))
        res[k] = np.uint8(data0)[:,:,0]
        
        
def ward_parallel(data,ang,mmin,mmax,conv=True,nthreads=32):
    print('ward_parallel')
    if ang<0:
        data = data[:,::-1]
        ang=-ang    
    data0 = data[data.shape[0]//2]    
    data0=Image.from_array(data0)
    data0.distort('arc', (ang,))
    shape = np.float32(data0).shape[:2]
    res = np.zeros([data.shape[0],*shape],dtype='uint8')
    lchunk = int(np.ceil(data.shape[0]/nthreads))
    procs = []
    for k in range(nthreads):
        st = k*lchunk
        end = min((k+1)*lchunk,data.shape[0])     
        if st>=end:
            continue   
        read_thread = Thread(
            target=ward0, args=(data,res, st, end, ang,mmin,mmax,conv))
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