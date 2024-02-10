from tkinter import Canvas
from Piece import *

class BoardState:
    def __init__(self, canvas, boardGraphic) -> None:
        self.boardGraphic = boardGraphic
        self.canvas: Canvas = canvas
        self.clickPosition = None
        # sizes
        self.sqrSize = self.boardGraphic.sqrSize
        self.labelSize = self.boardGraphic.labelSize
        self.offset = self.boardGraphic.offset
        # state variables
        self.isPicking = True
        self.turn = "W"
        self.takenPieces = {
            "W": [],
            "B": []
        }
        # objects into board
        self.boardList = self.initBoard()
        self.positions = self.createPositions()
        

    def initBoard(self) -> list[list[Piece]]: 
       return [[Rook("B"), Knight("B"), Bishop("B"), Queen("B"), King("B"), Bishop("B"), Knight("B"), Rook("B")],
               [Pawn("B"), Pawn("B"), Pawn("B"), Pawn("B"), Pawn("B"), Pawn("B"), Pawn("B"), Pawn("B")],
               [None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None],
               [None, None, None, None, None, None, None, None],
               [Pawn("W"), Pawn("W"), Pawn("W"), Pawn("W"), Pawn("W"), Pawn("W"), Pawn("W"), Pawn("W")],
               [Rook("W"), Knight("W"), Bishop("W"), Queen("W"), King("W"), Bishop("W"), Knight("W"), Rook("W")]]
    
    def createPositions(self):
        positions = []
        for row in range(8):
            for column in range(8):
                positions.append((row * self.sqrSize + self.offset, column * self.sqrSize + self.offset, 
                                 row * self.sqrSize + self.offset + self.sqrSize, column * self.sqrSize + self.offset + self.sqrSize,
                                 (column, row)))
        return positions
    
    def handleClick(self, event):
        column = event.x
        row = event.y
        
        for x1, y1, x2, y2, pos in self.positions:
            if ((column > x1 and column < x2)
                and (row > y1 and row < y2)):
                self.handleSquare(pos[0], pos[1], x1, y1)

    def showTaken(self):
        bRowCounter = -1
        for i, piece in enumerate(self.takenPieces["B"]):
            if (isinstance(piece, King)):
                self.endGame("W")
            if i % 7 == 0:
                bRowCounter += 1
            self.canvas.coords(piece.imgId, 
                               self.boardGraphic.boardSize + self.sqrSize * 1.2 + (i%7) * (self.sqrSize - self.sqrSize * 0.35),
                               self.sqrSize//0.8 + bRowCounter * self.sqrSize)
        wRowCounter = -1
        for j, piece in enumerate(self.takenPieces["W"]):
            if (isinstance(piece, King)):
                self.endGame("B")
            if j % 7 == 0:
                wRowCounter += 1
            self.canvas.coords(piece.imgId, 
                               self.boardGraphic.boardSize + self.sqrSize * 1.2 + (j%7) * (self.sqrSize - self.sqrSize * 0.35), 
                               self.sqrSize * 7.5 - wRowCounter * self.sqrSize)


    def setTurn(self):
        if (self.turn == "W"):
            self.turn = "B"
        else:
            self.turn = "W"
        # set player 
        if (self.turn == "W"):
            self.canvas.itemconfig(tagOrId="white", fill=self.boardGraphic.whiteStats, font=("Verdana", self.labelSize, "bold"))
            self.canvas.itemconfig(tagOrId="black", fill=self.boardGraphic.black, font=("Verdana", self.labelSize))
        else:
            self.canvas.itemconfig(tagOrId="black", fill=self.boardGraphic.black, font=("Verdana", self.labelSize, "bold"))
            self.canvas.itemconfig(tagOrId="white", fill=self.boardGraphic.whiteStats, font=("Verdana", self.labelSize))
        
    def handleSquare(self, row, column, x, y):
        if (self.isPicking):
            self.piece: Piece = self.boardList[row][column]
            # pick only a piece with desired color
            if (self.boardList[row][column] is None or self.piece.color != self.turn):
                return
            self.clickPosition = (row, column)
            #lights on
            self.validSqr = self.piece.validMoves(row, column, self.boardList)
            self.boardGraphic.lightsOn(self.validSqr)
            self.isPicking = False
            
        else:
            newPiece = self.boardList[row][column]
            if (self.clickPosition is None):
                return
            # when clicked twice on same piece, do nothing
            if (row == self.clickPosition[0] and column == self.clickPosition[1]):
                return
            # pick another piece in the same turn
            if (newPiece is not None and newPiece.color == self.turn):  
                self.boardGraphic.lightsOff(self.validSqr)
                self.isPicking = True
                self.handleSquare(row, column, x, y)

            # Move the piece
            if (self.boardList[self.clickPosition[0]][self.clickPosition[1]] is not None):
                if ((row, column) in self.validSqr):
                    # take a piece
                    if (newPiece is not None and newPiece.color != self.turn):
                        self.takenPieces[newPiece.color].append(newPiece)
                        self.showTaken()
                    #move
                    self.boardList[row][column] = self.boardList[self.clickPosition[0]][self.clickPosition[1]]
                    self.boardList[self.clickPosition[0]][self.clickPosition[1]] = None
                    self.canvas.coords(self.piece.imgId, x + self.sqrSize//2, y + self.sqrSize//2)
                    # lights off
                    self.boardGraphic.lightsOff(self.validSqr)
                    self.isPicking = True
                    self.clickPosition = None
                    self.setTurn()

    def endGame(self):
        self.btn = ImageTk.PhotoImage(file="./img/button_play-again.png")
        self.playAgain = tkinter.Button(self.boardGraphic.root, image=self.btn, border=0, command=self.boardGraphic.setNewGame)
        self.playAgain.place(x=self.boardGraphic.boardSize + self.boardGraphic.boardSize//4, 
                             y= self.boardGraphic.boardSize//2 + self.offset)

            


    
    
