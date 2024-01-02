import h5py
import sys
import numexpr as ne
import numpy as np

def write_meta(in_dataset_name, out_h5):

        # try:  # trying to copy meta
            import meta

            mp = meta.read_meta.Hdf5MetadataReader(in_dataset_name)
            meta_dict = mp.readMetadata()
            mp.close()
            with h5py.File(in_dataset_name,'r') as f:
                print("  *** meta data from raw dataset %s copied to rec hdf file" % in_dataset_name)
                for key, value in meta_dict.items():
                    # print(key, value)
                    if key.find('exchange') != 1:
                        dset = out_h5.create_dataset(key, data=value[0], dtype=f[key].dtype, shape=(1,))
                        if value[1] is not None:
                            s = value[1]
                            utf8_type = h5py.string_dtype('utf-8', len(s)+1)
                            dset.attrs['units'] =  np.array(s.encode("utf-8"), dtype=utf8_type)
                # except:
                #     print('write_meta() error: Skip copying meta')
                #     pass        
        
def downsampling(data,bin):
    for j in range(bin):
            x = data[:, :, ::2]
            y = data[:, :, 1::2]
            data = ne.evaluate('x + y')  # should use multithreading
    for k in range(bin):
        x = data[:, ::2]
        y = data[:, 1::2]
        data = ne.evaluate('x + y')
    return data


        
infile = sys.argv[1]
bin = int(sys.argv[2])

outfile = f'{sys.argv[1][:-3]}_subtheta.h5'
with h5py.File(infile,'r') as f:
    with h5py.File(outfile,'w') as fout:        
        
        data = f['/exchange/data']        
        data_dark = f['/exchange/data_dark']
        data_white = f['/exchange/data_white']
        print(f'{data.shape=}')
        print(f'{data_dark.shape=}')
        print(f'{data_white.shape=}')
        theta = f['/exchange/theta'][::5]
        
        print('init new dataset')
        fout.create_dataset('exchange/data',chunks=(1,data.shape[1]//2**bin,data.shape[2]//2**bin),shape=(data.shape[0]//5,data.shape[1]//2**bin,data.shape[2]//2**bin),dtype='float32')        
        data_dark0 = downsampling(data_dark[:].astype('float32'),bin)             
        data_white0 = downsampling(data_white[:].astype('float32'),bin)                     
        fout.create_dataset('exchange/data_dark',chunks=(1,*data_dark0.shape[1:]),data=data_dark0)
        fout.create_dataset('exchange/data_white',chunks=(1,*data_white0.shape[1:]),data=data_white0)
        fout.create_dataset('exchange/theta',data=theta)
        
        print('set projections')
        print(data.shape)
        # dark = np.mean(data_dark0,axis=0)
        # white = np.mean(data_white0,axis=0)
            
        write_meta(infile, fout)
        for k in range(0,data.shape[0]//5):
            print(k)
            # print(f'{k}/{data.shape[0]//2**bin}')
            data0 = downsampling(data[k*5:k*5+1],bin)             
            # data0 = (data0-dark)/(white-dark)
            # data0[data0 <= 0] = 1
            # data0[:] = -np.log(data0)
            # data0[np.isnan(data0)] = 6.0
            # data0[np.isinf(data0)] = 0
            fout['exchange/data'][k] = data0
        
        
        