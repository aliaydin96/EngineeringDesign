from Self_Localization import *
from Environment_Sensing_Unit import *
from motor import *
x_position_initial = 0
y_position_initial =0
angle_initial=90
desired_x_position = 0
desired_y_position = 0

for forCounter in range(1):
    ESU(forCounter)
#    self_localization_part(x_position,y_position,anglesum,desired_x_position,desired_y_position,forCounter)
    [x_position,y_position ,angle] = self_localization_part(x_position_initial,y_position_initial,angle_initial,desired_x_position,desired_y_position,forCounter)
 
    x_position_initial = x_position
    y_position_initial = y_position
    angle_initial = angle     
    

