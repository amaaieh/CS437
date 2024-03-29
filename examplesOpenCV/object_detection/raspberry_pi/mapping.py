#Draw map from vision
import math
import numpy as np
from scipy.ndimage import distance_transform_edt

def update_map_by_scan(map, scan, facing, car_position, distance=80):
  for i in range(len(scan)):
    rads = 5*i*math.pi/180.0
    x_diff = scan[i]*math.cos(rads)
    y_diff = scan[i]*math.sin(rads)
    target = (0,0)
    #right
    if facing == 0:
      target = (car_position[0] + y_diff, car_position[1] + x_diff)
    #up      
    if facing == 1:
      target = (car_position[0] + x_diff, car_position[1] + y_diff)
    #down
    if facing == 3:
      target = (car_position[0] - x_diff, car_position[1] - y_diff)
    #left
    if facing == 2:
      target = (car_position[0] - y_diff, car_position[1] - x_diff)
    if int(target[0]) < len(map) and int(target[1]) < len(map[0]) and int(target[0]) > 0 and int(target[1]) > 0:
        if scan[i] == 0:
            map[int(target[0]), int(target[1])] = 0
        else:
            map[int(target[0]), int(target[1])] = 1
  return map

def pad_map(map):
  copy = np.copy(map) 
  distance_map = distance_transform_edt(copy == 0)
  close_areas = distance_map <= 20
  copy[close_areas] = 1
  return copy
