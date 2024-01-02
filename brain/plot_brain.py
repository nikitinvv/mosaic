import dxchange
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

fnames = ['recon_slice0676_center19.50.tiff','recon_slice0676_center1624.50.tiff','recon_slice0676_center19.90.tiff']
for k in range(3):
    rec = dxchange.read_tiff(f'/data/2022-11-Nikitin/slab4_rec/try_center/brain_slab4_122_subtheta/{fnames[k]}')[:].copy()
    mmin = -5.5e-4
    mmax = 5.5e-4
    rec[0,0]= mmin
    rec[0,1]= mmax
    recp = rec[rec.shape[0]//2-250:rec.shape[0]//2+250,rec.shape[1]//2-250:rec.shape[1]//2+250]
    recp[0,0]= mmin
    recp[0,1]= mmax
    recpp = rec[rec.shape[0]//2-250:rec.shape[0]//2+250,rec.shape[1]-600:rec.shape[1]-100]
    recpp[0,0]= mmin
    recpp[0,1]= mmax

    fig = plt.figure(constrained_layout=True, figsize=(10.7, 2.8))
    grid = fig.add_gridspec(1, 3, height_ratios=[1])

    ax0 = fig.add_subplot(grid[0])
    im = ax0.imshow(rec, cmap='gray',vmin=mmin, vmax=mmax)
    # scalebar = ScaleBar(1.38, "um", length_fraction=0.25)
    # ax0.add_artist(scalebar)
    divider = make_axes_locatable(ax0)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax0.set_xticks([])
    ax0.set_yticks([])
    cb = plt.colorbar(im, cax=cax,format='%.0e')
    cb.remove()
    # plt.colorbar(im, cax=cax,format='%.0e')
    plt.savefig(f'rec{fnames[k]}.png',dpi=300,bbox_inches='tight')

    fig = plt.figure(constrained_layout=True, figsize=(10.7, 2.8))
    grid = fig.add_gridspec(1, 3, height_ratios=[1])

    ax0 = fig.add_subplot(grid[0])
    im = ax0.imshow(recp, cmap='gray',vmin=mmin, vmax=mmax)
    # scalebar = ScaleBar(1.38, "um", length_fraction=0.25)
    # ax0.add_artist(scalebar)
    divider = make_axes_locatable(ax0)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax0.set_xticks([])
    ax0.set_yticks([])
    cb = plt.colorbar(im, cax=cax,format='%.0e')
    cb.remove()
    plt.savefig(f'recp{fnames[k]}.png',dpi=300,bbox_inches='tight')


    fig = plt.figure(constrained_layout=True, figsize=(10.7, 2.8))
    grid = fig.add_gridspec(1, 3, height_ratios=[1])

    ax0 = fig.add_subplot(grid[0])
    im = ax0.imshow(recpp, cmap='gray',vmin=mmin, vmax=mmax)
    # scalebar = ScaleBar(1.38, "um", length_fraction=0.25)
    # ax0.add_artist(scalebar)
    divider = make_axes_locatable(ax0)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax0.set_xticks([])
    ax0.set_yticks([])
    cb = plt.colorbar(im, cax=cax,format='%.0e')
    cb.remove()
    plt.savefig(f'recpp{fnames[k]}.png',dpi=300,bbox_inches='tight')
