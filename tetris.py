from cmu_112_graphics import *
import random

def gameDimensions():
    rows,cols,cellsize,margin = 15,10,20,25
    return (rows,cols,cellsize,margin)

def piecesCreate():
     # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                          "cyan", "green", "orange" ]
    return tetrisPieces, tetrisPieceColors

def newFallingPiece(app):
    app.tetrisPieces, app.tetrisPieceColors = piecesCreate()
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.piece = app.tetrisPieces[randomIndex]
    app.color = app.tetrisPieceColors[randomIndex]
    app.initialrow = 0
    app.initialcol = (app.cols-1)/2

def appStarted(app):
    (app.rows,app.cols,app.cellsize,app.margin) = gameDimensions()
    app.emptyColor = "blue"
    app.board = [([app.emptyColor]*app.cols) for row in range(app.rows)]
    # stores the new peice and color 
    newFallingPiece(app) # app.piece, app.color, intial row, col
    app.timerDelay = 300
    app.GameOver = False 
    app.score = 0 

def moveFallingPiece(app,drow,dcol):
    # get new step 
    newrow = app.initialrow + drow
    newcol = app.initialcol + dcol
    # check if step is legal
    if fallingPiecesLegal(app.board,app.piece,app.initialrow,
    app.initialcol,app.emptyColor):
        newrow = app.initialrow + drow
        newcol = app.initialcol + dcol
        if fallingPiecesLegal(app.board,app.piece,newrow,newcol,app.emptyColor):
            return True
    return False

def placeFallingPiece(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col] == True:
                #print("ap")
                currow = row + app.initialrow
                curcol = col + int(app.initialcol-0.5)
                curcolor = app.color
                if len(app.piece) == 1:
                    curcol -= 1 
                if (currow == app.rows-1) or (curcolor != app.emptyColor):
                    # place the piece on board
                    if not app.GameOver:
                        app.board[currow][curcol] = app.color
def isGameOver(app):
    for col in range(app.cols):
        if app.board[0][col] != app.emptyColor:
            app.GameOver = True 

def isFull(L,row,color):
    for col in range(len(L[0])):
        if L[row][col] == color:
            return False
    return True 


def removeFullRow(app):
    newlist = [app.emptyColor]*app.cols
    numrow = 0 
    for row in range(app.rows):
        if isFull(app.board,row,app.emptyColor):
            numrow +=1 
            app.board.pop(row)
            app.board.insert(0,newlist)
    app.score += numrow**2

def timerFired(app):
    if not app.GameOver:
        drow = 1
        dcol = 0 
        if moveFallingPiece(app,drow,dcol):
            app.initialrow += drow
            app.initialcol += dcol
        elif not moveFallingPiece(app,drow,dcol):
            placeFallingPiece(app)
            isGameOver(app)
            if not app.GameOver:
                newFallingPiece(app)
        removeFullRow(app)

def fallingPiecesLegal(board,piece,initialrow,initialcol,empty):
    rows = len(board)-1
    cols = len(board[0])-1
    if len(piece) == 1:
        initialcol -=1
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col] == True:
                currow = row + initialrow
                curcol = col + int(initialcol-0.5)
                if not ((0 <= currow <= rows) and (0 <= curcol <= cols)):
                    return False
                if (board[currow][curcol] != empty):
                    return False
    return True
    
def rotatecounter90(piece):
    newcol = len(piece)
    newrow = len(piece[0])
    rows = []
    result = [[None] for row in range(newrow)]
    for col in range(len(piece[0])):
        for row in range(len(piece)):
            rows.append(piece[row][col])
        result[newrow-col-1] = rows
        rows = list() 
    return result

def keyPressed(app,event):
    if event.key == "r":
        appStarted(app)
    if not app.GameOver:
        if event.key == "Left":
            drow = 0
            dcol = -1
            if moveFallingPiece(app,drow,dcol):
                app.initialrow += drow
                app.initialcol += dcol
        elif event.key == "Space":
            drow = 1
            dcol = 0 
            if moveFallingPiece(app,drow,dcol):
                app.initialrow += drow
        elif event.key == "Right":
            drow = 0
            dcol = 1
            if moveFallingPiece(app,drow,dcol):
                app.initialrow += drow
                app.initialcol += dcol
        elif event.key == "Up":
            drow = 1
            dcol = 0
            if moveFallingPiece(app,drow,dcol):
                new = rotatecounter90(app.piece)
                if fallingPiecesLegal(app.board,new,app.initialrow,app.initialcol,
                app.emptyColor):
                    app.piece = new
    

