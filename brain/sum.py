import dxchange
import numpy as np
from os import walk
import time
from threading import Thread
#bin2
# lamino_start = 700
# lamino_end = 1260

slab=4
chunk_size = 1024
nproj = 14976

class WRThread():
    def __init__(self):
        self.thread = None

    def run(self, fun, args):
        self.thread = Thread(target=fun, args=args)
        self.thread.start()

    def is_alive(self):
        if self.thread == None:
            return False
        return self.thread.is_alive()

    def join(self):
        if self.thread == None:
            return
        self.thread.join()


def find_free_thread(threads):
    ithread = 0
    while True:
        if not threads[ithread].is_alive():
            break
        ithread = ithread+1
        # ithread=(ithread+1)%len(threads)
        if ithread == len(threads):
            ithread = 0
            time.sleep(0.01)
    return ithread

def sum(l):
    print(l)
    data = dxchange.read_tiff(f'/data/2022-11-Nikitin/slab{slab}/mosaic_part0/try_center/{l}').copy()
    for id_chunk in range(nchunk):  
        print(id_chunk)      
        st = id_chunk*chunk_size
        end = st + lchunk[id_chunk]
        # print(st,end)
        data += dxchange.read_tiff(f'//data/2022-11-Nikitin/slab{slab}/mosaic_part{id_chunk}/try_center/{l}')
    dxchange.write_tiff(data,f'/data/2022-11-Nikitin/slab{slab}/mosaic_rec/try_center/{l}',overwrite=True)


nchunk = int(np.ceil(nproj/chunk_size))
lchunk = np.minimum(
            chunk_size, np.int32(nproj-np.arange(nchunk)*chunk_size))  # chunk sizes

s=''
filenames = next(walk(f'/data/2022-11-Nikitin/slab{slab}/mosaic_part0/try_center'), (None, None, []))[2][1:]  # [] if no file skip rec_line
# print(f'/data/2022-11-Nikitin/slab{slab}/mosaic_part0',filenames)
# for l in filenames:
#     print(f'{l=}')
#     data = dxchange.read_tiff(f'/data/2022-11-Nikitin/slab{slab}/mosaic_part0/{l}').copy()
#     for id_chunk in range(nchunk):  
#         print(id_chunk)      
#         st = id_chunk*chunk_size
#         end = st + lchunk[id_chunk]
#         # print(st,end)
#         data += dxchange.read_tiff(f'//data/2022-11-Nikitin/slab{slab}/mosaic_part{id_chunk}/{l}')
#     dxchange.write_tiff(data,f'/data/2022-11-Nikitin/slab{slab}/mosaic_rec/result/{l}',overwrite=True)

threads = []
for k in range(32):
    threads.append(WRThread())
            
for l in filenames:
    ithread = find_free_thread(threads)
    threads[ithread].run(sum, (l,))