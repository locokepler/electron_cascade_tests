# makes a set of wire planes with a equal spacing between each wire. This gives
# a hexagonal tiling.
# The HGM is built with the wires going in the Z direction, the planes 
# extending in the Y axis, and the path through being in the X direction

import numpy as np

num_of_planes = 2 # how many vertical planes to make
length_mm = 100.0 # wire length in mm
width_ribbons = 20 # number of wires wide each plane is
ribbon_angle = 79.8 # angle of the ribbon above the horizontal

thickness_mm = 150/1000 # thickness of a ribbon
width_mm = 10.0 # width of a ribbon
pitch_mm = 1 # the distance between wires. Measured from center to center
# the wires are 
# path_length_mm = (50/1000) * 6
# ribbon_angle = np.rad2deg(np.arccos(thickness_mm/path_length_mm))
# width_mm = (pitch_mm * 2) / np.cos(np.deg2rad(ribbon_angle))

# ribbon_angle = np.rad2deg(np.arccos(np.sqrt(1)/width_mm))

cross_dist = ((width_ribbons - 0.5) * pitch_mm) + (width_mm * np.cos(ribbon_angle * (np.pi / 180)))
half_height = width_mm * np.sin(ribbon_angle * (np.pi / 180)) * (num_of_planes / 2)

box_buffer_mm = 1
# half_height += box_buffer_mm / 2

# coating_thickness_mm = 0.001

corner = [half_height + (0.5 * box_buffer_mm), cross_dist / 2, length_mm / 2]

# material = "\"G4_W\""
material = "\"G4_GLASS_LEAD\""
# coating = "\"G4_MAGNESIUM_OXIDE\""
parent_nm = "HGM"

file_text = "# A TOPAS file containing the ribbon based HGM.\n"
file_text += "# Built at angle " + str(ribbon_angle) + " deg"

dynode_box = "\n # the box holding the HGM (made of vacuum)\n"
dynode_box += "s:Ge/" + parent_nm + "/Type      = \"TsBox\"\n"
dynode_box += "s:Ge/" + parent_nm + "/Material  = \"Vacuum\"\n"
dynode_box += "d:Ge/" + parent_nm + "/HLX       = " + str(corner[0] + thickness_mm) + " mm\n" # includes a small fudge to fit
dynode_box += "d:Ge/" + parent_nm + "/HLY       = " + str(corner[1] + thickness_mm) + " mm\n" # ibid
dynode_box += "d:Ge/" + parent_nm + "/HLZ       = " + str(corner[2]) + " mm\n"

dynode_box += "\n# Add an electric field to the box to move secondaries\n"
dynode_box += "s:Ge/" + parent_nm + "/Field = \"UniformElectroMagnetic\"\n"
dynode_box += "u:Ge/" + parent_nm + "/ElectricFieldDirectionX    = -1.0\n"
dynode_box += "u:Ge/" + parent_nm + "/ElectricFieldDirectionY    = 0.0\n"
dynode_box += "u:Ge/" + parent_nm + "/ElectricFieldDirectionZ    = 0.0\n"
dynode_box += "d:Ge/" + parent_nm + "/ElectricFieldStrength      = 500 V/mm\n"
dynode_box += "u:Ge/" + parent_nm + "/MagneticFieldDirectionX    = 0.0\n"
dynode_box += "u:Ge/" + parent_nm + "/MagneticFieldDirectionY    = 1.0\n"
dynode_box += "u:Ge/" + parent_nm + "/MagneticFieldDirectionZ    = 0.0\n"
dynode_box += "d:Ge/" + parent_nm + "/MagneticFieldStrength      = 0.0 tesla"

dynode_box += "\n# phase space scorer for the whole HGM (for secondary electron emission)\n"
dynode_box += "s:Sc/full_HGM/Quantity   \t = \"PhaseSpace\"\n"
dynode_box += "s:Sc/full_HGM/Surface    \t = \"" + parent_nm + "/AnySurface\"\n"
dynode_box += "s:Sc/full_HGM/OutputType \t = \"ASCII\"\n"
dynode_box += "b:Sc/full_HGM/IncludeTimeOfFlight\t = \"True\"\n"
dynode_box += "s:Sc/full_HGM/IncludeEmptyHistories \t = \"InSequence\"\n"
# dynode_box += "b:Sc/full_HGM/IncludeTrackID     \t = \"True\"\n"
dynode_box += "b:Sc/full_HGM/IncludeRunID       \t = \"True\"\n"
dynode_box += "sv:Sc/full_HGM/OnlyIncludeParticlesCharged   \t = 1 \"negative\"\n"
dynode_box += "s:Sc/full_HGM/IfOutputFileAlreadyExists   \t = \"Overwrite\"\n"
dynode_box += "b:Sc/full_HGM/PropagateToChildren         \t = \"true\"\n"
# dynode_box += "s:Sc/full_HGM/Quantity   \t = \"PhaseSpace\"\n"
# dynode_box += "s:Sc/full_HGM/Quantity   \t = \"PhaseSpace\"\n"

