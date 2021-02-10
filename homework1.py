


actions = {
    "right": (0, 1),
    "left": (0, -1),
    "up": (-1, 0),
    "down": (1, 0)
}

direction = ["right","left","up","down"]

class Node():
    def __init__(self,state,depth,parent,action,cost):
        self.state = state
        self.depth = depth
        self.action = action
        self.parent = parent
        self.cost  =  cost

        for i in range(3):
            for j in range(3):
                if self.state[i][j] == "*":
                    self.blank_loc =(i, j)

    def get_state(self):
        return self.state

    def get_cost(self):
        return self.cost

    def is_valid_child(self,next_move_loc):
        i,j = next_move_loc
        return 0 <= i < 3 and 0 <= j < 3

    def get_blank_loc(self):
        return self.blank_loc

    def get_children(self,path):
        children = []
        for dir in direction:
            row_dir, col_dir = actions[dir]
            next_move_loc = (self.blank_loc[0]+row_dir,self.blank_loc[1]+col_dir)
            if self.is_valid_child(next_move_loc):
                child_state = []
                for i in range(3):
                    temp = []
                    for j in range(3):
                      temp.append(self.state[i][j])
                    child_state.append(temp)

                temp_value = self.state[next_move_loc[0]][next_move_loc[1]]
                child_state[next_move_loc[0]][next_move_loc[1]] = "*"
                child_state[self.blank_loc[0]][self.blank_loc[1]] = temp_value
                child_state_tup = tuple(tuple(i) for i in child_state)
                child_node  = Node(child_state_tup,self.depth+1,self,dir,self.cost+1)
                repeat = False
                for j in path:
                    if is_goal_state(j,child_node):
                        repeat = True
                if repeat is False:
                    children.append(child_node)
        return children


    def get_str(self):
        state_flatten = []
        for i in range(3):
            for j in range(3):
                state_flatten.append(self.state[i][j])
        state_str =  "".join(state_flatten)
        return state_str

    def __str__(self):
        return str(self.state)


def is_goal_state(node,goal):
    return node.get_str()==goal.get_str()

def get_state_tuple(data):
    state = tuple(tuple(data[i:i + 3]) for i in range(0, 9, 3))
    return tuple(state)

def get_puzzle_print(state):
    for i in state:
        print(i)
    print("\n")


def dfs(node,goal,path,depth,limit,count):
       count+=1
       path.append(node)

       if is_goal_state(node,goal):
            return node,depth,path,count
       elif limit==0:
             path.pop()
             return "cut_off",None,None,count
       else:
            cut_off_occ = False
            children = node.get_children(path)
            for i in children:
                res,dep,p,count= dfs(i,goal,path,depth+1,limit-1,count)
                if res=="cut_off":
                    cut_off_occ =True
                else:
                    if res!="failure:":
                       return res,dep,p,count

            path.pop()
            if cut_off_occ:
                return "cut_off",None,None,count
            else:
                return "failure",None,None,count


def read_state(file):
    with  open(file) as file:
        data = file.read().split()
        state = get_state_tuple(data)
        node = Node(state,depth=0,parent=None,action = None,cost=0)
        return node

if __name__ == '__main__':


    start_node = read_state("puzzle_file.txt")
    goal_node =   read_state("goal_state_file.txt")

    path = []
    node,depth,path,count = dfs(start_node,goal_node,path,depth=0,limit=3,count=0)
    if node=="cut_off" or node=="failure":
        print("Unsuccessfull")
    else:
        for ix,i in enumerate(path):
            get_puzzle_print(i.get_state())
            print(ix)
        print("Number of moves",depth)
        print("Number of states enqueued",count)


