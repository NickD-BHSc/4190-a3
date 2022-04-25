import sys
import re
from states import State, Boulder, Terminal

class Grid():

    def __init__(self, grid, width, height, startState, K, Episodes, discount, noise):
        self.grid = grid
        self.width = width
        self.height = height     
        self.startState = startState
        self.K = K
        self.Episodes = Episodes

        self.noise = noise
        self.discount = discount

        
    def checkTerminals(self, agentPosition):
        if self.grid[agentPosition[0]][agentPosition[1]].symbol == 'T':
            return True
        return False
    
    def getGrid(self):
        return self.grid

    def printUtility(self):
        result = ''
        for i in range(self.height):
            result += '['
            for j in range(self.width):
                state = self.grid[j][self.height-1 - i]
                if state.symbol == 'B':
                    result += 'B  : , '
                else:
                    value = state.utility
                    result += f'{value:.2f}:'+ state.policy + ', '
            result += ']\n'
        print(result)

    def printQvalue(self):
        RED='\033[0;31m'
        GREEN='\033[0;32m'
        BLACK='\033[0;30m'
        WHITE='\033[0;37m'
        BLUE='\033[0;34m'
        for y in range(self.height):
            flippedY = self.height-1 -y
            for i in range(4):
                for x in range(self.width):
                    isTerminal = self.grid[x][flippedY].symbol == 'T'
                    if self.grid[x][flippedY].symbol == 'B' or i%4 == 0:
                        print(f"{BLUE}################", end='')
                    elif isTerminal:
                        if i%4 == 2:
                            value = self.grid[x][flippedY].qvalues["EXIT"]
                            color = WHITE
                            if(value < 0):
                                color = RED
                                print(f"{BLUE}#{BLACK}____{color}{value:.2f}{BLACK}_____ ", end='')
                            else:
                                if(value > 0):
                                    color = GREEN
                                print(f"{BLUE}#{BLACK}_____{color}{value:.2f}{BLACK}_____ ", end='')
                        else:
                            print(f"{BLUE}#{BLACK}______________ ", end='')
                            
                    elif i%4 == 1:
                        value = self.grid[x][flippedY].qvalues["N"]
                        color = WHITE
                        if(round(value, 2) < 0):
                            color = RED
                            print(f"{BLUE}#{BLACK}____{color}{value:.2f}{BLACK}_____ ", end='')
                        else:
                            if(round(value, 2) > 0):
                                color = GREEN
                            print(f"{BLUE}#{BLACK}_____{color}{value:.2f}{BLACK}_____ ", end='')
                    elif i%4 == 2:
                        value1 = self.grid[x][flippedY].qvalues["W"]
                        value2 = self.grid[x][flippedY].qvalues["E"]
                        color1 = WHITE
                        if(round(value1, 2)  < 0):
                            color1 = RED
                            print(f"{BLUE}#{color1}{value1:.2f}", end='')
                        else:
                            if(round(value1, 2)  > 0):
                                color1 = GREEN
                            print(f"{BLUE}# {color1}{value1:.2f}", end='')
                        if(round(value2, 2)  < 0):
                            color2 = RED
                            print(f"{BLACK}____{color2}{value2:.2f}{BLACK} ",  end='')
                        else:
                            if(round(value2, 2)  > 0):
                                color2 = GREEN
                            print(f"{BLACK}_____{color2}{value2:.2f}{BLACK} ",  end='')
                    elif i%4 == 3:
                        value = self.grid[x][flippedY].qvalues["S"]
                        color = WHITE
                        if(value < 0):
                            color = RED
                            print(f"{BLUE}#{BLACK}____{color}{value:.2f}{BLACK}_____ ", end='')
                        else:
                            if(value > 0):
                                color = GREEN
                            print(f"{BLUE}#{BLACK}_____{color}{value:.2f}{BLACK}_____ ", end='')
                print(f"{BLUE}#")
    
        for x in range(self.width):
            print(f"{BLUE}################{WHITE}", end='')
        print('') #newline

    #toString function
    def __str__(self):
        result = ''
        for i in range(self.height):
            result += '['
            for j in range(self.width):
                result += str(self.grid[j][self.height-1 - i]) + ' '
            result += ']\n'

        return result
    
    #another toString function (idk its some python stuff)
    def __repr__(self):
        return "Grid"



#sets up the grid from a file
def setupGrid():
    fileName = "gridConf"
    if len(sys.argv) > 1:
        fileName = sys.argv[1]

    print(f"Solving puzzles in file: gridFiles/{fileName}.txt")
    try:
        filePath = "gridFiles/" + fileName + ".txt"
        file = open(filePath)
    except FileNotFoundError:
        print(f"Couldn't find file gridFiles/{fileName}.txt.... Please try again.")
        exit()


    ## START PARSING
    line = file.readline().split('=') # x=?
    x = int(line[1])
    line = file.readline().split('=') # y=?
    y = int(line[1])
    line = file.readline() # Terminal=?
    terminalString = line
    line = file.readline() # Boulder=?
    boulderString = line
    line = file.readline() # RobotStartState=?
    robotStartString = line
    line = file.readline().split('=') # K=?
    K = int(line[1])
    line = file.readline().split('=') # Episodes=?
    Episodes = int(line[1])
    line = file.readline().split('=') # Alpha=?
    alpha = float(line[1])
    line = file.readline().split('=') # discount=?
    discount = float(line[1])
    line = file.readline().split('=') # noise=?
    noise = float(line[1])
    line = file.readline().split('=') # transitionCost=?
    transitionCost = float(line[1])

    grid = [ [0]*y for i in range(x)]  ## create a grid of size x y filled with empty States

    for i in range(x):
        for j in range(y):
            grid[i][j] = State(transitionCost)

    #Set up terminals
    terminalString = terminalString[10:]
    terminalString = re.findall(r'(?<=\{)(.*?)(?=\})', terminalString)

    
    for s in terminalString:
        s = s.split(',')
        xPos = int(s[0])
        yPos = int(s[1])
        cost = int(s[2])
        grid[xPos][yPos] = Terminal(cost)

    #Set up boulders
    boulderString = boulderString[9:]
    boulderString = re.findall(r'(?<=\{)(.*?)(?=\})', boulderString)
    
    for s in boulderString:
        s = s.split(',')
        xPos = int(s[0])
        yPos = int(s[1])
        grid[xPos][yPos] = Boulder()

    #get the startState
    robotStartString = re.findall(r'(?<=\{)(.*?)(?=\})', robotStartString)
    startState = robotStartString[0].split(',')


    file.close()
    
    return Grid(grid, x, y, startState, K, Episodes, discount, noise)
