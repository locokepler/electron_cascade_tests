import numpy as np


source_file_base = "run_zone/backplane"
total_runs = 13

output = "combined"

all_files_names = []
all_data = []

for i in range(total_runs):
    filename = " "
    if (i == 0):
        filename = source_file_base + ".phsp"
    else:
        filename = source_file_base + "_" + str(i) + ".phsp"
    print("loading " + filename)
    all_data.append(np.loadtxt(filename))

# only working for the first history
all_hists = np.zeros((2,12))


for i in range(total_runs):
    # check if the file only has one entry
    if (np.shape(all_data[i])[0] == 12):
        if (all_data[i][6] != -1):
            # non-empty history
            all_hists = np.append(all_hists, [all_data[i]], axis=0)

    else:
        all_hists = np.append(all_hists, all_data[i], axis=0)

            
np.savetxt(output + ".phsp", all_hists[2:], fmt='%12f %12f %12f %12f %12f %12f %12i %12i %2i %2i %12f %12i')


























































































# # now go through the data one history at a time, combining it all into a single great big mashup

# # Iteration moves along by finding new histories
# total_histories = np.sum(all_data[0][:,9])
# print("Total histories: " + str(total_histories))

# handled_histories = 0
# blank_hist = np.array([0,0,0,0,0,0,-1,0,0,1,0,0])
# all_hists = np.zeros((2,12))

# working_location = np.zeros((len(all_data)))

# while (handled_histories < total_histories):
#     # first check if there is anything in any dataset from this history
#     blank = True
#     for i in range(len(all_data)):
#         # is there a -1 in the weight of every entry at it's index?
#         blank = blank and (all_data[i][working_location[i], 6] == -1)

#     if (blank):
#         all_hists = np.append(all_hists, [blank_hist], axis=0)
#     else:
#         # there is something of value here, lets step through adding it. We append nothing if it
#         # has weight -1, otherwise we append the value
#         for i in range(len(all_data)):
#             first_hist = 1
#             keep_looking = 1

#             while (keep_looking):
#                 data = all_data[i][working_location[i]]
#                 working_location[i] += 1

#                 if ((data[6] != -1) and ((data[9] == 0) or (first_hist))):
#                     # non-empty history, time to append
#                     first_hist = 0
#                     all_hists = np.append(all_hists, [data], axis=0)
#                 else:
#                     keep_looking = 0


# np.savetxt(output + ".phsp", all_hists[2:], fmt='%12f %12f %12f %12f %12f %12f %12i %12i %2i %2i %12f %12i')

