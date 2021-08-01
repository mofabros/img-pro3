#
#This script takes inputs N,M,S, and two .png files (of the same height and width) - one RGB and one in black and white
#This script then takes N patches of MxM size from random locations in the RGB file based on the control file in black and white
#(the randomness of the locations is limited by the imposed ratio S of center black pixels to center white pixels)
#

from PIL import Image, ImageDraw, ImageEnhance
import random
import math


N = int(input("What is N? (number of patches, integer > 0) "))
M = int(input("What is M? (patch size, odd integer > 0) "))
S = float(input("What is S? (ratio of center black:white pixels, value between 0-1, inclusive) "))
orgpath_rgb = input("What is the RGB filename? (you can use 'default') ")
orgpath_bw = input("What is the Black/White filename? (you can use 'default') ")

#N = 100
#M = 201
#S = .78
if orgpath_rgb == 'default':
	orgpath_rgb = 'org1.png'
if orgpath_bw == 'default':
	orgpath_bw = 'org2.png'

image_rgb = Image.open(orgpath_rgb)

image_bw = Image.open(orgpath_bw)

def find_white_coordinates(image):
	list = []
	image_data = image.load()
	height,width = image.size
	for y in range(0,height):
		for x in range(0,width):
			if image_data[y,x]!=0:
				list.append((x,y))
	return list
	
def create_patches(amount,size,accuracy,image,white_coord):
	all_patches = []
	num_white_center_pix = int(amount*accuracy) #calculate how many patches of the RGB .png file need a white center pixel in the same pixel location as in the black and white .png file
	image_data = image.load()
	height, width = image.size

	used_coord = [] #hold used coordinates to prevent duplicate random locations in the RGB .png file
	for white_pix in range(0,num_white_center_pix): # based on the assumptions, this loop will create approx. N*S patches out of the RGB .png file that have a corresponding white center pixel in the black and white .png file
		rand_seed = random.randint(0,len(white_coord)-1)
		blank_image = Image.new('RGB',(size,size),color="black")
		x,y=white_coord.pop(rand_seed)
		
		track_h = 0
		track_w = 0
		for y_coord in range(y-math.floor(size/2),y+math.ceil(size/2)): # traverse the relevant area in the RBG .png file
			for x_coord in range(x-math.floor(size/2),x+math.ceil(size/2)):
				if 0<=y_coord<height and 0<=x_coord<width: # if pixel lies within the original RGB .png file, put it in the patch, else make it black if outside the edges
					r,g,b = image_data[y_coord,x_coord]
					blank_image.putpixel((track_h,track_w),(r,g,b))
				track_w+=1
			track_h+=1
			track_w=0
		all_patches.append(blank_image)
		used_coord.append((x,y))
		
	num_black_center_pix = amount-num_white_center_pix
	
	for black_pix in range(0,num_black_center_pix): # based on the assumptions, this loop will create approx. N*(1-S) patches out of the RGB .png file that have a corresponding black center pixel in the black and white .png file
		y = random.randint(0,height)
		x = random.randint(0,width)
		while (x,y) in used_coord: # prevent coordinate duplicates
			y = random.randint(0,height)
			x = random.randint(0,width)
		used_coord.append((x,y))
		
		blank_image = Image.new('RGB',(size,size),color="black")
		
		track_h = 0
		track_w = 0
		for y_coord in range(y-math.floor(size/2),y+math.ceil(size/2)): # traverse the relevant area in the RBG .png file
			for x_coord in range(x-math.floor(size/2),x+math.ceil(size/2)):
				if 0<=y_coord<height and 0<=x_coord<width:
					r,g,b = image_data[y_coord,x_coord]
					blank_image.putpixel((track_h,track_w),(r,g,b))
				track_w+=1
			track_h+=1
			track_w=0
		all_patches.append(blank_image)
	return all_patches
	
def save_patches(patches):
	save_num=1
	for image in patches:
		image.save(str(save_num)+'.png')
		save_num+=1
		



white_coordinates = find_white_coordinates(image_bw)

my_patches = create_patches(N,M,S,image_rgb,white_coordinates)

save_patches(my_patches)