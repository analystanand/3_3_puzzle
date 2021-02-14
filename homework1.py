import sys
import heapq
import itertools

actions = {
    "right": (0, 1),
    "left": (0, -1),
    "up": (-1, 0),
    "down": (1, 0)
}

direction = ["right", "left", "up", "down"]


class Node():
    def __init__(self, state, depth, parent, action, cost):
        self.state = state
        self.depth = depth
        self.action = action
        self.parent = parent
        self.cost = cost
        self.loc_key = {}

        for i in range(3):
            for j in range(3):
                self.loc_key[self.state[i][j]] = (i, j)

        self.blank_loc = self.loc_key["*"]

    def get_loc(self):
        return self.loc_key

    def get_state(self):
        return self.state

    def get_cost(self):
        return self.cost

    def is_valid_child(self, next_move_loc):
        i, j = next_move_loc
        return 0 <= i < 3 and 0 <= j < 3

    def get_blank_loc(self):
        return self.blank_loc

    def get_children(self, path):
        children = []
        for dir in direction:
            row_dir, col_dir = actions[dir]
            next_move_loc = (self.blank_loc[0] + row_dir, self.blank_loc[1] + col_dir)
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
                child_node = Node(child_state_tup, self.depth + 1, self, dir, self.cost + 1)
                repeat = False
                for j in path:
                    if is_goal_state(j, child_node):
                        repeat = True
                if repeat is False:
                    children.append(child_node)
        return children

    def get_str(self):
        state_flatten = []
        for i in range(3):
            for j in range(3):
                state_flatten.append(self.state[i][j])
        state_str = "".join(state_flatten)
        return state_str

    def __str__(self):
        return str(self.state)


def is_goal_state(node, goal):
    return node.get_str() == goal.get_str()


def get_state_tuple(data):
    state = tuple(tuple(data[i:i + 3]) for i in range(0, 9, 3))
    return tuple(state)


def get_puzzle_print(state):
    for i in state:
        print(i)
    print("\n")


def dfs(node, goal, path, depth, limit, count):
    count += 1
    path.append(node)

    if is_goal_state(node, goal):
        return node, depth, path, count
    elif limit == 0:
        path.pop()
        return "cut_off", None, None, count
    else:
        cut_off_occ = False
        children = node.get_children(path)
        for i in children:
            res, dep, p, count = dfs(i, goal, path, depth + 1, limit - 1, count)
            if res == "cut_off":
                cut_off_occ = True
            else:
                if res != "failure:":
                    return res, dep, p, count

        path.pop()
        if cut_off_occ:
            return "cut_off", None, None, count
        else:
            return "failure", None, None, count


def read_state(file):
    with  open(file) as file:
        data = file.read().split()
        state = get_state_tuple(data)
        node = Node(state, depth=0, parent=None, action=None, cost=0)
        return node


def heuristic_wrong_tile(start, goal):
    cost = 0
    for i, j in zip(list(start.get_str()), list(goal.get_str())):
        if i != "*" and i != j:
            cost += 1
    return cost


def heuristic_manhattan(start, goal):
    d1, d2 = start.get_loc(), goal.get_loc()
    cost = 0
    for k, v in d1.items():
        if k != "*":
            x1, y1 = d1[k]
            x2, y2 = d2[k]
            cost += abs(x2 - x1) + abs(y2 - y1)
    return cost


class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.counter = itertools.count()

    def is_empty(self):
        return not self.elements

    def addToQueue(self, item, priority):
        count = next(self.counter)
        entry = (priority, count, item)
        heapq.heappush(self.elements, entry)

    def getFromQueue(self):
        return heapq.heappop(self.elements)[2]

    def __str__(self):
        return str(self.elements)


def get_path(predecessors, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = predecessors[current]
    path.append(start)
    path.reverse()
    return path


def astar(start_node, goal_node, heuristic, limit):
    pri_que = PriorityQueue()
    pri_que.addToQueue(start_node, 0)
    path_traversel = {start_node.get_state(): None}
    g_values = {start_node: 0}
    path = []
    overall_cost = 0

    while not pri_que.is_empty():
        current_node = pri_que.getFromQueue()
        path.append(current_node)

        if is_goal_state(current_node, goal_node):
            return get_path(path_traversel, start_node.get_state(), goal_node.get_state()), len(path)
        elif overall_cost > limit:
            break
        else:
            children = current_node.get_children(path)
            for i in children:
                cost = g_values[current_node] + 1
                g_values[i] = cost
                f_value = cost + heuristic(current_node, goal_node)
                pri_que.addToQueue(i, f_value)
                path_traversel[i.get_state()] = current_node.get_state()
                overall_cost = cost
    return None, None


if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print(sys.argv[0], "takes 3 arguments. Not ", len(sys.argv) - 1)
        sys.exit()

    algorithm = sys.argv[1]
    start_state = sys.argv[2]
    goal_state = sys.argv[3]

    path = []
    start_node = read_state(start_state)
    goal_node = read_state(goal_state)

    print("Input Tile position")
    get_puzzle_print(start_node.get_state())
    print("Goal Position")
    get_puzzle_print(goal_node.get_state())
    limit_depth = 10
    if algorithm == "dfs":
        print("Depth First Search")
        node, depth, path, count = dfs(start_node, goal_node, path, depth=0, limit=limit_depth, count=0)
        if node == "cut_off" or node == "failure":
            print("Unsuccessfull:cutoff reached or Failure")
        else:
            print("Output (List of states starting from input to goal state, if found):")
            for ix, i in enumerate(path):
                print(ix + 1)
                get_puzzle_print(i.get_state())
            print("Number of moves", depth)
            print("Number of states enqueued", count)
    elif algorithm == "ids":
        c = 0
        result = True
        print("Iterative Deepening Search")
        for j in range(limit_depth + 1):
            path = []
            node, depth, path, count = dfs(start_node, goal_node, path, depth=0, limit=j, count=0)
            c += count  # summing all previous enqueued states count
            if node == "cut_off" or node == "failure":
                continue
            else:
                print("Output (List of states starting from input to goal state, if found):")
                result = False
                for ix, i in enumerate(path):
                    print(ix + 1)
                    get_puzzle_print(i.get_state())
                print("Number of moves", depth)
                print("Number of states enqueued", c)
                break
        if result:
            print("Unsuccessfull:cutoff reached or Failure")
    elif algorithm == "astar1":
        print("A_star: heuristic_wrong_tile ")

        path, moves = astar(start_node, goal_node, heuristic_wrong_tile, limit_depth)
        if path is not None:
            for i in path:
                get_puzzle_print(i)
            print("Number of moves", len(path) - 1)
            print("Number of states enqueued", moves)
        else:
            print("Unsuccessfull:cutoff reached or Failure")
    elif algorithm == "astar2":
        print("A_star: heuristic_manhattan ")
        path, moves = astar(start_node, goal_node, heuristic_manhattan, limit_depth)
        if path is not None:
            for i in path:
                get_puzzle_print(i)
            print("Number of moves", len(path) - 1)
            print("Number of states enqueued", moves)
        else:
            print("Unsuccessfull:cutoff reached or Failure")
    else:
        print("Please type correct algo name")
