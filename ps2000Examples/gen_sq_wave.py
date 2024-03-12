import ctypes
import numpy as np

def gen_square(t, duty, low_thres):
    t, w = np.asarray(t), np.asarray(duty)
    w = np.asarray(w + (t - t))
    t = np.asarray(t + (w - w))
    if t.dtype.char in ['fFdD']:
        ytype = t.dtype.char
    else:
        ytype = 'd'

    y = np.zeros(t.shape, ytype)
    # width must be between 0 and 1 inclusive
    mask1 = (w > 1) | (w < 0)
    np.place(y, mask1, np.nan)
    # on the interval 0 to duty*2*pi the function is 1
    tmod = np.mod(t, 2 * np.pi)
    
    mask2 = (32767-mask1)&(tmod<w*2*np.pi)
    np.place(y, mask2, 32767)
	
	#mask2 = (32767 - mask1) & (tmod < w * 2 * np.pi)
    #np.place(y, mask2, 32767)	
	
    # on the interval duty*2*pi to 2*pi function is  (pi*(w+1)-tmod) / (pi*(1-w))
    mask3 = (1 - mask1) & (1 - mask2)
    np.place(y, mask3, low_thres)
    return y