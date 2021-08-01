# img-pro3
# Process patches of an RGB image based on a black and white control image
#
# This script takes inputs N,M,S, and two .png files (of the same height and width) - one RGB and one in black and white
# This script then takes N patches of MxM size from random locations in the RGB file based on the control file in black and white
# (the randomness of the locations is limited by the imposed ratio S of center black pixels to center white pixels)
