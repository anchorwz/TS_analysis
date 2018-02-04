import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt
from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim, show
from matplotlib.lines import Line2D
from sklearn.preprocessing import normalize

from saxpy import SAX
import Time_series
import Fitting
import WindowSliding


def read_para(argv):
    ''' python test.py -n n -w w -a a'''
    myopts, args = getopt.getopt(sys.argv[1:],"n:w:a:")
    
    for opt, arg in myopts:
        if opt in ('-n'):
            n=arg
        elif opt in ('-w'):
            w=arg
        elif opt in ('-a'):
            a=arg
        else:
            print("Usage: python test.py -n n -w w -a a")

    return (int(n), int(w), int(a))

def DrawPlot(data, plot_title):
    plot(range(len(data)), data, alpha=0.8, color='red')
    title(plot_title)
    xlabel('Time')
    ylabel('Signal')
    xlim((0, len(data)-1))

def DrawLines(lines):
    ax = gca()
    for line in lines:
        tline = Line2D((line[0], line[2]), (line[1], line[3]))
        ax.add_line(tline)


n, w, a = read_para(sys.argv[1:])

#1 represent SAX and calculate the frequence

x = Time_series.Time_series_CAR(n)
data = x.tolist()
sax = SAX(w, a, 1e-6)
(letters, indices) = sax.to_letter_rep(data)
frq = sax.symbol_frequency(data)

#2 Dimensionality reduction with linear interprolation

a = np.asarray(data,dtype=np.float64)
newdata =  (a + np.random.normal(0,3,n)).tolist()
nordata = normalize(a[:,np.newaxis], axis=0).ravel()

figure()
lines = WindowSliding.WindowSliding(nordata, Fitting.Fitting, Fitting.SumofSquaredError)
DrawPlot(nordata, 'Pecewise linear approximation with Sliding Window')
DrawLines(lines)
show()
