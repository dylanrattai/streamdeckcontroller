#button bools
grid0 = false
grid1 = false
grid2 = false
column0 = false
column1 = false
column2 = false
row0 = false
row1 = false
row2 = false
setTgt = false
markGrid = false
removeMark = false
markPlaced = false
fellLow = false
resetTgt = false

#targeting ints (perspective in comments = looking at grid from field NOT DRIVER STATION)
grid = None #0 = left outer grid, 3 = co-op grid, 6 = right outer grid
column = None #0 = leftmost column, 1 = middle column, 2 = rightmost column
row = None #0 = lowest row, 1 = middle row, 2 = highest row
selectedNode = [None, None] #use to hold pose in only columns and rows
tgt = [None, None] #Column, Row

def setTgtInts():
  if(grid0):
    grid = 0
  elif(grid1):
    grid = 3
  elif(grid2):
    grid = 6
  if(column0):
    column = 0
  elif(column1):
    column = 1
  elif(column2):
    column = 2
  if(row0):
    row = 0
  elif(row1):
    row = 1
  elif(row2):
    row = 2
  selectedNode = [grid + column, row]

def setTgt():
  try:
    tgt = [grid + column, row]
  except:
    return None

def updateNetworktable():
  #send target node to table
  #send commands to networktable
  
while true:
  updateNetworktable()
  setTgtInts()