dynode_box += "\n# Parallel world plate for observing electrons crossing back of HGM\n"
dynode_box += "s:Ge/BackPlate/Parent = \"World\"\n"
dynode_box += "b:Ge/BackPlate/IsParallel = \"True\"\n"
dynode_box += "s:Ge/BackPlate/Type = \"TsBox\"\n"
dynode_box += "d:Ge/BackPlate/HLX = 0.01 mm\n"
dynode_box += "d:Ge/BackPlate/HLY = " + str(corner[1] + thickness_mm) + " mm\n"
dynode_box += "d:Ge/BackPlate/HLZ = " + str(corner[2]) + " mm\n"
dynode_box += "d:Ge/BackPlate/transx = " + str(half_height - (0.5 * box_buffer_mm) + thickness_mm) + " mm\n"
# dynode_box += "d:Ge/BackPlate/transy = Ge/" + parent_nm + "/transy mm\n"
# dynode_box += "d:Ge/BackPlate/transz = Ge/" + parent_nm + "/transz mm\n"
dynode_box += "\n"
dynode_box += "s:Sc/backplane/Quantity = \"Phasespace\"\n"
dynode_box += "s:Sc/backplane/Surface = \"BackPlate/XPlusSurface\"\n"
dynode_box += "s:Sc/backplane/OutputType = \"ASCII\"\n"
dynode_box += "b:Sc/backplane/IncludeTimeOfFlight = \"True\"\n"
dynode_box += "s:Sc/backplane/IncludeEmptyHistories = \"InSequence\"\n"
dynode_box += "b:Sc/backplane/IncludeRunID = \"True\"\n"
dynode_box += "sv:Sc/backplane/OnlyIncludeParticlesCharged = 1 \"negative\"\n"
dynode_box += "s:Sc/backplane/IfOutputFileAlreadyExists = \"Increment\"\n"
dynode_box += "b:Sc/backplane/PropagateToChildren = \"false\"\n"

# The first wire is to be placed in the +x +y corner of the box. It is one radius short of the corner to fit

location = corner
location[2] = 0.0
location[0] -= (width_mm * np.sin(ribbon_angle * (np.pi / 180)) / 2) + (box_buffer_mm)
location[1] -= width_mm * np.cos(ribbon_angle * (np.pi / 180)) / 2

y_add_sub = -1
angle_flip = 1

dynode_structure = "\n\n# the planes of the structure\n\n"

for i in range(num_of_planes):
    for j in range(width_ribbons):
        # place a wire at the location, then move over one
        dynode_structure += "\n# plane coating " + str(i) + "_" + str(j) + "\n"
        dynode_structure += "s:Ge/C_" + str(i) + "_" + str(j) + "/Type      \t = \"TsBox\"\n"
        dynode_structure += "s:Ge/C_" + str(i) + "_" + str(j) + "/Parent    \t = \"" + parent_nm + "\"\n"
        dynode_structure += "s:Ge/C_" + str(i) + "_" + str(j) + "/Material  \t = " + material + "\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/HLZ       \t = " + str(length_mm / 2) + " mm\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/HLX    \t = " + str(thickness_mm / 2) + " mm\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/HLY    \t = " + str(width_mm / 2) + " mm\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/TransX    \t = " + str(location[0]) + " mm\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/TransY    \t = " + str(location[1]) + " mm\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/TransZ    \t = " + str(location[2]) + " mm\n"
        dynode_structure += "d:Ge/C_" + str(i) + "_" + str(j) + "/RotZ    \t = " + str(ribbon_angle * angle_flip) + " deg\n"

        # dynode_structure += "\n# plane " + str(i) + "_" + str(j) + "\n"
        # dynode_structure += "s:Ge/" + str(i) + "_" + str(j) + "/Type      \t = \"TsBox\"\n"
        # dynode_structure += "s:Ge/" + str(i) + "_" + str(j) + "/Parent    \t = \"" + parent_nm + "\"\n"
        # dynode_structure += "s:Ge/" + str(i) + "_" + str(j) + "/Material  \t = " + material + "\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/HLZ       \t = " + str(length_mm / 2) + " mm\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/HLX       \t = " + str((thickness_mm) / 2) + " mm\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/HLY       \t = " + str(width_mm / 2) + " mm\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/TransX    \t = 0 mm\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/TransY    \t = 0 mm\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/TransZ    \t = 0 mm\n"
        # dynode_structure += "d:Ge/" + str(i) + "_" + str(j) + "/RotZ      \t = 0 deg\n"


        location[1] += y_add_sub * pitch_mm
    
    location[0] += -width_mm * np.sin(ribbon_angle * (np.pi / 180))
    location[1] += -y_add_sub * pitch_mm * 0.5
    y_add_sub = -y_add_sub
    angle_flip = -angle_flip


print(file_text + dynode_box + dynode_structure)






