#Read from the file
input = open("file.txt", "r")

#Returns tuple of tuples that represents the state taken from the file
def LoadFromFile(filepath):
	valid = False
	n = int(filepath.readline())
	row = 0
	data = []
	error_message = "txt file inputed is invalid. try again"
	
	#creates a list of lists
	while row < n:
		temp = []
		s = filepath.readline()
		temp = s.replace("*", "0").split() #makes the list of strings
		if "0" in temp:
			valid = True
		if len(temp) != n: #checks if row is correct length
			return error_message
		temp = [int(i) for i in temp]
		data.append(temp)
		row = row + 1
	if len(data) != n: #Checks if it has the right number of rows
		return error_message
#checks to see if a hole is in the txt
	if valid == False:
		return error_message
	returnTuple = tuple(map(tuple, data))
	return returnTuple


#Computes the neighbors of a given state
# Returns a collection of pairs that contain
# the tile that goes into the hole and the new state
def ComputeNeighbors(state):
	hole_coords = [0,0]
	state = list(map(list, state))
	replace = []
	length = len(state)
	for row in range(length):
		for col in range(length):
			if state[row][col] == 0:
				hole_coords[0] = row
				hole_coords[1] = col

	#above 
	if isValid(hole_coords[0] - 1, hole_coords[1], length) == True:
		temp = [row[:] for row in state]
		neighbor = temp[hole_coords[0] - 1][hole_coords[1]]
		temp[hole_coords[0]][hole_coords[1]] = neighbor
		temp[hole_coords[0] - 1][hole_coords[1]] = 0
		tempAdd = tuple(map(tuple, temp))
		tupleAdd = (neighbor, tempAdd)
		replace.append(tupleAdd)

	#below
	if isValid(hole_coords[0] + 1, hole_coords[1], length) == True:
		temp = [row[:] for row in state]
		neighbor = temp[hole_coords[0] + 1][hole_coords[1]]
		temp[hole_coords[0]][hole_coords[1]] = neighbor
		temp[hole_coords[0] + 1][hole_coords[1]] = 0
		tempAdd = tuple(map(tuple, temp))
		tupleAdd = (neighbor, tempAdd)
		replace.append(tupleAdd)

	#right
	if isValid(hole_coords[0], hole_coords[1] + 1, length) == True:
		temp = [row[:] for row in state]
		neighbor = temp[hole_coords[0]][hole_coords[1] + 1]
		temp[hole_coords[0]][hole_coords[1]] = neighbor
		temp[hole_coords[0]][hole_coords[1] + 1] = 0
		tempAdd = tuple(map(tuple, temp))
		tupleAdd = (neighbor, tempAdd)
		replace.append(tupleAdd)

	#left
	if isValid(hole_coords[0], hole_coords[1] - 1, length) == True:
		temp = [row[:] for row in state]
		neighbor = temp[hole_coords[0]][hole_coords[1] - 1]
		temp[hole_coords[0]][hole_coords[1]] = neighbor
		temp[hole_coords[0]][hole_coords[1] - 1] = 0
		tempAdd = tuple(map(tuple, temp))
		tupleAdd = (neighbor, tempAdd)
		replace.append(tupleAdd)
	returnTuple = tuple(replace)
	return returnTuple

#Makes sure the input is within the given boundaries
def isValid(y,x, length):
	if x >= 0 and x <= length -1:
		if y >= 0 and y <= length -1:
			return True
	return False

#Prints out the state - just for testing
def DeBugPrint(state):
	n = len(state)
	row = 0
	print("_____________________________")
	while row < n:
		s = str(state[row]).strip('[]')
		temp = s.replace(",", "	")
		print(temp)
		row = row + 1
	print("_____________________________")

#Returns True if the state is the goal, false otherwise
def IsGoal(state):
	length = len(state)
	flattenState = [j for sub in state for j in sub]#Makes the state a single list
	NoHole = flattenState[:(length*length) - 1]
	lastLine = state[length - 1]
	if sorted(NoHole) == NoHole:
		if lastLine[length - 1] == 0:
			return True
	return False

