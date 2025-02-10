import numpy as np
import time

x_axis = 20
y_axis = 20
mines_number = 50
get_mines_randomly_2d = 0

## Random board
grid = np.full((y_axis, x_axis), 9,dtype=int)
get_mines_randomly = np.random.choice(grid.size, mines_number, replace=False)
get_mines_randomly_2d = np.unravel_index(get_mines_randomly, grid.shape)
grid[get_mines_randomly_2d] = -1

## Random start point
x ,y = None, None
while True:
    x, y = np.random.randint(0, x_axis), np.random.randint(0, y_axis)
    if grid[x, y] == 9:
        grid[x, y] = 0
        break

## untouch_lst : list of unchosen squares
get_mines_randomly_2d = np.transpose(get_mines_randomly_2d).tolist()
untouch_lst = [(x,y) for x in range(x_axis) for y in range(y_axis)]
untouch_lst.remove((x,y))


def spread(x,y,grid,queue,around = []):
    for i,j in around:
        a,b = x+i,y+j
        if grid[a][b] == 9:
            check_around(a,b,grid,queue)


def check_around(x,y,grid,queue = []):
    if not grid[x][y] == -1:
        count = 0
        check_p = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for i,j in check_p[:]:
            a,b = x+i,y+j
            if a in range(0,x_axis) and b in range(0,y_axis):
                if grid[a,b] == -1:
                    count += 1
                elif grid[a,b] in range(0,9):
                    check_p.remove((i,j))
            else: 
                check_p.remove((i,j))
        if count == 0:
            grid[x][y] = 0
            spread(x,y,grid, queue,check_p)
            if (x,y) in untouch_lst:
                untouch_lst.remove((x,y))
        else:
            grid[x][y] = count
            if (x,y) in untouch_lst:
                untouch_lst.remove((x,y))
            queue.append((x,y,check_p))
    return queue ,grid

queue=[]
# # # # specific example
# x_axis , y_axis = 5,5
# grid = np.array([[9,2,9,9,9],
#                  [9,9,2,9,2],
#                  [9,3,3,9,9],
#                  [1,9,2,2,2],
#                  [9,1,1,1,9]])
# not_9_indices = np.where(grid != 9)
# list_number = list(zip(not_9_indices[0], not_9_indices[1]))
# untouch_lst = [(x,y) for x in range(x_axis) for y in range(y_axis)]
# queue=[]
# for x,y in list_number:
#     check_p = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
#     for i,j in check_p[:]:
#         a,b=x+i,y+j
#         if a in range(0,x_axis) and b in range(0,y_axis):
#             if grid[a,b] in range(0,9):
#                 check_p.remove((i,j))
#         else: check_p.remove((i,j))
#     queue.append((x,y,check_p))
#     untouch_lst.remove((x,y))
# def check_around(x,y,grid,queue = []):
#     grid[x][y]=0
#     untouch_lst.remove((x,y))
#     return [] , grid
# ################################

# queue = []

mine_found = []

def shrink_p(queue):
    for x , y, p in queue[:]:
        if p:
            for i,j in p[:]:
                a , b = x+i, y+j
                if (a,b) not in untouch_lst:
                    p.remove((i,j))
        else: queue.remove((x,y,p))
    return queue

queue, grid = check_around(x,y,grid,[])
queue =  shrink_p(queue)
steps = [((x,y),grid)]
steps_to_win = []

# Heuristics
# check around if number == the left square aka that is the mine, and if the unknow square = mine found then press the left square
def check_mine_base_on_square_left(queue, grid, mine_found):
    k = True
    while k:
        k= False
        for x,y ,p in queue[:]:
            mine = 0
            not_mine = 0
            for i,j in p[:]:
                a,b = x+i,y+j
                if (a,b) in mine_found:
                    mine += 1
                elif (a,b) in untouch_lst:
                    not_mine += 1
                else: p.remove((i,j))
            if mine == grid[x,y]:
                k= True
                g= grid.copy()
                for i,j in p[:]:
                    a,b = x+i,y+j
                    if (a,b) not in mine_found and (a,b) in untouch_lst:
                        new_queue , grid = check_around(a,b,g)
                        steps.append(((a,b),g))
                        steps_to_win.append((a,b))
                        queue += shrink_p(new_queue)
                queue.remove((x,y,p))
            elif not_mine <= grid[x][y] - mine:
                k = True
                for i,j in p[:]:
                    a,b = x+i,y+j
                    if (a,b) not in mine_found:
                        mine_found.append((a,b))
                queue.remove((x,y,p))



start_time = time.time()
check_mine_base_on_square_left(queue,grid,mine_found)
end_time = time.time()

print(mine_found)

if not mine_found:
    print("Your first step, step on a number, must choose a random square")
if len(mine_found) != 50:
    print("You get a case that u need to make a gacha square to keep moving")
print("step to win: " + str(steps_to_win))
print("Time to run: " + str(end_time-start_time))
def navigate_list(lst):
    current_position = 0
    while True:
        square, grid = lst[current_position]
        print("Chosen square: " + str(square))
        print(grid)
        user_input = input("Press 'a' to go backward, 'd' to go forward, or 'q' to quit: ").lower()
        if user_input == 'a':
            current_position = max(0, current_position - 1)
        elif user_input == 'd':
            current_position = min(len(lst) - 1, current_position + 1)
        elif user_input == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please enter 'a', 'd', or 'q'.")

navigate_list(steps)