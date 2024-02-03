import picar_4wd as fc
import time
import numpy as np
import nav
import matplotlib.pyplot as plt
import mapping
import navigation

from enum import Enum

#represents direction picar is facing North is +Y as reference point
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

map_idx = 0

#used to make accessing vector more readable
POSITION = 0
DIRECTION = 1
NUMSTEPS = 2

#how far ahead our sensors should scan
scanDist = 80
#number of steps our robot should take before scanning and updating our surroundings map

#map of our surroundings each 0 represents a cm^2 area
piMap = np.zeros((250, 250))
endPoint = (100, 230)

#hardcode our robot start position to the middle of the map facing North
startVector = [np.array([100, 100]), NORTH, 0]
picarVector = startVector

def completeScan():
  
    scan_list = []
    for angle in range(-90, 90, 5):
        tmp = fc.get_distance_at(angle)
        scan_list.append(tmp)    
    
    parsed_scan_list = []
    for scan_val in scan_list:
        if scan_val == -2 or scan_val > 80:
            parsed_scan_list.append(0)
        else:
            parsed_scan_list.append(scan_val)
    
    return parsed_scan_list

def plot_map(updated_map):
    global map_idx
    copy = np.copy(updated_map)
    plt.imshow(mapping.pad_map(copy), cmap='binary', interpolation='nearest', origin='lower')
    plt.colorbar()  # Optionally add a color bar
    plt.savefig("mapC" + str(map_idx) + ".png")
    plt.plot(picarVector[POSITION][0], picarVector[POSITION][1], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
    print("MAPC#" + str(map_idx))
    plt.clf
    map_idx += 1

def ScanSurroundings():
    
    global piMap
    scan_list = completeScan()
    piMap = np.zeros_like(piMap)
    piMap = mapping.update_map_by_scan(piMap, scan_list, picarVector[DIRECTION], picarVector[POSITION])
    plot_map(piMap)

def Move(newDir):
    changeDirection(newDir)
    nav.forwardX(1)
    updateVec(newDir)
    print("PICAR VECTOR" + str(picarVector))
    return

def updateVec(newDir):
    
    picarVector[DIRECTION] = newDir

    if picarVector[DIRECTION] == NORTH:
        picarVector[POSITION] += np.array([0, 8])
    elif picarVector[DIRECTION] == EAST:
        picarVector[POSITION] += np.array([8, 0])
    elif picarVector[DIRECTION] == SOUTH:
        picarVector[POSITION] += np.array([0, -8])
    elif picarVector[DIRECTION] == WEST:
        picarVector[POSITION] += np.array([-8, 0])
    else:
        print("you messed up")
    
    picarVector[NUMSTEPS] += 1
    if(picarVector[NUMSTEPS] == 1):
        picarVector[NUMSTEPS] = 0
        ScanSurroundings()
        print("PICAR POSITION" + str(picarVector[POSITION]))
        #calcualte next A*
        
#change direction will physiclly rotate the car to face the new direction
def changeDirection(newDir):
    change = picarVector[DIRECTION] - newDir
    print(change)
    if (change == 0): # no turn
        return
    elif (abs(change) == 1) or (abs(change) == 3): #90 degree turn
        if(change == -1) or (change == 3): #right turn
            nav.turnRight90()
            return
        elif(change == -3) or (change == 1): #left turn
            nav.turnLeft90()
            return
    elif (abs(change) == 2): # 180 degree turn
        nav.turn180()
        return
    else:
        print("Error changing from " + str(picarVector[DIRECTION]) + " to " + str(newDir))
        exit(-1)

def get_directions(point_list):
    

    if point_list == None or len(point_list) == 1:
        print("PICAR POSITION" + str(picarVector[POSITION]))
        print("ENDPOIT" + str(endPoint))
        return


    for p_idx in range(0, 51, 10):
        if(p_idx >= 10):
            x = point_list[p_idx][0] - point_list[p_idx - 10][0]
            y = point_list[p_idx][1] - point_list[p_idx - 10][1]
            if(x > 5):
                Move(EAST)
            if(x < -5):
                Move(WEST)
            if(y > 5):
                Move(NORTH)
            if(y < -5):
                Move(SOUTH)
    
while True:
    ScanSurroundings()
    copy = np.copy(piMap)
    point_list = navigation.astar_numpy(mapping.pad_map(copy), picarVector[POSITION], endPoint)
    get_directions(point_list)


# Heuristic for A* algorithim 
# OPEN = priority queue containing START
# CLOSED = empty set
# while lowest rank in OPEN is not the GOAL:
#   current = remove lowest rank item from OPEN
#   add current to CLOSED
#   for neighbors of current:
#     cost = g(current) + movementcost(current, neighbor)
#     if neighbor in OPEN and cost less than g(neighbor):
#       remove neighbor from OPEN, because new path is better
#     if neighbor in CLOSED and cost less than g(neighbor): ⁽²⁾
#       remove neighbor from CLOSED
#     if neighbor not in OPEN and neighbor not in CLOSED:
#       set g(neighbor) to cost
#       add neighbor to OPEN
#       set priority queue rank to g(neighbor) + h(neighbor)
#       set neighbor's parent to current
# 
# reconstruct reverse path from goal to start
# by following parent pointers
#     
#     