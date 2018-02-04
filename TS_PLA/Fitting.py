from LeastSquareFit import LeastSquareFit

def SumofSquaredError(data, lines):
    ''' Return the sum of squared error for a least squares line fit of one line of data'''
    x0, y0, x1, y1, = lines
    para, error = LeastSquareFit(data, (x0, x1))
    return error

def Fitting(data, data_range):
    ''' Return a line fit to section of the data: (x0, y0) to (x1, y1) '''
    para, error = LeastSquareFit(data, data_range)
    y0 = para[0]*data_range[0] + para[1]
    y1 = para[0]*data_range[1] + para[1]
    return (data_range[0], y0, data_range[1], y1)
