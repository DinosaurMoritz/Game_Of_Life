import time
from consoleScreen import ConsoleScreen


class Game:
    def __init__(self, inputBoard=[], focusPoint=(0,0)):
        
        self.board = inputBoard
        self.newBoard = []
        
        self.screen = GameDisplay(focusPoint)
        
        self.generationCounter = 0
        
    def checkCellState(self, cell, firstRound=True):
        x,y = cell
        aliveNeighbourCounter = 0
        
        neighbours = [(x,y-1),(x-1,y),(x,y+1),(x+1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]
        
        for n in neighbours:
            if n in self.board:
                aliveNeighbourCounter = aliveNeighbourCounter + 1
                
            if firstRound:
                self.checkCellState(n, False)
                
        if cell in self.board:
            if aliveNeighbourCounter in (2, 3) and cell not in self.newBoard:
                self.newBoard.append(cell)
        else:
            if aliveNeighbourCounter == 3 and cell not in self.newBoard:
                self.newBoard.append(cell)
             
        
    def tick(self, displayAfterTick=True):
        startTime = time.time()
        
        for cell in self.board:
            self.checkCellState(cell)
        
        self.board = self.newBoard
        self.newBoard = []
        
        if displayAfterTick:
            self.display()
           
        self.generationCounter = self.generationCounter + 1 
        return f"Tick took {time.time()-startTime}s to run the {self.generationCounter}th generation!"
    
    def run(self, ticks=0, timeDelay=0):
        t1 = time.time()
        
        if ticks:
            for n in range(ticks):
                print(self.tick(True))
                time.sleep(timeDelay/1000)
        else:
            while True:
                print(self.tick(True))
                time.sleep(timeDelay/1000)
        
        print(f"Execution of run took {time.time()-t1}s!")
                
    def printBoard(self):
        print(self.board)
    
    def display(self):
        self.screen.display(self.board)
        print()
    


class GameDisplay:
    def __init__(self, focusPoint=(0,0), size=(70,50)):
        self.halfSizeX, self.halfSizeY = size[0]/2, size[1]/2
        self.screen = ConsoleScreen(size)
        self.focusPoint = focusPoint
        self.focusX, self.focusY = self.focusPoint
        
    def display(self, board):
        for i, cell in enumerate(board):
            cell =  cell[0] - self.focusX + self.halfSizeX, cell[1] - self.focusY + self.halfSizeY
            self.screen.drawPixel(cell)
            #print(cell)
        
        #input()
        self.screen.clearScreen()
        self.screen.display()
        self.screen.clearField()
        
        
if __name__ == "__main__":
    game = Game([(0,0),(0,1),(-1,0),(0,-1),(1,-1)]) #[(0,0), (1,1),(2,1),(2,0),(2,-1)], (50,50))
    game.run(100, 0)
    