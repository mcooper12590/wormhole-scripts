from numpy import arange
import glob
import imageio
from skimage import io

sname = "PZ104"
parentdir = "/media/maxc/Verbatim_2/29-30-07/"
recondir = parentdir + "Reconstructions/"
sdir = parentdir + "Cropped/"
numsuffix = "_Chamber-169um"
totimgs = len(glob.glob(recondir + "*" + numsuffix)) # total number of time slices

# Bounding box of image to crop to
sidedim = 950 # number of pixels high/wide
startx = 490;starty = 390
endx = startx+sidedim
endy = starty+sidedim

for i in arange(totimgs) + 1: # iterate over non-reference time slices
    wnum = str(i).zfill(2) # working time slice name
    tiflist = sorted(glob.glob(recondir + wnum + numsuffix + "/SliceViews/*.tif"))
    wimg = io.concatenate_images(io.ImageCollection(tiflist)) # working image
    print("Loaded working image: " + wnum)
    # Subtract over cropped window, if overflow uint16 -> pixel = 0 (ImageJ subtract behaviour)
    res = wimg[:,startx:endx,starty:endy]
    ofile = sdir + sname + "_" + wnum + ".tif"
    imageio.mimwrite(ofile, res)
    print("Wrote image")
