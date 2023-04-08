import numpy as np
from os.path import isfile

# Takes in a phasespace file from TOPAS and makes secondary electrons from given information

# How many electrons per crossing of the seconday emitter?
# We can have electrons per crossing per energy in a large file. Path for determing how many
# to make is as follows:
# Look up energy of crossing. That gives a mean and FWHM
# Choose a number from the distribution given by that mean and FWHM. That is how many new
# entries to make. These new entries should have a set of energies as given by another
# attached distribution. They are created with random angles. Need to determine if those
# angles should be both into and outof the secondary emitter or just out. Preferred is just
# outward angles (as defined by the sign of col 9 in the phsp file "flag to tell if Third 
# Direction Cosine is Negative (1 means true)"). Unfortunatly as phase space files do not
# contain the surface that the particle crossed we likely need to make an even spread of
# particles through 360 degrees.

# To process time information each new grouping of electrons gets given a new history. These
# histories are connected to an external file with the total TOF of that history. The way
# this is handled is that when creating a new group of secondaries the TOF from the startup
# file gets loaded. If there is no file we know this is the first run of the secondary 
# iteration, and so TOF is 0 ns. This loaded TOF is then added to the TOF of the incident
# electron, giving a new total TOF for the start of the new history. This process is then
# repeated, giving the total TOF of each electron (file TOF + last history TOF)

# To maintain good behavior of the backplane outputter, the backplane combiner code must be
# run on every generation of secondaries. This is necessasary to have the right history
# information available to the backplane for giving correct total times.
# For this reason backplane combiner code is now contained within this handling code. Each
# time it moves forward a history in the main tuple file it appends the current working
# history to the backplane file 


# read in the line from the phase space scorer:
# source_file = "put your filename here"
# source_file = "generation_" + str(generation) + "/full_HGM"
source_file = "full_HGM"
starting_histories = np.loadtxt(source_file + ".phsp")
print(np.shape(starting_histories))

backplane_source_file = "backplane"
backplane_histories = np.loadtxt(backplane_source_file + ".phsp")
backplane_out = []
backplane_index = 0

# time data storage file name
time_file = "time_data"
time_source = np.loadtxt(time_file)
print(np.shape(time_source))

existing_time = 0
if (np.shape(time_source)[0] != 0):
    existing_time = 1

history_number = -1
time_saves = []
total_histories = 0
recorded_histories = 0

total_electrons = 0


# output = "generation_" + str(generation + 1) + "/"
# output += "output"
output = "output"

blank_hist = np.array([0,0,0,0,0,0,-1,0,0,1,0,0,0])
print(np.shape(blank_hist))

all_hists = np.zeros((2,13))
first_in_hist = 1
prior_hist_written = 1

