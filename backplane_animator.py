import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


# full_data = np.loadtxt("combined_backplane.phsp")
# full_data = np.loadtxt("full_channel_test.phsp")
full_data = np.loadtxt("demo_backplane.phsp")
full_data = full_data[full_data[:, 6] > 0,:]
print(np.shape(full_data))

all_points = np.zeros((np.shape(full_data)[0], 3))
all_points[:,0] = full_data[:,1]
all_points[:,1] = full_data[:,2]
all_points[:,2] = full_data[:,10]

correct_order = np.argsort(all_points[:,2])
time_sorted = all_points[correct_order,:]

first_time = time_sorted[0,2]
last_time = time_sorted[np.shape(time_sorted)[0]-1, 2]

print("earliest: " + str(first_time))
print("latest: " + str(last_time))

# print(time_sorted)


def main():
    numframes = np.shape(time_sorted)[0]-1
    numpoints = 10
    # color_data = np.random.random((numframes, numpoints))
    x = time_sorted[:,0]
    y = time_sorted[:,1]

    fig, scat = plt.subplots()
    scat.set_ylim(top=np.amax(y), bottom=np.amin(y))
    scat.set_xlim(left=np.amin(x), right=np.amax(x))

    ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes),
                                  fargs=(time_sorted, scat), interval=3)
    plt.show()

def update_plot(i, data, scat):
    scat.scatter(data[i,0],data[i,1])
    return scat,

main()