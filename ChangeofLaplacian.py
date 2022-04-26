
import numpy as np
from matplotlib import pyplot as plt
import math
import imageio as io
import DiscreteLaplacian as DL

def getChangeofLaplacian(imagePath):

    image = np.array(io.imread(imagePath), dtype=np.longdouble)

    I_pad = np.pad(image, [(0, 0), (1, 1), (0, 0)], mode='symmetric')  # array padding
    IL = DL.del2((I_pad).astype(np.float64))  # second derivative
    FY = np.gradient((I_pad).astype(np.float64), axis=1)
    FX = np.gradient((I_pad).astype(np.float64), axis=0)
    # dx = np.absolute(FY)/np.sqrt(np.square(FX)+np.square(FY))

    ## np errstate to remove runtime warning
    with np.errstate(divide='ignore', invalid='ignore'):
        dx = np.true_divide(np.absolute(FY), np.sqrt(np.square(FX) + np.square(FY)))
        # dx=np.nan_to_num(fdx,nan=0)

        dy = np.true_divide(np.absolute(FX), np.sqrt(np.square(FX) + np.square(FY)))
        # dy=np.nan_to_num(fdy,nan=0)

    d_IL = np.ones(np.shape(IL))
    for i in range(1, np.size(IL, axis=0) - 1):
        for j in range(1, np.size(IL, axis=1) - 1):
            for channel in range(0, np.size(d_IL, axis=2)):
                a = IL[i - 1, j - 1, channel - 1]
                b = IL[(i + np.sign(FX[i - 1, j - 1, channel - 1])).astype(np.int32) - 1, j - 1, channel - 1]
                c = IL[(i + np.sign(FX[i - 1, j - 1, channel - 1])).astype(np.int32) - 1, (
                            j - np.sign(FY[i - 1, j - 1, channel - 1])).astype(np.int32) - 1, channel - 1]
                d = IL[i - 1, (j - np.sign(FY[i - 1, j - 1, channel - 1])).astype(np.int32) - 1, channel - 1]
                d_IL[i - 1, j - 1, channel - 1] = (1 - dx[i - 1, j - 1, channel - 1]) * (
                            1 - dy[i - 1, j - 1, channel - 1]) * a + (1 - dx[i - 1, j - 1, channel - 1]) * dy[
                                                      i - 1, j - 1, channel - 1] * b + dx[i - 1, j - 1, channel - 1] * (
                                                              1 - dy[i - 1, j - 1, channel - 1]) * d + dx[
                                                      i - 1, j - 1, channel - 1] * dy[i - 1, j - 1, channel - 1] * c - a

    # outside for loop
    d_IL = d_IL[:, 1:-1, :]
    d_IL = np.nan_to_num(d_IL, nan=0)

    return d_IL