import numpy as np
import time

x_axis = 5
y_axis = 5
mines_number = 4
get_mines_randomly_2d = 0

## Random board
real_grid = np.full((y_axis, x_axis), 9,dtype=int)
show_grid = real_grid.copy()
get_mines_randomly = np.random.choice(real_grid.size, mines_number, replace=False)
get_mines_randomly_2d = np.unravel_index(get_mines_randomly, real_grid.shape)
real_grid[get_mines_randomly_2d] = -1
## Print the original board
print("Original board : Bomb position only")
print(real_grid)
print("\n \n \n")


## Random start point
x_start ,y_start = None, None
while True:
    x_start, y_start = np.random.randint(0, x_axis), np.random.randint(0, y_axis)
    if real_grid[x_start, y_start] == 9:
        count = 0
        check_p = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for i,j in check_p[:]:
            a,b =x_start+i,y_start+j
            if a in range(0,x_axis) and b in range(0,y_axis):
                if real_grid[a,b] == -1:
                    count += 1
        if count == 0: ## Make sure the start point is a spreadable point
            break

## untouch_lst : list of unchosen squares
get_mines_randomly_2d = np.transpose(get_mines_randomly_2d).tolist()
untouch_lst = [(x,y) for x in range(x_axis) for y in range(y_axis)]
untouch_lst.remove((x_start,y_start))


## spread : the action occur when click a square with no mine around, all around square is auto-click
def spread(x,y,real_grid,show_grid,queue,around = []):
    for i,j in around:
        a,b = x+i,y+j
        if real_grid[a][b] == 9:
            check_around(a,b,real_grid,show_grid,queue)

## check_around : the action when click a square
def check_around(x,y,real_grid,show_grid,queue = []):
    if not real_grid[x][y] == -1:
        ## When click a no-mine square, it check around and get the number of mines around
        count = 0
        check_p = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for i,j in check_p[:]:
            a,b = x+i,y+j
            if a in range(0,x_axis) and b in range(0,y_axis):
                if real_grid[a,b] == -1:
                    count += 1
                elif real_grid[a,b] in range(0,9):
                    check_p.remove((i,j))
            else: 
                check_p.remove((i,j))
        ## If count = 0 than spread
        if count == 0:
            real_grid[x][y] = 0
            show_grid[x][y] = 0
            spread(x,y,real_grid,show_grid,queue,check_p)
            if (x,y) in untouch_lst:
                untouch_lst.remove((x,y))
        ## If not just reveal the count
        else:
            real_grid[x][y] = count
            show_grid[x][y] = count
            if (x,y) in untouch_lst:
                untouch_lst.remove((x,y))
            queue.append((x,y,check_p))
    return queue ,real_grid, show_grid

## queue : contains a list of tuples, each tuple is a point and around points used for check
queue=[]

## mine_found : list of mine found by the algorithm
mine_found = []

def shrink_p(queue): ## delete some around points in tuple that are already clicked by the algorithm
    for x , y, p in queue[:]:
        if p:
            for i,j in p[:]:
                a , b = x+i, y+j
                if (a,b) not in untouch_lst:
                    p.remove((i,j))
        else: queue.remove((x,y,p))
    return queue

## Actions after first random click at random start point by the algorithm
queue, real_grid, show_grid = check_around(x_start,y_start,real_grid,show_grid,[])
queue =  shrink_p(queue)
steps = [((x_start,y_start),show_grid)] ## steps: list of tuples, each tuple is a step move and state after that move
steps_to_win = [] ## wining step move list of algorithm
type_of_step = [] ## Type of step : either Click (click a square) or Flag (detect a bomb)
## Print the board after first move
print("Start board : After first random move")
print(show_grid)
print("\n \n \n")


# Heuristics
def check_mine_base_on_square_left(queue, real_grid, show_grid, mine_found):
    k = True
    while k:
        k= False
        for x,y ,p in queue[:]:
            mine = 0 # number of already found mines
            unknown = 0 # number of unknown squares
            for i,j in p[:]:
                a,b = x+i,y+j
                if (a,b) in mine_found:
                    mine += 1
                elif (a,b) in untouch_lst:
                    unknown += 1
                else: p.remove((i,j))
            
            s_grid= show_grid.copy()
            r_grid= real_grid.copy()
            
            if mine == real_grid[x,y]:
                # if all mines are found => other squares near x,y is sure no-bomb => click all other squares
                k= True
                for i,j in p[:]:
                    a,b = x+i,y+j
                    if (a,b) not in mine_found and (a,b) in untouch_lst:
                        new_queue,real_grid,show_grid = check_around(a,b,r_grid,s_grid)
                        steps.append(((a,b),s_grid))
                        steps_to_win.append((a,b))
                        type_of_step.append("Click")
                        queue += shrink_p(new_queue)
                queue.remove((x,y,p))
            
            elif unknown <= real_grid[x][y] - mine:
                # if unknown <= numbers of bomb left, all unknowns squares are bombs, add to mine_found
                k = True
                for i,j in p[:]:
                    a,b = x+i,y+j
                    if (a,b) not in mine_found:
                        mine_found.append((a,b))
                        s_grid[a][b] = -1
                        steps.append(((a,b),s_grid))
                        steps_to_win.append((a,b))
                        type_of_step.append("Flag")
                queue.remove((x,y,p))


## Run the rest algorithm
start_time = time.time()
check_mine_base_on_square_left(queue,real_grid,show_grid,mine_found)
end_time = time.time()


## Print result
print("List of mines found :")
print(mine_found)

## Start unsuccessful algorithm : needs to choose random square to continue
if not mine_found:
    print("Your first step, step on a number, must choose a random square")
if len(mine_found) != mines_number:
    print("You get a case that u need to make a gacha square to keep moving")
## End unsuccessful algorithm

## Steps list output
print("step to win: " + str(steps_to_win))
print("Time to run: " + str(end_time-start_time))
def navigate_list(steps, step_types):
    current_position = 0
    while True:
        print("\n \n")
        square, real_grid = steps[current_position]
        step_type = step_types[current_position]
        print("Move : " + str(step_type) + " Point " + str(square))
        print(real_grid)
        user_input = input("Press 'a' to go backward, 'd' to go forward, or 'q' to quit: ").lower()
        if user_input == 'a':
            current_position = max(0, current_position - 1)
        elif user_input == 'd':
            current_position = min(len(steps) - 1, current_position + 1)
        elif user_input == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please enter 'a', 'd', or 'q'.")

navigate_list(steps, type_of_step)


## PROBLEMS : 
## Luck-based
## Unknown square overlap
## No bombs left, but still have unknown squares