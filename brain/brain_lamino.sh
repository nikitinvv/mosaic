# some fix
# for k in $(ls -d /data/2022-11-Nikitin/bin0/*); do python fix_resolution.py $k; done
# python fix_x.py /data/2022-11-Nikitin/bin0/brain_slab1_061.h5

# stitch
# mosaic stitch --folder-name /data/2022-11-Nikitin/slab1/ 
# python bin.py /data/2022-11-Nikitin/slab1/mosaic/mosaic.h5
# mosaic stitch --folder-name /data/2022-11-Nikitin/slab2/ 
# python bin.py /data/2022-11-Nikitin/slab2/mosaic/mosaic.h5
# mosaic stitch --folder-name /data/2022-11-Nikitin/slab3/ 
# python bin.py /data/2022-11-Nikitin/slab3/mosaic/mosaic.h5
# mosaic stitch --folder-name /data/2022-11-Nikitin/slab4/ 
# python bin.py /data/2022-11-Nikitin/slab4/mosaic/mosaic.h5

# find rotation axis full
# python run_rec_try.py
# python run_sum_try_center.py

# binned recon for dragonfly 
# tomocupy recon_steps --binning 1 --file-name /data/2022-11-Nikitin/slab1/mosaic/mosaic_bin2.h5 --end-proj 3744 --lamino-angle 19.95 --rotation-axis 1874.5 --out-path-name /data/2022-11-Nikitin/slab1/mosaic_rec/mosaic_bin2_rec_bin --reconstruction-type full
# tomocupy recon_steps --binning 1 --file-name /data/2022-11-Nikitin/slab2/mosaic/mosaic_bin2.h5 --end-proj 3744 --lamino-angle 19.95 --rotation-axis 1875 --out-path-name /data/2022-11-Nikitin/slab2/mosaic_rec/mosaic_bin2_rec_bin --reconstruction-type full
# tomocupy recon_steps --binning 1 --file-name /data/2022-11-Nikitin/slab3/mosaic/mosaic_bin2.h5 --end-proj 3744 --lamino-angle 19.95 --rotation-axis 1873.5 --out-path-name /data/2022-11-Nikitin/slab3/mosaic_rec/mosaic_bin2_rec_bin --reconstruction-type full
# tomocupy recon_steps --binning 1 --file-name /data/2022-11-Nikitin/slab4/mosaic/mosaic_bin2.h5 --end-proj 3744 --lamino-angle 19.95 --rotation-axis 1873.5 --out-path-name /data/2022-11-Nikitin/slab4/mosaic_rec/mosaic_bin2_rec_bin --reconstruction-type full

# crop, rotate and bend
# python crop_slab1.py
# python crop_slab2.py
# python crop_slab3.py
# python crop_slab4.py

# full rec (fourierrec recon is shifted by (542-494)*4), numbers are taken from crop_slab..
python run_rec.py 1 7498 2112 3632
python run_rec.py 2 7500 1792 4512
python run_rec.py 3 7494 2992 4752
python run_rec.py 4 7494 2240 3792

