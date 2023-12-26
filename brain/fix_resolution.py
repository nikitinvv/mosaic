import h5py
import sys

with h5py.File(sys.argv[1],'a') as fid:
    print(sys.argv[1])
    fid['/measurement/instrument/detection_system/objective/resolution'][0]=0.92
    print(fid['/measurement/instrument/detection_system/objective/resolution'][0])
    