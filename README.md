# Overview #

This is my code for basic simulations of MCP like photomultiplers. As built it uses
a pattern of taking a list of electron locations and energies from TOPAS (https://www.topasmc.org/)
in the form of a .phsp file, making secondary electrons also in correct TOPAS phasespace
format, then passing those back into TOPAS to do move the physics along a bit farther.

The code is largely as is from my creation of it in spring 2023, but I made a simple demo
in October 2024 that should largely run from the downloading of the folder. You will need
to go into the scripts and set where TOPAS is on your computer, as it is unlikely to be
the same as on mine. 

The included TOPAS files run with uniform electric fields, however Cameron Poe did get a
version running with his arbitrary electric field extension.

# The Demo #

Get the repo onto your computer however you wish. Make sure you have a working install of
TOPAS as well. Set the location of that in the script `externally_generated_secondary_iterate.sh`
so that it can actually run TOPAS. You may also need to change which python version to run
as that was set to work on my laptop (a mac).

## Running the Demo Script ##

The demo script is `demo_run.sh` and it creates the `run_zone` folder, makes an example
LMCP like structure, and then runs the secondary emission behavior for an example electron.
The example electron is in the file `demo_electron.phsp`. The demo runs for 20 generations,
probably not enough to complete the cascade, but enough to give a good sample of the start
of the cascade. The demo may take a little while to run through, but it should be apparent
what is going on to some degree.

The plots that pop up at the end are just for demonstration, modify them or make new ones
to give better results for whatever you're doing. Do not forget the weight value! The weight
signifies how many electrons that individual electron repersents. If the weight is 0 then
it is an empty history that got recorded. I am not sure if the backplane can ever contain
those at this point, but it is something to be aware of.
