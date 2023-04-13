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

# Files may be too large, if so we will read a lot of lines, add them to the hist, then repeat

hist_range = (0,3)
hist_bins = 50

comb_hist = np.zeros((hist_bins))
comb_bins = np.zeros((hist_bins + 1))

rows = 10000000

# for i in range(10000):
	# # load the portion of the file
	# # full_data = np.loadtxt("combined_backplane.phsp")
	# # full_data = np.loadtxt("full_channel_test.phsp")
	# print("Loading rows " + str(i*rows) + " to " + str(i*rows + rows))
	# full_data = np.loadtxt("7.5mm_run.phsp", skiprows=i*rows, max_rows=rows)
	# # print(np.shape(full_data))
	# if (np.shape(full_data)[0] > 0):
	# 	full_data = full_data[full_data[:, 6] > 0,:]

	# 	times = full_data[:,10]

	# 	time_hist, comb_bins = np.histogram(times, bins=50, range=hist_range)
	# 	comb_hist += time_hist
	# else:
	# 	break
	
# run_name = "5mm_9e_run"
run_name = "7.5mm_run"
# run_name = "10mm_run"

full_data = np.loadtxt(run_name + ".phsp")
full_data = full_data[full_data[:, 6] > 0,:]

times = full_data[:,10]

print("first in at " + str(np.amin(times)) + " ns")

comb_hist, comb_bins = np.histogram(times, bins=200, weights=full_data[:,6])


size = (7,5)
top_of_graph = 0.96
graph_size = 0.72
right_of_graph = 0.97


fig_times, time_plot = plt.subplots(figsize=size)
plt.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)

time_plot.plot(comb_bins[:-1], ((comb_hist / e_per_coulomb)/ ((comb_bins[1]-comb_bins[0]) * 1e-9)))
time_plot.set_xlabel("time (ns)")
time_plot.set_ylabel("Amps")
time_plot.set_ylim(bottom=1e-9)
time_plot.set_xlim(left=0.0)
add_minor_ticks(time_plot, 5)
# time_plot.set_yscale('log')

fig_space, space_plot = plt.subplots(figsize=size)
plt.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)

electron_origin = (-0.13438, -0.00879)
y_range = 0.25
z_range = 0.03

space_plot.hist2d(full_data[:,1], full_data[:,2], bins=(300,300), weights=full_data[:,6], range=((electron_origin[0] - y_range, electron_origin[0] + y_range),(electron_origin[1] - z_range, electron_origin[1] + z_range)))
space_plot.set_xlabel("cm from origin")
space_plot.set_ylabel("cm from origin")

space_hist, space_y, space_z = np.histogram2d(full_data[:,1], full_data[:,2], bins=(300,300), weights=full_data[:,6], range=((electron_origin[0] - y_range, electron_origin[0] + y_range),(electron_origin[1] - z_range, electron_origin[1] + z_range)))

cm_to_mil = 393.701

fig_y_slice, y_slice_plot = plt.subplots(figsize=size)
plt.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)
y_slice_plot.bar((space_y[:-1] - electron_origin[0]) * cm_to_mil, space_hist[:,150],width=(space_y[1]-space_y[0]) * cm_to_mil)
y_slice_plot.set_xlabel("mil from origin")
y_slice_plot.set_ylabel("electrons")
add_minor_ticks(y_slice_plot, 5)
y_slice_plot.vlines(50,0,np.amax(space_hist[:,150]),'green', 'dashed')
y_slice_plot.vlines(56,0,np.amax(space_hist[:,150]),'green', 'dashed')
y_slice_plot.vlines(-50,0,np.amax(space_hist[:,150]),'green', 'dashed')
y_slice_plot.vlines(-56,0,np.amax(space_hist[:,150]),'green', 'dashed')


fig_z_slice, z_slice_plot = plt.subplots(figsize=size)
plt.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)
z_slice_plot.bar((space_z[:-1] - electron_origin[1]) * cm_to_mil, space_hist[149,:],width=(space_z[1]-space_z[0]) * cm_to_mil)
z_slice_plot.set_xlabel("mil from origin")
z_slice_plot.set_ylabel("electrons")
add_minor_ticks(z_slice_plot, 5)

z_slice_plot.vlines(0,0,np.amax(space_hist[149,:]),'green', 'dashed')
z_slice_plot.vlines(2,0,np.amax(space_hist[149,:]),'green', 'dashed')
z_slice_plot.vlines(8,0,np.amax(space_hist[149,:]),'green', 'dashed')
z_slice_plot.vlines(-6,0,np.amax(space_hist[149,:]),'green', 'dashed')

z_slice_plot.set_xlim(left=-3, right=8)




fig_times.savefig(run_name + '_current_flow.jpg')
fig_space.savefig(run_name + '_locations_of_crossing.jpg')
fig_y_slice.savefig(run_name + "_y_slice.jpg")
fig_z_slice.savefig(run_name + "_z_slice.jpg")