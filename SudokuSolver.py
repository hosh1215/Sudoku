from boards import board

def printBoard(status):
    print(status)
    for x in range(9):
        if x % 3 == 0:
            print("---------------------")
        for y in range(9):
            if y % 3 == 0:
                print("|",end="")
            print(board[x][y], end=" ")    
        print()
    print('===============================')

            
def validate(x,y,val):
    #Check x axis
    for i in range(9):
        if board[i][y] == val:
            return False
    #Check y axis
    for j in range(9):
        if board[x][j] == val:
            return False
    #Check local
    minX = x - x % 3
    minY = y - y % 3
    for i in range(3):
        for j in range(3):
            if board[minX+i][minY+j] == val:
                return False
    return True

def findValid(index):
    x = index // 9
    y = index % 9
    if index == 81:
        return True
    if board[x][y] > 0:
        return findValid(index + 1)
    for i in range(1,10):
        if validate(x,y,i):
            board[x][y] = i
            if findValid(index+1):
                return True
        board[x][y] = 0
    return False
    

if __name__ == '__main__':
    printBoard("Problem: ")
    findValid(0)
    printBoard("Solution: ")
