import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import plot
import sys, getopt
import csv
import os.path

from saxpy import SAX
import Time_series

def read_para(argv):
    ''' python main.py -n n -w w -a a'''
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

def file_len(fname):
    with open(fname) as f:
        line_count = 0
        for line in f:
            line_count += 1
    return line_count

def WriteDataFiles(data):

    ''' Write TS file in csv format'''

    fname = 'TS.csv'
    if os.path.isfile(fname) and file_len(fname)<=20:
        flen = file_len(fname) + 1
        mode = 'a'
    else:
        flen = 1
        mode = 'w'
    data.insert(0, str(flen))
        
    with open(fname, mode) as myfile:
        wr = csv.writer(myfile)
        wr.writerow(data)

def WriteInfoFile(letters, indices, freq, para):
    fname = 'file.txt'
    if os.path.isfile(fname) and file_len(fname)/5<=20:
        flen = file_len(fname)/5 + 1
        mode = 'a'
    else:
        flen = 1
        mode = 'w' 
    f = open(fname, mode)
    f.write( "----------------------%d---------------------\n" % flen)
    f.write("SAX parameters: %s\n" % str(para))
    f.write ("Symbolic letters: %s\n" % letters) 
    f.write("Indices: %s\n" % str(indices))         
    f.write("freq: %s\n"% str(freq))
    f.close()

n, w, a = read_para(sys.argv[1:])
para = {'n':n, 'w':w, 'a':a}
# represent SAX and calculate the frequence

x = Time_series.Time_series_CAR(n)
newx = x.tolist()
sax = SAX(w, a, 1e-6)
(letters, indices) = sax.to_letter_rep(newx)
frq = sax.symbol_frequency(newx)

# Write Data and information to files

WriteDataFiles(newx)
WriteInfoFile(letters, indices, frq, para)

