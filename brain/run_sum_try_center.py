
import numpy as np
import os
import tifffile
nchunk = 512
files = os.listdir('/data/2022-11-Nikitin/slab1/mosaic_part0/try_center')
os.system(f'mkdir /data/2022-11-Nikitin/slab1/mosaic_rec')
os.system(f'mkdir /data/2022-11-Nikitin/slab1/mosaic_rec/try_center')

for j in range(len(files)):    
    files[j]='/data/2022-11-Nikitin/slab1/mosaic_part0/try_center/'+files[j]
    d = tifffile.imread(files[j])
    for k in range(1,int(np.ceil(14976/nchunk))):
        ff = files[j].replace('part0',f'part{k}',1)
        print(ff)
        d+=tifffile.imread(files[j].replace('part0',f'part{k}',1))
    tifffile.imwrite(files[j].replace('_part0',f'_rec',1),d)
        # cmd = f'tomocupy recon_steps --binning 2 --center-search-step 4 --nsino-per-chunk 2 --nproj-per-chunk 2 --lamino-angle 20 --start-proj {st} --end-proj {end} --file-name /data/2022-11-Nikitin/slab1/mosaic/mosaic.h5 --out-path-name /data/2022-11-Nikitin/slab1/mosaic_part{k}'
        # os.system(cmd)