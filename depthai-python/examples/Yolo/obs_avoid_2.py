#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:33:27 2023

@author: danielruiz
"""
import numpy as np
import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
import time


#---Buckets (this should == 5)--------

buckets = 5

#-------------

def quadrents(num_sections,image,mag):
    r,c = np.shape(image)
    
    section_width = ((c)//num_sections)
    array_list = np.split(image, num_sections, axis=1)
    sum_array = []
    
    for i, array in enumerate(array_list):
        #print(f"Array {i+1} (10x1):\n", array)
        value = np.sum(array)
        sum_array.append(value)
    obs_section = np.argmax(sum_array)    
    turn_dir = turn_value(obs_section,num_sections,mag)
    
    #turn_value = (turn_value/turn_value)-0.5  This will return the dzturn to be straight
    avg_depth = np.max(sum_array)/51200
    
        
    return obs_section, turn_dir, avg_depth


def turn_value(section_number,columns,mag):
        
        
        if section_number == 0:
            #print("Slight Right Turn")
            output = 0.65 #"slight right"
            #print(output)
        elif section_number == 1:
            #print("Hard Right Turn")
            output = 0.75 #"hard right"
            #print(output)
        elif section_number == 2:
            #print("Hard Left or Right Turn")
            output = 0.25 # hard left or right
            #print(output)
        elif section_number == 3:
            #print("Hard Left Turn")
            output = 0.25 #"hard left"
            #print(output)
        elif section_number == 4:
            #print("Slight Left Turn")
            output = 0.35 #"slight left"
            #print(output)
        return output
        
        #Add a slight pause 
            
        # Dont forget to add actual steering values for this          
        '''
        This code pertains to how the steering values are assigned given the region where
        the object is located
    
        if section_number < columns //2:
            #turn right
            steering_value = mag/2
            print("turn right!")
            print("steering value = ",steering_value)
        elif section_number > columns//2:
            #turn left
            steering_value = -mag/2
            print("turn left!")
            print("steering value = ",steering_value)
        else:
            #go straight
            steering_value = mag
            print("go straight!")
            print("steering value = ",steering_value)
            
            '''
    
# Depth image array

'''
depth_image = np.array([[5, 1, 5, 5],
                       [5, 2, 5, 5],
                       [5, 3, 5, 5],
                       [5, 5, 5, 5],
                       [5,5,5,5]])
'''


#----- TEST DETPH IMAGE -----------

#depth_image = np.genfromtxt('DepthTest1.csv', delimiter=',')
#depth_image = np.genfromtxt('Max_Det.csv', delimiter=',')
#depth_image = np.genfromtxt('Min_Det.csv', delimiter=',')

#------------------------------------
#depth_array_1d = depth_image.flatten()

#---------- Create a color map plot---------------

# plt.imshow(depth_image, cmap='viridis')
# plt.title("Depth Array");plt.xlabel("X-Coordinate");plt.ylabel("Y-Coordinate")
# plt.colorbar(label = "Depth ")
# plt.grid(True)
# xticks = np.linspace(0,640,buckets+1)
# x_tick_labels =["0","1","2","3","4","5"]
# plt.xticks(xticks, x_tick_labels) 
# # Show the color map plot
# plt.show()

#-----------------------------------------------

# while True:
#    bucket,turn_dir,avg_depth = quadrents(buckets,depth_image,0.75)  #quadrents(buckets, image, steering rate)
#    #print(avg_depth)
#    if avg_depth > 50:
#        turn_input = turn_dir        # If our depth is above the threshold, set the variable == output of function
#        time.sleep(0.5)
#        print(turn_input)
#    else:
#        turn_input = 0.5             #Center the wheels
