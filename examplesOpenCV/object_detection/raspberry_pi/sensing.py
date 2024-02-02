import picar_4wd as fc
import time
import numpy as np
import nav
import matplotlib.pyplot as plt
import mapping

from enum import Enum

#represents direction picar is facing North is +Y as reference point
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

#used to make accessing vector more readable
POSITION = 0
DIRECTION = 1
NUMSTEPS = 2

#how far ahead our sensors should scan
scanDist = 80
#number of steps our robot should take before scanning and updating our surroundings map

#map of our surroundings each 0 represents a cm^2 area
piMap = np.zeros((250, 250))

#hardcode our robot start position to the middle of the map facing North
startVector = [np.array([100, 100]), NORTH, 0]
picarVector = startVector

def completeScan():
  
    scan_list = []
    for angle in range(-90, 90, 5):
        tmp = fc.get_distance_at(angle)
        scan_list.append(tmp)    
    
    print(scan_list)
    parsed_scan_list = []
    for scan_val in scan_list:
        if scan_val == -2 or scan_val > 80:
            parsed_scan_list.append(0)
        else:
            parsed_scan_list.append(1)
    
    print(parsed_scan_list)
    return parsed_scan_list

def plot_map(updated_map):
    plt.imshow(mapping.pad_map(updated_map), cmap='binary', interpolation='nearest', origin='lower')
    plt.colorbar()  # Optionally add a color bar
    plt.savefig("map.png")

def ScanSurroundings():
    
    global piMap
    scan_list = completeScan()
    piMap = mapping.update_map_by_scan(piMap, scan_list, picarVector[DIRECTION], picarVector[POSITION])
    plot_map(piMap)

def Move(newDir):
    changeDirection(newDir)
    updateVec(newDir)
    print(picarVector)
    nav.forwardX(1)
    return

def updateVec(newDir):
    
    picarVector[DIRECTION] = newDir

    if picarVector[DIRECTION] == NORTH:
        picarVector[POSITION] += np.array([10, 0])
    elif picarVector[DIRECTION] == EAST:
        picarVector[POSITION] += np.array([0, 10])
    elif picarVector[DIRECTION] == SOUTH:
        picarVector[POSITION] += np.array([-10, 0])
    elif picarVector[DIRECTION] == WEST:
        picarVector[POSITION] += np.array([0, -10])
    else:
        print("you messed up")
    
    picarVector[NUMSTEPS] += 1
    if(picarVector[NUMSTEPS] == 4):
        picarVector[NUMSTEPS] = 0
        ScanSurroundings()
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

#TESTING
def tests():
    ScanSurroundings()
    #A* get next 5 moves
    Move(NORTH) #straight
    Move(SOUTH) #180
    Move(EAST)  #left
    Move(SOUTH) #right
    Move(NORTH) #180
    Move(WEST) #left
    Move(SOUTH) #left
    Move(EAST) #left
    Move(SOUTH) #right
    Move(WEST) #right
    Move(NORTH) #right

tests()
#ScanSurroundings()
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