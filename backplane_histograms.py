import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def plot_prettier(dpi=150, fontsize=17):
	plt.rcParams['figure.dpi'] = dpi
	plt.rc("savefig", dpi=dpi)
	plt.rc('font', size=fontsize)
	plt.rc('xtick', direction='in')
	plt.rc('ytick', direction='in')
	plt.rc('xtick.major', pad=5)
	plt.rc('xtick.minor', pad=5)
	plt.rc('ytick.major', pad=5)
	plt.rc('ytick.minor', pad=5)
	plt.rc('lines', dotted_pattern = [2., 2.])
	# plt.rc('text', usetex=True)

plot_prettier()

def add_minor_ticks(plot, ticks, bot=True, tp=True, lft=True, rght=True):
	plot.tick_params(which = 'minor', bottom=bot, top=tp, left=lft, right=rght)
	plot.tick_params(bottom=True, top=True, left=True, right=True)
	if (bot or tp):
		plot.xaxis.set_minor_locator((AutoMinorLocator(int(ticks))))
	if (lft or rght):
		plot.yaxis.set_minor_locator((AutoMinorLocator(int(ticks))))

e_per_coulomb = 6.242e18

# full_data = np.loadtxt("combined_backplane.phsp")
full_data = np.loadtxt("full_channel_test.phsp")
full_data = full_data[full_data[:, 6] > 0,:]
print(np.shape(full_data))

times = full_data[:,10]

time_hist, time_bins = np.histogram(times, bins=50)

size = (7,5)
top_of_graph = 0.96
graph_size = 0.72
right_of_graph = 0.97


fig_times, time_plot = plt.subplots(figsize=size)
plt.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)

time_plot.plot(time_bins[:-1], ((time_hist / e_per_coulomb)/ ((time_bins[1]-time_bins[0]) * 1e-9)))
time_plot.set_xlabel("time (ns)")
time_plot.set_ylabel("Amps")
add_minor_ticks(time_plot, 5)
# time_plot.set_ylim(bottom=0)
time_plot.set_yscale('log')


plt.show()
