# use Python 3 to run main.py
import enum

class GridState(enum.Enum):
    EMPTY = 0,
    BLUE = 1,
    RED = 2

class Grid:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = None
        self.initGrid()
    
    def initGrid(self):
        self._grid = ([[GridState.EMPTY for _ in range(self._cols)]
                        for _ in range(self._rows)])
        
    def getGrid(self):
        return self._grid
    
    def getColumnCount(self):
        return self._cols
    
    def placePiece(self, column, piece):
        if column < 0 or column >= self._cols:
            raise ValueError('Invalid column')
        if piece == GridState.EMPTY:
            raise ValueError('Invaoid piece')
        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][column] == GridState.EMPTY:
                self._grid[row][column] = piece
                return row
    
    def checkWin(self, connectN, row, col, piece):
        count = 0
        # check horizontal
        for c in range(self._cols):
            if self._grid[row][c] == piece:
                # count will only continue to add up the all adjacent position all is same piece type 
                count += 1
            else:
                # when it is disconnected and do not reach connectN num, reset count to 0
                count = 0 
            if count == connectN:
                return True
        # check vertical
        for r in range(self._rows):
            if self._grid[r][col] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        # check diagonal
        for r in range(self._rows):
            c = row + col - r
            if c >= 0 and c < self._cols and self._grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        # check anti-diagonal
        for r in range(self._rows):
            c = col - row + r
            if c >= 0 and c < self._cols and self._grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True

        return False

class Player:
    def __init__(self, name, pieceColor):
        self._name = name
        self._pieceColor = pieceColor
    def getName(self):
        return self._name
    def getPieceColor(self):
        return self._pieceColor

class Game:
    def __init__(self, grid, connectN, targetScore):
        self._grid = grid
        self._connectN = connectN
        self._targetScore = targetScore

        self._players = [
            Player('Player 1', GridState.BLUE),
            Player('Player 2', GridState.RED)
        ]

        self._score = {}
        for player in self._players:
            self._score[player.getName()] = 0

    def printBoard(self):
        print('Board:\n')
        grid = self._grid.getGrid()
        for i in range(len(grid)):
            row = ''
            for piece in grid[i]:
                if piece == GridState.EMPTY:
                    row += '0 '
                elif piece == GridState.YELLOW:
                    row += 'Y '
                elif piece == GridState.RED:
                    row += 'R '
            print(row)
        print('')

    def playMove(self, player):
        self.printBoard()
        print(f"{player.getName()}'s turn")
        colCnt = self._grid.getColumnCount()
        moveColumn = int(input(f"Enter column between {0} and {colCnt - 1} to add piece: "))
        moveRow = self._grid.placePiece(moveColumn, player.getPieceColor())
        return (moveRow, moveColumn)

    def playRound(self):
        while True:
            for player in self._players:
                row, col = self.playMove(player)
                pieceColor = player.getPieceColor()
                if self._grid.checkWin(self._connectN, row, col, pieceColor):
                    self._score[player.getName()] += 1
                    return player

    def play(self):
        maxScore = 0
        winner = None
        while maxScore < self._targetScore:
            winner = self.playRound()
            print(f"{winner.getName()} won the round")
            maxScore = max(self._score[winner.getName()], maxScore)

            self._grid.initGrid() # reset grid
        print(f"{winner.getName()} won the game")

grid = Grid(6, 7)
game = Game(grid, 4, 1)
game.play()