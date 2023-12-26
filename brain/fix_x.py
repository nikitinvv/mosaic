import h5py
import sys

with h5py.File(sys.argv[1],'a') as fid:
    print(sys.argv[1])
    fid['/measurement/instrument/sample_motor_stack/setup/x'][0]=-5.4
    # print(fid['/measurement/instrument/detection_system/objective/resolution'][0])
    