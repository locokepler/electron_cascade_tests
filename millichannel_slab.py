import numpy as np

# makes a millichannel slab. This is a structure of many thin glass ribbons with
# ridges to form channels when stacked. This structure is approximated in TOPAS
# by this code. The approximation is done by creating a large box the size of
# the stacked structure. This box is made of the ribbon material. Volumes
# corrosponding to the holes in the structure formed in the stackup are then added
# as children of the full box. In this implementation they are rectangular prism
# subtractions with a height of alpha, length of gamma, and separated by sections
# of glass beta thick. The ribbons themselves are t thick, the full structure is
# has a length of W from one end of a channel to the far side (in the direction
# of the field), and a cross direction length of l, in the direction of alpha.
# Finally there is the number of channels in the direction of beta and gamma, set
# as m

mil = 25.4 / 1000

alpha_mm = 2 * mil
beta_mm = 6 * mil
gamma_mm = 100 * mil
t_mm = 6 * mil
w_mm = 10
l_mm = 5
m = 4
material = "\"G4_GLASS_LEAD\""

fudge_mm = 0.3

k_mm = m * (beta_mm + gamma_mm) + beta_mm

# the numbers won't produce a perfect number of channels, so lets find the max
# number we can fit. In the t and alpha direction the maximum that can be fit is
# N * (T + alpha) + T < l_mm

n = np.floor((l_mm - t_mm) / (t_mm + alpha_mm))

parent_nm = "millichannel"

file_text = "# A TOPAS file defining the millichannel slab design for testing\n"
file_text += "# alpha = " + str(alpha_mm) + "mm\n"
file_text += "# beta = " + str(beta_mm) + "mm\n"
file_text += "# gamma = " + str(gamma_mm) + "mm\n"
file_text += "# t = " + str(t_mm) + "mm\n"
file_text += "# W = " + str(w_mm) + "mm\n"
file_text += "# L = " + str(l_mm) + "mm\n"
file_text += "# K = " + str(l_mm) + "mm\n"
file_text += "# N = " + str(n) + "\n"
file_text += "# M = " + str(m) + "\n"
file_text += "# material: " + material + "\n"

# build the big box

mill_box = "\n# the box of the millichannel slab\n"
mill_box += "s:Ge/" + parent_nm + "/Type     = \"TsBox\"\n"
mill_box += "s:Ge/" + parent_nm + "/Material = \"Vacuum\"\n"
mill_box += "d:Ge/" + parent_nm + "/HLX = " + str((w_mm + fudge_mm) / 2) + " mm\n"
mill_box += "d:Ge/" + parent_nm + "/HLY = " + str(k_mm / 2) + " mm\n"
mill_box += "d:Ge/" + parent_nm + "/HLZ = " + str(l_mm / 2) + " mm\n"
# mill_box += "s:Ge/" + parent_nm + "/ = \n"

mill_box += "s:Ge/" + parent_nm + "/Field                   = \"UniformElectroMagnetic\"\n"
mill_box += "u:Ge/" + parent_nm + "/ElectricFieldDirectionX = -1\n"
mill_box += "u:Ge/" + parent_nm + "/ElectricFieldDirectionY = 0\n"
mill_box += "u:Ge/" + parent_nm + "/ElectricFieldDirectionZ = 0\n"
mill_box += "d:Ge/" + parent_nm + "/ElectricFieldStrength   = 1000 V/mm\n"
mill_box += "u:Ge/" + parent_nm + "/MagneticFieldDirectionX = 0\n"
mill_box += "u:Ge/" + parent_nm + "/MagneticFieldDirectionY = 1\n"
mill_box += "u:Ge/" + parent_nm + "/MagneticFieldDirectionZ = 0\n"
mill_box += "d:Ge/" + parent_nm + "/MagneticFieldStrength   = 0.0 tesla\n"

mill_box += "\n# phase space scorer for the whole HGM (for secondary electron emission)\n"
mill_box += "s:Sc/full_HGM/Quantity   \t = \"PhaseSpace\"\n"
mill_box += "s:Sc/full_HGM/Surface    \t = \"" + parent_nm + "/AnySurface\"\n"
mill_box += "s:Sc/full_HGM/OutputType \t = \"ASCII\"\n"
mill_box += "b:Sc/full_HGM/IncludeTimeOfFlight\t = \"True\"\n"
mill_box += "s:Sc/full_HGM/IncludeEmptyHistories \t = \"InSequence\"\n"
mill_box += "b:Sc/full_HGM/IncludeTrackID     \t = \"True\"\n"
mill_box += "b:Sc/full_HGM/IncludeRunID       \t = \"True\"\n"
mill_box += "sv:Sc/full_HGM/OnlyIncludeParticlesCharged   \t = 1 \"negative\"\n"
mill_box += "s:Sc/full_HGM/IfOutputFileAlreadyExists   \t = \"Overwrite\"\n"
mill_box += "b:Sc/full_HGM/PropagateToChildren         \t = \"true\"\n"
# dynode_box += "s:Sc/full_HGM/Quantity   \t = \"PhaseSpace\"\n"
# dynode_box += "s:Sc/full_HGM/Quantity   \t = \"PhaseSpace\"\n"

