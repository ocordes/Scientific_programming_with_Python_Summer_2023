import numpy as np
from astropy.io import fits


class AstroIO(object):
    def read_file(self, filename):
        """
        read_file reads a FITS file and returns the numpy data array
        """
        hdulist = fits.open(filename)
        data   = hdulist[0].data
        return data
    
    def write_file(self, data, filename):
        """
        write_file writes a numpy data array into a FITS-file
        """
        hdu = fits.PrimaryHDU(data)
        hdu.writeto(filename, overwrite=True)      


# start with your solution here