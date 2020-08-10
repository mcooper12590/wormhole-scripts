from skimage import io
from numpy import arange, sum
import glob

# Directory information where time slices live
parentdir = "/media/maxc/Data/Tomography/Time_Series/PZ103/"
recondir = parentdir + "Reconstructions/"
numsuffix = "_Chamber-169um"
totimgs = len(glob.glob(recondir + "*" + numsuffix)) # total number of time slices

refimgnum = "01" # Reference time slice number
refslicenum = 800 # Reference slice number

refdir = recondir + refimgnum + numsuffix + "/SliceViews/"
refsliceloc = refdir + str(refslicenum-1).zfill(5) + ".tif"
refimg = io.imread(refsliceloc) # Reference slice from ref time slice

pm = 20 # +/- value to check reference against
pmrange = arange(refslicenum-pm-1, refslicenum+pm) # Slice numbers to load from moving img

#movnum = "40" # Moving image time slice number

# Check each time slice for a shift
for i in arange(totimgs-1) + 2: # iterate over non-reference time slices
    movslices = [ \
        recondir + str(i).zfill(2) + numsuffix + "/SliceViews/" + \
        str(j).zfill(5) + ".tif" for j in pmrange] # List of slices to load
    movimg = io.concatenate_images(io.ImageCollection(movslices)) # Load slices from moving image
    # Find best fit slice by sum of square differences vs ref slice
    movslice = sum( \
           sum((movimg-refimg)**2, axis=1), \
           axis=1).argmin()
    movamnt = pm-movslice
    print("Offset for time slice " + str(i) + ": " + str(movamnt))
