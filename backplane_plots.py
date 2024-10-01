import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import scipy.stats as st
import seaborn as sns

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

size = (7,5)
top_of_graph = 0.96
graph_size = 0.72
right_of_graph = 0.97



full_data = np.loadtxt("demo_backplane.phsp")
full_data = full_data[full_data[:, 6] > 0,:]
print(np.shape(full_data))

all_points = np.zeros((np.shape(full_data)[0], 3))
all_points[:,0] = full_data[:,1]
all_points[:,1] = full_data[:,2]
all_points[:,2] = full_data[:,6] # the third set of info is the culling weights

times = full_data[:, 10]

fig_time = plt.figure()
time_plt = fig_time.add_subplot()
fig_time.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)

t_hist, t_bins = np.histogram(times, bins=50, weights=all_points[:,2])

time_plt.bar(t_bins[:-1], (t_hist / ((t_bins[1:] - t_bins[:-1]) * e_per_coulomb)) * 1000 * 1e9, width=t_bins[1:] - t_bins[:-1])

time_plt.set_xlabel("time (ns)")
time_plt.set_ylabel("current (mA)")


x = all_points[:, 0]
y = all_points[:, 1]
xmin, xmax = -np.amax(-x), np.amax(x)
ymin, ymax = -np.amax(-y), np.amax(y)

# Peform the kernel density estimate
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])
values = np.vstack([x, y])
kernel = st.gaussian_kde(values, weights=all_points[:,2])
f = np.reshape(kernel(positions).T, xx.shape)

fig = plt.figure()
fig.subplots_adjust(bottom=top_of_graph-graph_size,top=top_of_graph,left=right_of_graph-graph_size,right=right_of_graph)
ax = fig.gca()

# Contourf plot
cfset = ax.contourf(xx, yy, f, cmap='viridis')
## Or kernel density estimate plot instead of the contourf plot
#ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
# Contour plot
cset = ax.contour(xx, yy, f, colors='k')
# Label plot
ax.clabel(cset, inline=1, fontsize=10)
ax.set_xlabel('cm')
ax.set_ylabel('cm')

plt.show()



# fig_pos = plt.figure()

# ax = fig_pos.add_subplot()

# ax= sns.kdeplot(data=all_points[:,2], x=all_points[:,0], y=all_points[:,1], fill=True, palette='viridis')
# # x=0, y=1, weights=all_points[:,2]
# plt.show()

