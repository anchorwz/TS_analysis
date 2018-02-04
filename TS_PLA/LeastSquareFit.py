from numpy import arange, array, ones
from numpy.linalg import lstsq 

def LeastSquareFit(data, data_range):
    '''Return parameters and error of a least square fit'''
    x = arange(data_range[0],data_range[1]+1)
    y = array(data[data_range[0]:data_range[1]+1])
    A = ones( (len(x),2), float)
    A[:,0] = x
    (para, residuals, rank, s) = lstsq(A, y)
    try:
        error = residuals[0]
    except IndexError:
        error = 0.0
    return (para, error)

def LeastSquareFitS(data, data_range, func):
    
    x = arange(data_range[0], data_range[1]+1)
    y = array(data[data_range[0]:data_range[1]+1])
    x0 = array([0.0, 0.0])
    sigma = ones(len(x))
    popt, pcov = optimization.curve_fit(func, x, y, x0, sigma)
    return (popt, pcov)

def func(x, a, b):
    return a*x + b

