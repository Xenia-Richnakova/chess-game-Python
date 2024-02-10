import tkinter
from PIL import Image, ImageTk

class Piece:
    def __init__(self, color) -> None:
        self.color = color
        self.imgId = None
        self.hasMoved = False

    def pieceImg(self, imgSize):
        img = Image.open(self.path)
        img = img.resize((imgSize, imgSize))
        # need to use self here so Python will not just throw it away
        self.pieceImage = ImageTk.PhotoImage(img)
        return self.pieceImage
    
    def checkRange(self, row, column):
        # prevent getting out of range error
        if (row > 7 or row < 0):
            return False
        if (column > 7 or column < 0):
            return False
        return True

    def canMove(self, row, column, boardList):
        if (self.checkRange(row, column)):
            if (boardList[row][column] is None):
                return True
            if (boardList[row][column].color != self.color):
                return True
            else:
                return False
        else:
            return False

class Pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.path = f"./img/pawn{color}.png"

    def validMoves(self, row, column, boardList) -> list[(int, int)]:
        res = []
        if self.color == "W":
            if boardList[row - 1][column] is None:
                res.append((row - 1, column))
            if ((column - 1 > 0 and boardList[row - 1][column - 1] is not None) and 
                boardList[row - 1][column - 1].color != self.color):
                res.append((row - 1, column - 1))
            if ((column + 1 < 8 and boardList[row - 1][column + 1] is not None) and
                boardList[row - 1][column + 1].color != self.color):
                res.append((row - 1, column + 1))
            if (self.hasMoved == False and 
                (boardList[row - 1][column] is None and boardList[row - 2][column] is None)):
                res.append((row - 2, column))
        else:
            if boardList[row + 1][column] is None:
                res.append((row + 1, column))
            if ((column - 1 > 0 and boardList[row + 1][column - 1] is not None) and 
                boardList[row + 1][column - 1].color != self.color):
                res.append((row + 1, column - 1))
            if ((column + 1 < 8 and boardList[row + 1][column + 1] is not None) and 
                boardList[row + 1][column + 1].color != self.color):
                res.append((row + 1, column + 1))
            if (self.hasMoved == False and 
                (boardList[row + 1][column] is None and boardList[row + 2][column] is None)):
                res.append((row + 2, column))
        return res


class Rook(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.path = f"./img/rook{color}.png"

    # possibilities 
    def validMoves(self, row, column, boardList) -> list[(int, int)]: 
        res = []
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for x, y in directions:
            for i in range(1,8):
                newRow = row + (i * x)
                newCol = column + (i * y)
                if (self.canMove(newRow, newCol, boardList)):
                    res.append((newRow, newCol))
                    if (boardList[newRow][newCol] is not None and
                        boardList[newRow][newCol].color != self.color):
                        break
                else:
                    break
        return res

class Knight(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.path = f"./img/knight{color}.png"
    
    def validMoves(self, row, column, boardList) -> list[(int, int)]: 
        res = []
        directions = [(1, -2), (-1, -2), (2, -1), (-2, -1), (-1, 2), (1, 2), (2, 1), (-2, 1)]
        for x, y in directions:
            if (self.canMove(row + x, column + y, boardList)):
                res.append((row + x, column + y))
        return res


class Bishop(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.path = f"./img/bishop{color}.png"

    def validMoves(self, row, column, boardList) -> list[(int, int)]: 
        res = []
        directions = [(1, -1), (-1, -1), (-1, 1), (1, 1)]
        for x, y in directions:
            for i in range(1,8):
                newRow = row + (i * x)
                newCol = column + (i * y)
                if (self.canMove(newRow, newCol, boardList)):
                    res.append((newRow, newCol))
                    if (boardList[newRow][newCol] is not None and
                        boardList[newRow][newCol].color != self.color):
                        break
                else:
                    break
        return res

class King(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.path = f"./img/king{color}.png"
    
    def validMoves(self, row, column, boardList) -> list[(int, int)]: 
        res = []
        directions = [(1, -1), (-1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)]
        for x, y in directions:
            if (self.canMove(row + x, column + y, boardList)):
                res.append((row + x, column + y))
        return res

class Queen(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.path = f"./img/queen{color}.png"

    def validMoves(self, row, column, boardList) -> list[(int, int)]: 
        res = []
        directions = [(1, -1), (-1, -1), (-1, 1), (1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)]
        for x, y in directions:
            for i in range(1,8):
                newRow = row + (i * x)
                newCol = column + (i * y)
                if (self.canMove(newRow, newCol, boardList)):
                    res.append((newRow, newCol))
                    if (boardList[newRow][newCol] is not None and
                        boardList[newRow][newCol].color != self.color):
                        break
                else:
                    break
        return res



