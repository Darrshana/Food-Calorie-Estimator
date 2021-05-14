import cv2
import numpy as np
from image_segment import *
import random

secure_random = random.SystemRandom()
randomfloat = secure_random.uniform(22.7,25.4)

#density - gram / cm^3
density_dict = { 1:0.609 ,2:0.94, 3:0.218,4:0.513, 5:0.44,6:0.300}
#kcal
calorie_dict = { 1:52,2:89,3:24,4:40,5:47,6:20}
#skin of photo to real multiplier
skin_multiplier = 5*2.3

def getCalorie(label, volume): #volume in cm^3
	calorie = calorie_dict[int(label)]
	density = density_dict[int(label)]
	mass = volume*density*1.0
	
	print('Volume: ',volume,'cm^3')
	print('Mass: ', mass, 'grams')
	calorie_tot = (calorie/100.0)*mass
	print('Calories: ',calorie_tot,'cal')
	return mass, calorie_tot, calorie #calorie per 100 grams

def getVolume(label, area, skin_area, pix_to_cm_multiplier, fruit_contour):
	area_fruit = (area/skin_area)*skin_multiplier #area in cm^2
	label = int(label)
	volume = 100
	if label == 1 or label == 5  or label == 4 or label == 6 : #sphere-apple,tomato,orange,,onion
		radius = np.sqrt(area_fruit/np.pi)
		volume = (4/3)*np.pi*radius*radius*radius
		#print (area_fruit, radius, volume, skin_area)
	
	if label == 2 or label == 3 : #cylinder like banana
		fruit_rect = cv2.minAreaRect(fruit_contour)
		height = max(fruit_rect[1])*pix_to_cm_multiplier
		radius = area_fruit/(2.0*height)
		volume = np.pi*radius*radius*height
		
	
	
	return volume

def calories(result,img,name):
	print(name)
	'''
	if (name == "Bread"):
		print('')
		print('Volume: 40.42553914 cm^3')
		print('Mass: ',randomfloat/0.24,'grams')
		print('Calories: ',randomfloat,'cal')
		return randomfloat'''
	img_path = img
	fruit_areas,final_f,areaod,skin_areas, fruit_contours, pix_cm = getAreaOfFood(img)
	volume = getVolume(result, fruit_areas, skin_areas, pix_cm, fruit_contours)
	mass, cal, cal_100 = getCalorie(result, volume)
	fruit_volumes = volume
	fruit_calories = cal
	fruit_calories_100grams = cal_100
	fruit_mass =mass
    #print("\nfruit_volumes",fruit_volumes,"\nfruit_calories",fruit_calories,"\nruit_calories_100grams",fruit_calories_100grams,"\nfruit_mass",fruit_mass)
	return fruit_calories

