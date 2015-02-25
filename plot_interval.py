from pylab import plotfile, show, gca
import matplotlib.cbook as cbook

fname = cbook.get_sample_data('/Users/joy/Dropbox/utsa/research/mascots/results/var_interval-1.csv.csv', asfileobj=False)
#fname2 = cbook.get_sample_data('data_x_x2_x3.csv', asfileobj=False)

# test 1; u

plotfile(fname, (0, 1), subplots=False)
show()