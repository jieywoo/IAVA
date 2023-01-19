from math import factorial
import numpy as np

def savitzky_golay(y, window_size=5, order=2, deriv=0, rate=1):
  try:
    window_size = np.abs(np.int(window_size))
    order = np.abs(np.int(order))
  except ValueError:
    raise ValueError("window_size and order have to be of type int")
  if window_size % 2 != 1 or window_size < 1:
    raise TypeError("window_size size must be a positive odd number")
  if window_size < order + 2:
    raise TypeError("window_size is too small for the polynomials order")
  order_range = range(order+1)
  half_window = (window_size -1) // 2
  # precompute coefficients
  b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
  m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
  # pad the signal at the extremes with values taken from the signal itself
  firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
  lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
  y = np.concatenate((firstvals, y, lastvals))
  return np.convolve( m[::-1], y, mode='valid')

def leastSquareFilter(x, list_window_size, list_filter_idx_size):
  # Manually identified size for each feature
  # window_size = [10,10,10,3,3,3,3,3,3,3,10,10]
  # filter_idx_size = [15,15,15,5,5,5,5,5,5,5,15,15]
  return [np.round(np.mean(savitzky_golay(x[:,f])[-list_filter_idx_size[f]:]),list_window_size[f]) for f in range(x.shape[1])]