for i in range(np.shape(starting_histories)[0]):

    # Is this an empty history? (is the weight 1 or -1)
    # If it's empty then we just reoutput it and move to the next line.
    working_hist = starting_histories[i,:]
    if (working_hist[9]):
        history_number += 1
        # print("read history " + str(history_number))

        # now we need to write the backplane phsp to its output for the current history
        current_backplane = backplane_histories[backplane_index, :]
        if (existing_time):
            current_backplane[10] += time_source[history_number - 1]
        backplane_out.append(str(current_backplane[0]) + " " + str(current_backplane[1]) + " " + str(current_backplane[2]) + " " + str(current_backplane[3]) + " " + str(current_backplane[4]) + " " + str(current_backplane[5]) + " " + str(current_backplane[6]) + " " + str(current_backplane[7]) + " " + str(current_backplane[8]) + " " + str(current_backplane[9]) + " " + str(current_backplane[10]) + " " + str(current_backplane[11]) + "\n")
        backplane_index += 1
        while ((backplane_index < np.shape(backplane_histories)[0]) and (backplane_histories[backplane_index, 9] == 0)):
            current_backplane = backplane_histories[backplane_index, :]
            if (existing_time):
                current_backplane[10] += time_source[history_number - 1]
            backplane_out.append(str(current_backplane[0]) + " " + str(current_backplane[1]) + " " + str(current_backplane[2]) + " " + str(current_backplane[3]) + " " + str(current_backplane[4]) + " " + str(current_backplane[5]) + " " + str(current_backplane[6]) + " " + str(current_backplane[7]) + " " + str(current_backplane[8]) + " " + str(current_backplane[9]) + " " + str(current_backplane[10]) + " " + str(current_backplane[11]) + "\n")
            backplane_index += 1


    if ((working_hist[6] == 1) and (working_hist[7] == 11) and (working_hist[5] > 0.0001)):
        # if the weight of the history is 1 (so we have a real history)
        # We have also checked that it is an electron, and it has enough energy

        # If not empty then we need to go through the process of making secondaries
        first_in_hist = 1
        
        # what energy is it at, find the correct distribution of new electrons
        prior_hist_written = 1
        energy_MeV = working_hist[5] # measured in MeV

        # lets record the time of this interaction within the history
        run_time = working_hist[10]
        if (existing_time):
            run_time += time_source[history_number]
        # print(run_time)

        time_saves.append(str(run_time) + "\n")

        number_of_electrons = 5

        electron_energy_MeV = 0.00005
        total_electrons += number_of_electrons
        total_histories += 1
        recorded_histories +=1

        new_electrons = np.zeros((number_of_electrons, 13))
        # print(np.shape(new_electrons))
        # ok now how many electrons, what energy does each one get

        for i in range(number_of_electrons):
            new_electrons[i] = working_hist
            electron_energy_MeV = np.random.normal(10, 2)
            if (electron_energy_MeV <= 4):
                electron_energy_MeV = 4
            electron_energy_MeV = electron_energy_MeV / 1000000
            new_electrons[i,5] = electron_energy_MeV
            new_electrons[i,9] = first_in_hist
            first_in_hist = 0
            # Ok give each a direction
            direction = np.random.normal(0.0,1.0, 3)
            direction = direction/np.linalg.norm(direction)
            # This is a trick from stackexchange. A vector made from N normally distributied lengths
            # will be uniformly distributed over a sphere, so if normalized give a uniform distribution
            # on the unit sphere.
            # This direction vector contains the direction cosines for the direction
            new_electrons[i,3] = direction[0]
            new_electrons[i,4] = direction[1]
            if (direction[2] < 0):
                new_electrons[i,8] = 1
            else:
                new_electrons[i,8] = 0


        # Print the new electrons to the new phase space file.
        # new_electrons = new_electrons[:-2,:] # remove the last electron in the list (the parent electron)
        # print(np.shape(new_electrons))

        all_hists = np.append(all_hists, new_electrons, axis=0)

        # print(np.shape(all_hists))

        # np.savetxt(output, new_electrons, fmt='%12f %12f %12f %12f %12f %12f %12i %12i %2i %2i %12d %12i')
    if (working_hist[9]):
        if (not prior_hist_written):
            all_hists = np.append(all_hists, [blank_hist], axis=0)
            time_saves.append(str(0.0) + "\n")
            total_histories += 1
        prior_hist_written = 0



if (not prior_hist_written):
    all_hists = np.append(all_hists, [blank_hist], axis=0)

        
np.savetxt(output + ".phsp", all_hists[2:], fmt='%12f %12f %12f %12f %12f %12f %12i %12i %2i %2i %12f %12i %12i')

print(total_electrons)
    
header = open(source_file + ".header", "r")
full_file = header.readlines()
full_file[2] = "Number of Original Histories: " + str(int(total_histories)) + "\n"
full_file[3] = "Number of Original Histories that Reached Phase Space: " + str(int(recorded_histories)) + "\n"
full_file[4] = "Number of Scored Particles: " + str(int(total_electrons)) + "\n"

out_header = open(output + ".header", "w")

out_header.writelines(full_file)

out_header.close()

time_out = open(time_file, "w")

time_out.writelines(time_saves)

combined_backplanes = "combined.phsp"
combined_out = open(combined_backplanes, "a")
combined_out.writelines(backplane_out)
