import pygame

def delete_in_row(sudoku, sudoku_state, row, num):
    for col in range(9):
        if sudoku_state[row][col] == "N":

            sudoku[row][col][(num - 1) // 3][(num - 1) % 3] = 0
    return sudoku, sudoku_state


def delete_in_col(sudoku, sudoku_state, col, num):
    for row in range(9):
        if sudoku_state[row][col] == "N":
            sudoku[row][col][(num - 1) // 3][(num - 1) % 3] = 0
    return sudoku, sudoku_state


def delete_in_square(sudoku, sudoku_state, row, col, num):
    for roww in range((row // 3) * 3, (row // 3) * 3 + 3):
        for coll in range((col // 3) * 3, (col // 3) * 3 + 3):
            if sudoku_state[roww][coll] == "N":
                sudoku[roww][coll][(num - 1) // 3][(num - 1) % 3] = 0
    return sudoku, sudoku_state


def naked_single(sudoku, sudoku_state, row, col):
    flag = False
    num = 0
    count = 0
    for i in range(3):
        for j in range(3):
            if sudoku[row][col][i][j] == 0:
                count += 1
    if count == 8:
        flag = True
        brk = False
        for i in range(3):
            for j in range(3):
                if sudoku[row][col][i][j] != 0:
                    num = sudoku[row][col][i][j]
                    sudoku[row][col] = str(num)
                    sudoku_state[row][col] = "F"
                    brk = True
                    break
            if brk:
                break

        sudoku, sudoku_state = delete_in_row(sudoku,sudoku_state, row, num)
        sudoku, sudoku_state = delete_in_col(sudoku,sudoku_state, col, num)
        sudoku, sudoku_state = delete_in_square(sudoku, sudoku_state, row, col, num)

    return sudoku, sudoku_state, flag


def state0(sudoku, sudoku_state):
    while True:
        flag = False
        for row in range(9):
            for col in range(9):
                f = False
                if sudoku_state[row][col] == "N":
                    sudoku, sudoku_state, f = naked_single(sudoku, sudoku_state, row, col)
                if f:
                    flag = True
        if not flag:
            break
    return sudoku, sudoku_state


def hidden_single_check_row(sudoku, sudoku_state):
    f = False
    for row in range(9):
        count = [0] * 9
        col_num = [-1] * 9
        for col in range(9):
            for r in range(3):
                for c in range(3):
                    if sudoku_state[row][col] == "N" and sudoku[row][col][r][c] != 0:
                        count[r*3+c] += 1
                        col_num[r*3+c] = col
        for num in range(len(count)):
            if count[num] == 1:
                f = True
                sudoku[row][col_num[num]] = str(num+1)
                sudoku_state[row][col_num[num]] = "F"
                sudoku, sudoku_state = delete_in_row(sudoku, sudoku_state, row, num+1)
                sudoku, sudoku_state = delete_in_col(sudoku, sudoku_state, col_num[num], num+1)
                sudoku, sudoku_state = delete_in_square(sudoku, sudoku_state, row, col_num[num], num+1)
    return sudoku, sudoku_state, f


def hidden_single_check_col(sudoku, sudoku_state):
    f = False
    for col in range(9):
        count = [0] * 9
        row_num = [-1] * 9
        for row in range(9):
            for r in range(3):
                for c in range(3):
                    if sudoku_state[row][col] == "N" and sudoku[row][col][r][c] != 0:
                        count[r * 3 + c] += 1
                        row_num[r * 3 + c] = row
        for num in range(len(count)):
            if count[num] == 1:
                f = True
                sudoku[row_num[num]][col] = str(num+1)
                sudoku_state[row_num[num]][col] = "F"
                sudoku, sudoku_state = delete_in_row(sudoku, sudoku_state, row_num[num], num+1)
                sudoku, sudoku_state = delete_in_col(sudoku, sudoku_state, col, num+1)
                sudoku, sudoku_state = delete_in_square(sudoku, sudoku_state, row_num[num], col, num+1)
    return sudoku, sudoku_state, f


def hidden_single_check_square(sudoku, sudoku_state):
    f = False
    for square in range(9):
        count = [0] * 9
        row_num = [-1] * 9
        col_num = [-1] * 9
        for row in range((square//3)*3, (square//3)*3+3):
            for col in range((square%3)*3, (square%3)*3+3):
                for r in range(3):
                    for c in range(3):
                        if sudoku_state[row][col] == "N" and sudoku[row][col][r][c] != 0:
                            count[r * 3 + c] += 1
                            row_num[r * 3 + c] = row
                            col_num[r * 3 + c] = col
        for num in range(len(count)):
            if count[num] == 1:
                f = True
                sudoku[row_num[num]][col_num[num]] = str(num+1)
                sudoku_state[row_num[num]][col_num[num]] = "F"
                sudoku, sudoku_state = delete_in_row(sudoku, sudoku_state, row_num[num], num+1)
                sudoku, sudoku_state = delete_in_col(sudoku, sudoku_state, col_num[num], num+1)
                sudoku, sudoku_state = delete_in_square(sudoku, sudoku_state, row_num[num], col_num[num], num+1)
    return sudoku, sudoku_state, f


def hidden_single(sudoku, sudoku_state):
    while True:

        sudoku, sudoku_state, f1 = hidden_single_check_row(sudoku, sudoku_state)
        sudoku, sudoku_state, f2 = hidden_single_check_col(sudoku, sudoku_state)
        sudoku, sudoku_state, f3 = hidden_single_check_square(sudoku, sudoku_state)
        if not f1 and not f2 and not f3:
            break
    return sudoku, sudoku_state


def state1(sudoku, sudoku_state):
    while True:
        sudoku1, sudoku_state1 = hidden_single(sudoku, sudoku_state)
        sudoku2, sudoku_state2 = state0(sudoku1, sudoku_state1)
        if sudoku == sudoku2:
            sudoku = sudoku2
            sudoku_state = sudoku_state2
            break
        sudoku = sudoku2
        sudoku_state = sudoku_state2
    return sudoku, sudoku_state


def naked_pair_check_row(sudoku, sudoku_state):
    for i in range(9):
        two_member_list = []
        two_member_list_col = []
        for j in range(9):
            zero_count = 0
            for r in range(3):
                for c in range(3):
                    if sudoku_state[i][j] == "N" and sudoku[i][j][r][c] == 0:
                        zero_count += 1
            if zero_count == 7:
                tmpi = []
                for a in range(3):
                    tmp = []
                    for b in range(3):
                        tmp.append(sudoku[i][j][a][b])
                    tmpi.append(tmp)
                two_member_list.append(tmpi)
                two_member_list_col.append(j)
        for k in range(len(two_member_list)):
            for l in range(k+1, len(two_member_list)):
                if two_member_list[k] == two_member_list[l]:
                    for r in range(3):
                        for c in range(3):
                            if two_member_list[k][r][c] != 0:
                                num = two_member_list[k][r][c]
                                sudoku, sudoku_state = delete_in_row(sudoku, sudoku_state, i, num)
                sudoku[i][two_member_list_col[k]] = two_member_list[k]
                sudoku[i][two_member_list_col[l]] = two_member_list[l]
                continue
    return sudoku


def naked_pair_check_col(sudoku, sudoku_state):
    for j in range(9):
        two_member_list = []
        two_member_list_row = []
        for i in range(9):
            zero_count = 0
            for r in range(3):
                for c in range(3):
                    if sudoku_state[i][j] == "N" and sudoku[i][j][r][c] == 0:
                        zero_count += 1
            if zero_count == 7:
                tmpi = []
                for a in range(3):
                    tmp = []
                    for b in range(3):
                        tmp.append(sudoku[i][j][a][b])
                    tmpi.append(tmp)
                two_member_list.append(tmpi)
                two_member_list_row.append(i)
        for k in range(len(two_member_list)):
            for l in range(k+1, len(two_member_list)):
                if two_member_list[k] == two_member_list[l]:
                    for r in range(3):
                        for c in range(3):
                            if two_member_list[k][r][c] != 0:
                                num = two_member_list[k][r][c]
                                sudoku, sudoku_state = delete_in_col(sudoku, sudoku_state, j, num)

                sudoku[two_member_list_row[k]][j] = two_member_list[k]
                sudoku[two_member_list_row[l]][j] = two_member_list[l]
                continue
    return sudoku


def naked_pair_check_square(sudoku, sudoku_state):
    for square in range(9):
        two_member_list = []
        two_member_list_row = []
        two_member_list_col = []
        for i in range((square//3)*3, (square//3)*3+3):
            for j in range((square%3)*3, (square%3)*3+3):
                zero_count = 0
                for r in range(3):
                    for c in range(3):
                        if sudoku_state[i][j] == "N" and sudoku[i][j][r][c] == 0:
                            zero_count += 1
                if zero_count == 7:
                    tmpi = []
                    for a in range(3):
                        tmp = []
                        for b in range(3):
                            tmp.append(sudoku[i][j][a][b])
                        tmpi.append(tmp)
                    two_member_list.append(tmpi)
                    two_member_list_row.append(i)
                    two_member_list_col.append(j)
        for k in range(len(two_member_list)):
            for l in range(k+1,len(two_member_list)):
                if two_member_list[k] == two_member_list[l]:
                    for r in range(3):
                        for c in range(3):
                            if two_member_list[k][r][c] != 0:
                                num = two_member_list[k][r][c]
                                sudoku, sudoku_state = delete_in_square(sudoku, sudoku_state, two_member_list_row[k], two_member_list_col[k], num)
                sudoku[two_member_list_row[k]][two_member_list_col[k]] = two_member_list[k]
                sudoku[two_member_list_row[l]][two_member_list_col[l]] = two_member_list[l]
                continue
    return sudoku


def naked_pair(sudoku, sudoku_state):
    while True:
        f1, f2, f3 = False, False, False
        sudoku1 = naked_pair_check_row(sudoku, sudoku_state)
        if sudoku == sudoku1:
            f1 = True
        sudoku = sudoku1
        sudoku2 = naked_pair_check_col(sudoku, sudoku_state)
        if sudoku == sudoku2:
            f2 = True
        sudoku = sudoku2
        sudoku3 = naked_pair_check_square(sudoku, sudoku_state)
        if sudoku == sudoku3:
            f3 = True
        sudoku = sudoku3
        if f1 and f2 and f3:
            break
    return sudoku, sudoku_state


def state2(sudoku, sudoku_state):
    while True:
        sudoku1, sudoku_state1 = naked_pair(sudoku, sudoku_state)
        sudoku2, sudoku_state2 = state1(sudoku1, sudoku_state1)
        if sudoku2 == sudoku:
            sudoku = sudoku2
            sudoku_state = sudoku_state2
            break
        sudoku = sudoku2
        sudoku_state = sudoku_state2
    return sudoku, sudoku_state


def hidden_pair_row(sudoku, sudoku_state):
    for row in range(9):
        count_of_numbers = [0]*9
        col_of_numbers = []
        for a in range(9):
            col_of_numbers.append([])
        for col in range(9):
            if sudoku_state[row][col] == "N":
                for r in range(3):
                    for c in range(3):
                        if sudoku[row][col][r][c] != 0:
                            count_of_numbers[sudoku[row][col][r][c]-1] += 1
                            col_of_numbers[sudoku[row][col][r][c]-1].append(col)
        numbers = []
        cols = []
        for i in range(9):
            if count_of_numbers[i] == 2:
                numbers.append(i+1)
                cols.append(col_of_numbers[i])
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                if cols[i][0] == cols[j][0] and cols[i][1] == cols[j][1]:
                    nums_array = []
                    for x in range(3):
                        tmp = []
                        for y in range(3):
                            tmp.append(0)
                        nums_array.append(tmp)
                    nums_array[(numbers[i]-1)//3][(numbers[i]-1)%3] = numbers[i]
                    nums_array[(numbers[j]-1)//3][(numbers[j]-1)%3] = numbers[j]
                    sudoku[row][cols[i][0]] = nums_array
                    sudoku[row][cols[i][1]] = nums_array
    return sudoku, sudoku_state


def hidden_pair_col(sudoku, sudoku_state):
    for col in range(9):
        count_of_numbers = [0]*9
        row_of_numbers = []
        for a in range(9):
            row_of_numbers.append([])
        for row in range(9):
            if sudoku_state[row][col] == "N":
                for r in range(3):
                    for c in range(3):
                        if sudoku[row][col][r][c] != 0:
                            count_of_numbers[sudoku[row][col][r][c]-1] += 1
                            row_of_numbers[sudoku[row][col][r][c]-1].append(row)
        numbers = []
        rows = []
        for i in range(9):
            if count_of_numbers[i] == 2:
                numbers.append(i+1)
                rows.append(row_of_numbers[i])
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                if rows[i][0] == rows[j][0] and rows[i][1] == rows[j][1]:
                    nums_array = []
                    for x in range(3):
                        tmp = []
                        for y in range(3):
                            tmp.append(0)
                        nums_array.append(tmp)
                    nums_array[(numbers[i] - 1) // 3][(numbers[i] - 1) % 3] = numbers[i]
                    nums_array[(numbers[j] - 1) // 3][(numbers[j] - 1) % 3] = numbers[j]
                    sudoku[rows[i][0]][col] = nums_array
                    sudoku[rows[i][1]][col] = nums_array
    return sudoku, sudoku_state


def hidden_pair_square(sudoku, sudoku_state):
    for square in range(9):
        count_of_numbers = [0] * 9
        row_of_numbers = []
        for a in range(9):
            row_of_numbers.append([])
        col_of_numbers = []
        for b in range(9):
            col_of_numbers.append([])
        for row in range((square//3)*3, (square//3)*3+3):
            for col in range((square%3)*3, (square%3)*3+3):
                if sudoku_state[row][col] == "N":
                    for r in range(3):
                        for c in range(3):
                            if sudoku[row][col][r][c] != 0:
                                count_of_numbers[sudoku[row][col][r][c] - 1] += 1
                                row_of_numbers[sudoku[row][col][r][c] - 1].append(row)
                                col_of_numbers[sudoku[row][col][r][c] - 1].append(col)
        numbers = []
        rows = []
        cols = []
        for i in range(9):
            if count_of_numbers[i] == 2:
                numbers.append(i + 1)
                rows.append(row_of_numbers[i])
                cols.append(col_of_numbers[i])
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if rows[i][0] == rows[j][0] and rows[i][1] == rows[j][1] and cols[i][0] == cols[j][0] and cols[i][1] == cols[j][1]:
                    nums_array = []
                    for x in range(3):
                        tmp = []
                        for y in range(3):
                            tmp.append(0)
                        nums_array.append(tmp)
                    nums_array[(numbers[i]-1) // 3][(numbers[i]-1) % 3] = numbers[i]
                    nums_array[(numbers[j]-1) // 3][(numbers[j]-1) % 3] = numbers[j]
                    sudoku[rows[i][0]][cols[i][0]] = nums_array
                    sudoku[rows[i][1]][cols[i][1]] = nums_array
    return sudoku, sudoku_state


def hidden_pair(sudoku, sudoku_state):
    while True:
        f1, f2, f3 = False, False, False
        sudoku1, sudoku_state = hidden_pair_row(sudoku, sudoku_state)
        if sudoku == sudoku1:
            f1 = True
        sudoku = sudoku1
        sudoku2, sudoku_state = hidden_pair_col(sudoku, sudoku_state)
        if sudoku == sudoku2:
            f2 = True
        sudoku = sudoku2
        sudoku3, sudoku_state = hidden_pair_square(sudoku, sudoku_state)
        if sudoku == sudoku3:
            f3 = True
        sudoku = sudoku3
        if f1 and f2 and f3:
            break
    return sudoku, sudoku_state


def state3(sudoku, sudoku_state):
    while True:
        sudoku1, sudoku_state1 = hidden_pair(sudoku, sudoku_state)
        sudoku2, sudoku_state2 = state2(sudoku1, sudoku_state1)
        if sudoku == sudoku2:
            sudoku = sudoku2
            sudoku_state = sudoku_state2
            break
        sudoku = sudoku2
        sudoku_state = sudoku_state2
    return sudoku, sudoku_state


def check_row(sudoku, row, col):
    res = []
    for i in range(3):
        tmp = []
        for j in range(3):
            tmp.append(sudoku[row][col][i][j])
        res.append(tmp)
    for i in range(1, 10):
        if str(i) in sudoku[row]:
            res[(i - 1) // 3][(i - 1) % 3] = 0
    return res


def check_col(sudoku, sudoku_state, row, col):
    res = []
    for i in range(3):
        tmp = []
        for j in range(3):
            tmp.append(sudoku[row][col][i][j])
        res.append(tmp)
    temp = []
    for i in range(9):
        if sudoku_state[i][col] == "F":
            temp.append(sudoku[i][col])
    for i in range(1, 10):
        if str(i) in temp:
            res[(i - 1) // 3][(i - 1) % 3] = 0
    return res


def check_square(sudoku, sudoku_state, row, col):
    res = []
    for i in range(3):
        tmp = []
        for j in range(3):
            tmp.append(sudoku[row][col][i][j])
        res.append(tmp)
    temp = []
    for i in range((row // 3) * 3, (row // 3) * 3 + 3):
        for j in range((col // 3) * 3, (col // 3) * 3 + 3):
            if sudoku_state[i][j] == "F":
                temp.append(sudoku[i][j])
    for i in range(1, 10):
        if str(i) in temp:
            res[(i - 1) // 3][(i - 1) % 3] = 0
    return res


                
#for i in range(0, 811, 30):
#   for j in range(0, 811, 30):
#        surface.blit(text,((30-text.get_width())//2+i,(30-text.get_height())//2+j))



#"Soduku" is shown on the surface and its color is changed when the DownKeyis pressed on the Keyboard
#Press Escape to exit the program
sudoku = []
for i in range(9):
    inp = input()
    temp = []
    for i in inp:
        temp.append(i)
    sudoku.append(temp)

sudoku_state = []
for i in range(9):
    temp = []
    for j in range(9):
        if sudoku[i][j] == "?":
            temp.append("N")
        else:
            temp.append("F")
    sudoku_state.append(temp)


temp = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for i in range(9):
    for j in range(9):
        if sudoku[i][j] == "?":
            sudoku[i][j] = temp


for i in range(9):
    for j in range(9):
        if sudoku_state[i][j] == "N":
            sudoku[i][j] = check_row(sudoku, i, j)
            sudoku[i][j] = check_col(sudoku, sudoku_state, i, j)
            sudoku[i][j] = check_square(sudoku, sudoku_state, i, j)


###

    
l = sudoku
    
White = (255, 255, 255)
Black = (0,0,0)
Red = (255,0,0)
Blue = (0,0,255)
#initialize all imported pygame modules
pygame.init()
#initialize a window or screen for display
size = (810,810)
surface = pygame.display.set_mode(size)
#fill Surface with a solid color
color = White
surface.fill(color)
#draw a straight line
color = Black

for i in range(0, 811, 30):
    pygame.draw.line(surface, color, (i,0), (i,size[1]), 1)
#complete a boarder  
for i in range(0, 811, 90):
    pygame.draw.line(surface, color, (i,0), (i,size[1]), 3)
    
for i in range(0, 811, 270):
    pygame.draw.line(surface, color, (i,0), (i,size[1]), 7)
    
for j in range(0, 811,30):
    pygame.draw.line(surface, Black, (0,j), (size[0],j) , 1)
    
for j in range(0, 811,90):
    pygame.draw.line(surface, Black, (0,j), (size[0],j) , 3)
    
for j in range(0, 811,270):
    pygame.draw.line(surface, Black, (0,j), (size[0],j) , 7)

    
font_name, font_size = "Times new Roman", 20
font = pygame.font.SysFont(font_name, font_size)
font1 = pygame.font.SysFont(font_name, 3*font_size)
color = Black

width = 0
hight = 0
for row in range(9):
    for col in range(9):
        if len(l[row][col]) != 3:
            left, top, wid, hei = width, hight, 90, 90
            rect = pygame.Rect(left, top, wid, hei)
            pygame.draw.rect(surface, White, rect)
            text = font1.render(str(l[row][col]), True, color)
            surface.blit(text,((90-text.get_width())//2+width,(90-text.get_height())//2+hight))
            width += 90 
            continue
        for r in range(3):
            for c in range(3):
                
                text = font.render(str(l[row][col][r][c]), True, color)
                surface.blit(text,((30-text.get_width())//2+width,(30-text.get_height())//2+hight))
                width += 30
            width -= 90
            hight += 30
        hight -= 90
        width += 90
    hight += 90
    width = 0
state = 0
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key== pygame.K_ESCAPE):
            exit(0)
            break
        if event.type == pygame.KEYDOWN and event.key== pygame.K_DOWN:
            print("hi")
            if state == 0:
                print("hi0")
                sudoku, sudoku_state = state0(sudoku, sudoku_state)
                l = sudoku
                state = 1
                
            elif state == 1:
                print("hi1")
                sudoku, sudoku_state = state1(sudoku, sudoku_state)
                l = sudoku
                state = 2
            elif state == 2:
                sudoku, sudoku_state = state2(sudoku, sudoku_state)
                l = sudoku
                state = 3
                
        
        White = (255, 255, 255)
        Black = (0,0,0)
        Red = (255,0,0)
        Blue = (0,0,255)
#initialize all imported pygame modules
        pygame.init()
#initialize a window or screen for display
        size = (810,810)
        surface = pygame.display.set_mode(size)
#fill Surface with a solid color
        color = White
        surface.fill(color)
#draw a straight line
        color = Black

        for i in range(0, 811, 30):
            pygame.draw.line(surface, color, (i,0), (i,size[1]), 1)
#complete a boarder  
        for i in range(0, 811, 90):
            pygame.draw.line(surface, color, (i,0), (i,size[1]), 3)
    
        for i in range(0, 811, 270):
            pygame.draw.line(surface, color, (i,0), (i,size[1]), 7)
    
        for j in range(0, 811,30):
            pygame.draw.line(surface, Black, (0,j), (size[0],j) , 1)
    
        for j in range(0, 811,90):
            pygame.draw.line(surface, Black, (0,j), (size[0],j) , 3)
    
        for j in range(0, 811,270):
            pygame.draw.line(surface, Black, (0,j), (size[0],j) , 7)

    #draw a rectangle on the given surface
    #left, top, width, height = width, width, size[0]-2*width, size[1]-2*width
    #rect = pygame.Rect(left, top, width, height)
    #pygame.draw.rect(surface, Blue, rect)
    #show a text on the given surface
    
        font_name, font_size = "Times new Roman", 20
        font = pygame.font.SysFont(font_name, font_size)
        font1 = pygame.font.SysFont(font_name, 3*font_size)
        color = Black
        
        
        width = 0
        hight = 0
        for row in range(9):
            for col in range(9):
                if len(l[row][col]) != 3:
                    left, top, wid, hei = width, hight, 90, 90
                    rect = pygame.Rect(left, top, wid, hei)
                    pygame.draw.rect(surface, White, rect)
                    text = font1.render(str(l[row][col]), True, color)
                    surface.blit(text,((90-text.get_width())//2+width,(90-text.get_height())//2+hight))
                    width += 90 
                    continue
                for r in range(3):
                    for c in range(3):
                
                        text = font.render(str(l[row][col][r][c]), True, color)
                        surface.blit(text,((30-text.get_width())//2+width,(30-text.get_height())//2+hight))
                        width += 30
                    width -= 90
                    hight += 30
                hight -= 90
                width += 90
            hight += 90
            width = 0
        color = Black

        for i in range(0, 811, 90):
            pygame.draw.line(surface, color, (i,0), (i,size[1]), 3)
    
        for i in range(0, 811, 270):
            pygame.draw.line(surface, color, (i,0), (i,size[1]), 7)
    
        for j in range(0, 811,90):
            pygame.draw.line(surface, Black, (0,j), (size[0],j) , 3)
    
        for j in range(0, 811,270):
            pygame.draw.line(surface, Black, (0,j), (size[0],j) , 7)
        pygame.display.flip()            
            
#sudoku, sudoku_state = state0(sudoku, sudoku_state)
#print(sudoku)
#sudoku, sudoku_state = state1(sudoku, sudoku_state)
#print(sudoku)
#sudoku, sudoku_state = state2(sudoku, sudoku_state)
#print(sudoku)
#sudoku, sudoku_state = hidden_pair(sudoku,sudoku_state)
#print("final")
#print(sudoku)