def drawBoard(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app,canvas,row,col)

def getCellBound(app,row,col):
    x1,y1 = app.margin+col*app.cellsize, app.margin+row*app.cellsize
    x2,y2 = x1 + app.cellsize, y1 +app.cellsize
    return x1,y1,x2,y2


# center the location getting rid of black margins
def addingside(app,x1,y1,x2,y2):
    x1,y1 = x1+0.05*app.cellsize,y1+0.05*app.cellsize
    x2,y2 = x2-0.05*app.cellsize,y2-0.05*app.cellsize
    return x1,y1,x2,y2

def drawCell(app,canvas,row,col):
    color = app.board[row][col]
    x1,y1,x2,y2 = getCellBound(app,row,col)
    canvas.create_rectangle(x1,y1,x2,y2,fill = "black")
    x1,y1,x2,y2 = addingside(app,x1,y1,x2,y2)
    canvas.create_rectangle(x1,y1,x2,y2,fill = color)

def drawPiece(app,canvas):
    rows = len(app.piece)
    cols = len(app.piece[0])
    # iterate each chose cell
    for row in range(rows):
        for col in range(cols):
            # only draw it if the element is True 
            if app.piece[row][col] == True:
                color = app.color
                # if column number is even 
                if cols %2 != 0 or cols == 2 and app.cols %2 == 0:
                    x1,y1,x2,y2 = getCellBound(app,row+app.initialrow,
                                            col+app.initialcol)
                elif cols%2 == 0 and cols != 2 and app.cols %2 == 0:
                    x1,y1,x2,y2 = getCellBound(app,row+app.initialrow,
                            col+app.initialcol-1)
                # if column number is odd
                elif cols %2 != 0 or cols == 2 and app.cols %2 != 0:
                    x1,y1,x2,y2 = getCellBound(app,row+app.initialrow,
                                            col+app.initialcol-1)
                elif cols %2 != 0 or cols == 2 and app.cols %2 == 0:
                    x1,y1,x2,y2 = getCellBound(app,row+app.initialrow,
                                            col+app.initialcol)
                # row correction
                x1,x2 = x1-0.5*app.cellsize, x2 - 0.5*app.cellsize
                # adding black margins
                x1,y1,x2,y2 = addingside(app,x1,y1,x2,y2)
                # draw the piece 
                canvas.create_rectangle(x1,y1,x2,y2,fill = color)

def drawOverMessage(app,canvas):
    text = "Game Over"
    # draw the background 
    startrow = 1
    endrow = 4
    startcol = 0
    endcol = app.cols
    for row in range(startrow,endrow+1):
        for col in range(startcol,endcol):
            x1,y1,x2,y2 = getCellBound(app,row,col)
            canvas.create_rectangle(x1,y1,x2,y2,fill = "black")
    # draw the text 
    cx = app.width/2 
    cy = app.margin + (endrow-startrow)*app.cellsize
    canvas.create_text(cx,cy,text = text, fill = "yellow",
    font = "Arial 25 bold")

def drawScore(app,canvas):
    cx = app.width/2
    cy = app.margin/2
    text = f"Score:  {app.score}" 
    canvas.create_text(cx,cy,text= text,font = "Arial 15 bold")

def redrawAll(app,canvas):
    # fill back ground 
    canvas.create_rectangle(0,0,app.width,app.height,fill = "orange")
    # drawboard
    drawBoard(app,canvas)
    drawPiece(app,canvas)
    drawScore(app,canvas)
    if app.GameOver:
        drawOverMessage(app,canvas)
    


def playTetris():
    (rows,cols,cellsize,margin) = gameDimensions()
    width = cols*cellsize + 2*margin
    height = rows*cellsize + 2*margin
    runApp(width = width,height = height)

def main():
    playTetris()
main()