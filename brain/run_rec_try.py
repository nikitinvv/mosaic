
import numpy as np
import os
import sys
import subprocess
fname = f'/data/2022-11-Nikitin/slab{sys.argv[1]}/mosaic/mosaic.h5'
out_path_name0=f'/data/2022-11-Nikitin/slab{sys.argv[1]}/mosaic_part'
nchunk = 1024

#3 done
# nsino = ((2608+4368)//2)/5936
# center = 7494
#2 running
# nsino = ((1808+3568)//2)/5936
# center = 7500
#4
nsino = ((1856+3408)//2)/5936
center = 7499
#1
# nsino = ((1728+3248)//2)/5936
# center = 7499.5

for k in range(0,int(np.ceil(14976/nchunk)),4):
    out_path_name = out_path_name0+f'{k}/try_center'
    st = k*nchunk
    end = min(st+nchunk,14976)
    cmd1 = f"ssh -t tomo@tomo1 \"bash -c 'source ~/.bashrc; conda activate tomocupy; CUDA_VISIBLE_DEVICES=0 tomocupy recon_steps \
        --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 \
        --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --nsino {nsino}  \
        --out-path-name {out_path_name} \'\""
    print(cmd1)
    p1 = subprocess.Popen(cmd1, shell=True)
    #exit()
    
    out_path_name = out_path_name0+f'{k+1}/try_center'
    st = (k+1)*nchunk
    end = min(st+nchunk,14976)
    cmd2 = f"ssh -t tomo@tomo1 \"bash -c 'source ~/.bashrc; conda activate tomocupy; CUDA_VISIBLE_DEVICES=1 tomocupy recon_steps \
         --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 \
        --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --nsino {nsino}  \
        --out-path-name {out_path_name} \'\""
    print(cmd2)
    p2 = subprocess.Popen(cmd2, shell=True)
    
    out_path_name = out_path_name0+f'{k+2}/try_center'
    st = (k+2)*nchunk
    end = min(st+nchunk,14976)
    cmd3 = f"ssh -t tomo@tomo2 \"bash -c 'source ~/.bashrc; conda activate tomocupy; CUDA_VISIBLE_DEVICES=0 tomocupy recon_steps \
         --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 \
        --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --nsino {nsino}  \
        --out-path-name {out_path_name} \'\""
    print(cmd3)
    p3 = subprocess.Popen(cmd3, shell=True)
    
    out_path_name = out_path_name0+f'{k+3}/try_center'
    st = (k+3)*nchunk
    end = min(st+nchunk,14976)
    cmd4 = f"ssh -t tomo@tomo2 \"bash -c 'source ~/.bashrc; conda activate tomocupy; CUDA_VISIBLE_DEVICES=1 tomocupy recon_steps \
         --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 \
        --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --nsino {nsino}  \
        --out-path-name {out_path_name} \'\""
    print(cmd4)
    p4 = subprocess.Popen(cmd4, shell=True)
    
    out_path_name = out_path_name0+f'{k+4}/try_center'
    st = (k+4)*nchunk
    end = min(st+nchunk,14976)
    cmd5 = f"ssh -t tomo@tomo3 \"bash -c 'source ~/.bashrc; conda activate tomocupy; CUDA_VISIBLE_DEVICES=0 tomocupy recon_steps \
         --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 \
        --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --nsino {nsino}  \
        --out-path-name {out_path_name} \'\""
    print(cmd5)
    p5 = subprocess.Popen(cmd5, shell=True)
    
    # st = (k+5)*nchunk
    # end = min(st+nchunk,14976)
    # print(cmd6)
    # cmd6 = f"ssh -t tomo@tomo3 \"bash -c 'source ~/.bashrc; conda activate tomocupy; CUDA_VISIBLE_DEVICES=1 tomocupy recon_steps --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --out-path-name {out_path_name} \'\""
    # p6 = subprocess.Popen(cmd6, shell=True)


    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()
    p5.wait()
    # p6.wait()

# cmd2 = f"ssh -t tomo@tomo2 \"bash -c 'source ~/.bashrc; conda activate tomocupy; tomocupy recon {line} --start-row {args.end_row//2} --end-row {args.end_row}\'\""
# print(f'Tomo1: {cmd1}')
# print(f'Tomo2: {cmd2}')
#     p1 = subprocess.Popen(cmd1, shell=True)
#     time.sleep(1)
#     p2 = subprocess.Popen(cmd2, shell=True)
#     p1.wait()
#     p2.wait()

# kk = range(0,int(np.ceil(14976/nchunk)),2)
# k = kk[int(sys.argv[1])]
# st = k*nchunk
# end = min(st+nchunk,14976)
# st1 = (k+1)*nchunk
# end1 = min(st1+nchunk,14976)
# cmd = f'CUDA_VISIBLE_DEVICES=0 tomocupy recon_steps --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --out-path-name {out_path_name}{k}/try_center &
# '
# os.system(cmd)

# cmd = f'CUDA_VISIBLE_DEVICES=1 tomocupy recon_steps --rotation-axis {center} --center-search-width 2 --nsino-per-chunk 2 --nproj-per-chunk 2 --lamino-angle 19.95 --start-proj {st} --end-proj {end} --file-name {fname} --out-path-name {out_path_name}{k}/try_center'
# os.system(cmd)