#Finds the path it takes to get from one 
def FindPath(parents, final_state):
	path = [] #getall the states
	tiles = []
	current = final_state
	count = 1

#create a list of all the states in the path
	while current != None:
		path.append(current)
		current = parents[current]

#find the tiles moved for each state
	for currstate in path:
		if(count < len(path)):
			tiles.append(FindTileChange(path[count], currstate))
			count = count + 1
	tiles.reverse()
	return tiles

#Swaps two tiles
def FindTileChange(parent, child):
	for neighbor in ComputeNeighbors(child):
		if neighbor[1] == parent:
			return neighbor[0]

#Uses the BFS method to find a solution to the puzzle
# Returns a sequence of tile needed to move to reach the goal
def BFS(state):
	frontier = [state]
	discovered = set(state)
	parents = {state: None}
	
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(current_state)

		if IsGoal(current_state):
			return FindPath(parents, current_state)

		for neighbor in ComputeNeighbors(current_state):
			if neighbor[1] not in discovered:
				frontier.append(neighbor[1])
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state
	return None

#Uses the DPS method to find a solution to the puzzle
#Returns a sequence of tiles needed to move to reach the goal
def DFS(state):
	frontier = [state]
	discovered = set(state)
	parents = {state: None}

	while frontier:
		current_state = frontier.pop(0)
		discovered.add(current_state)

		if IsGoal(current_state):
			return FindPath(parents, current_state)

		for neighbor in ComputeNeighbors(current_state):
			if neighbor[1] not in discovered:
				frontier.insert(0, neighbor[1]) #add to front
				discovered.add(neighbor[1])	
				parents[neighbor[1]] = current_state
	return None

#Creates a goalstate that represents our target for the method
def GetGoalState(state):
	flattenState = [j for sub in state for j in sub]#Makes the state a single list
	flattenState.remove(0)
	flattenState.sort()
	flattenState.append(0)
	goalstate = []
	print(flattenState)
	
	location = 0
	while location < len(state)*len(state):
		goalstate.append(flattenState[location:(location + 4)])
		location = location + len(state)
	goalstate = tuple(map(tuple, goalstate))
	return goalstate

#Implements the bidirectional search method
# Returns a list tiles needed to be moved to reach the goal state
def BidirectionalSearch(state):
	goal = GetGoalState(state)
	frontierF = [state]
	frontierB = [goal]
	discoveredF = set(state)
	discoveredB = set(goal)
	parentsF = {state: None}
	parentsB = {goal: None}

	while frontierF or frontierB:
		current_stateF = frontierF.pop(0)
		current_stateB = frontierB.pop(0)

		discoveredF.add(current_stateF)
		discoveredB.add(current_stateB)

		if len(discoveredF.intersection(discoveredB)) > 0:
			point = list(discoveredF.intersection(discoveredB))[0]
			pathF = FindPath(parentsF, point)
			pathB = FindPath(parentsB, point)
			pathB.reverse()
			return pathF + pathB


#Forward Compute Neighbors
		for neighbor in ComputeNeighbors(current_stateF):
			if neighbor[1] not in discoveredF:
				frontierF.append(neighbor[1])
				discoveredF.add(neighbor[1])	
				parentsF[neighbor[1]] = current_stateF

#BackwardsCompute Neighbors
		for neighbor in ComputeNeighbors(current_stateB):
			if neighbor[1] not in discoveredB:
				frontierB.append(neighbor[1])
				discoveredB.add(neighbor[1])	
				parentsB[neighbor[1]] = current_stateB

def main():
	state = LoadFromFile(input)
	print("BidirectionalSearch:")
	print(BidirectionalSearch(state))
	print("__________________________________")
	print("BFS:")
	print(BFS(state))
	print("__________________________________")
	print("DFS:")
	print(DFS(state))
	print("__________________________________")


main()