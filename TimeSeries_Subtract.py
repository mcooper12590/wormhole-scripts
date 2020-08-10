from numpy import arange
import glob
import imageio
from skimage import io

sname = "PZ103" #sample name
# Directory information
parentdir = "/media/maxc/Data/Tomography/Time_Series/PZ103/"
recondir = parentdir + "Reconstructions/"
sdir = parentdir + "Subtractions/"
numsuffix = "_Chamber-169um"
totimgs = len(glob.glob(recondir + "*" + numsuffix)) # total number of time slices

refnum = "01" # number of reference time slice
tiflist = sorted(glob.glob(recondir + refnum + numsuffix + "/SliceViews/*.tif"))
refimg = io.concatenate_images(io.ImageCollection(tiflist)) # load reference image
print("Loaded reference image: "+ refnum)
# Bounding box of image to crop to
sidedim = 250 # number of pixels high/wide
startx = 350;starty = 340
endx = startx+sidedim+1
endy = starty+sidedim+1

# Subtract time slices from reference time slice
for i in arange(totimgs-1) + 2: # iterate over non-reference time slices
    wnum = str(i).zfill(2) # working time slice name
    tiflist = sorted(glob.glob(recondir + wnum + numsuffix + "/SliceViews/*.tif"))
    wimg = io.concatenate_images(io.ImageCollection(tiflist)) # working image
    print("Loaded working image: " + wnum)
    # Subtract over cropped window, if overflow uint16 -> pixel = 0 (ImageJ subtract behaviour)
    res = refimg[:,startx:endx,starty:endy] - wimg[:,startx:endx,starty:endy]
    res[refimg[:,startx:endx,starty:endy] < wimg[:,startx:endx,starty:endy]] = 0
    ofile = sdir + sname + "_" + refnum + "-" + wnum + ".tif"
    imageio.mimwrite(ofile, res)
    print("Wrote image")