# insert a backplane here for readout of secondary electrons. See 
# ribbon_planes.py for an example of how to implement this

mill_box += "\n# Parallel world plate for observing electrons crossing back of HGM\n"
mill_box += "s:Ge/BackPlate/Parent = \"World\"\n"
mill_box += "b:Ge/BackPlate/IsParallel = \"True\"\n"
mill_box += "s:Ge/BackPlate/Type = \"TsBox\"\n"
mill_box += "d:Ge/BackPlate/HLX = 0.01 mm\n"
mill_box += "d:Ge/BackPlate/HLY = " + str(k_mm / 2) + " mm\n"
mill_box += "d:Ge/BackPlate/HLZ = " + str(l_mm / 2) + " mm\n"
mill_box += "d:Ge/BackPlate/transx = " + str(w_mm / 2) + " mm\n"
# dynode_box += "d:Ge/BackPlate/transy = Ge/" + parent_nm + "/transy mm\n"
# dynode_box += "d:Ge/BackPlate/transz = Ge/" + parent_nm + "/transz mm\n"
mill_box += "\n"
mill_box += "s:Sc/backplane/Quantity = \"Phasespace\"\n"
mill_box += "s:Sc/backplane/Surface = \"BackPlate/XPlusSurface\"\n"
mill_box += "s:Sc/backplane/OutputType = \"ASCII\"\n"
mill_box += "b:Sc/backplane/IncludeTimeOfFlight = \"True\"\n"
mill_box += "s:Sc/backplane/IncludeEmptyHistories = \"InSequence\"\n"
mill_box += "b:Sc/backplane/IncludeTrackID     \t = \"True\"\n"
mill_box += "b:Sc/backplane/IncludeRunID = \"True\"\n"
mill_box += "sv:Sc/backplane/OnlyIncludeParticlesCharged = 1 \"negative\"\n"
mill_box += "s:Sc/backplane/IfOutputFileAlreadyExists = \"Overwrite\"\n"
mill_box += "b:Sc/backplane/PropagateToChildren = \"false\"\n"

corner = [(k_mm + fudge_mm) / 2 - (beta_mm*2 + (gamma_mm / 2)), l_mm / 2 - (t_mm + (alpha_mm / 2))]

hole_structure = "\n\n# the holes of the millichannel slab"

for i in range(int(n)):
    for j in range(m):
        # each vacuum box is centered at
        # a y of corner[0] - j * (beta + gamma)
        # a z of corner[1] - i * (t + alpha)
        hole_structure += "\n# hole " + str(i) + "_" + str(j) + "\n"
        hole_structure += "s:Ge/" + str(i) + "_" + str(j) + "/Type = \"TsBox\"\n"
        hole_structure += "s:Ge/" + str(i) + "_" + str(j) + "/Parent = \"" + parent_nm + "\"\n"
        hole_structure += "s:Ge/" + str(i) + "_" + str(j) + "/Material = " + material + "\n"
        hole_structure += "d:Ge/" + str(i) + "_" + str(j) + "/HLX = " + str(w_mm / 2) + " mm\n"
        hole_structure += "d:Ge/" + str(i) + "_" + str(j) + "/HLY = " + str(gamma_mm / 2) + " mm\n"
        hole_structure += "d:Ge/" + str(i) + "_" + str(j) + "/HLZ = " + str(alpha_mm / 2) + " mm\n"
        hole_structure += "d:Ge/" + str(i) + "_" + str(j) + "/TransY = " + str(corner[0] - (j * (beta_mm + gamma_mm))) + " mm\n"
        hole_structure += "d:Ge/" + str(i) + "_" + str(j) + "/TransZ = " + str(corner[1] - (i * (t_mm + alpha_mm))) + " mm\n"
        # hole_structure += "d:Ge/" + str(i) + "_" + str(j) + "/TransX = \n"

file_text += "# Corner:\n#\tx = " + str((w_mm + fudge_mm) / 2) + " mm\n#\ty = " + str(corner[0]) + " mm\n#\tz = " + str(corner[1]) + " mm\n"

print(file_text + mill_box + hole_structure)