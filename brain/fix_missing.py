import h5py
import sys

with h5py.File(sys.argv[1],'r') as fid:
    print(sys.argv[1])
    unique_ids = fid['/defaults/NDArrayUniqueId']
    print(unique_ids[:])
    # print(fid['/measurement/instrument/detection_system/objective/resolution'][0])
    
    print(len(unique_ids[:]))