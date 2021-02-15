# 3_3_puzzle with different algorithms

Write a program to solve the 8-puzzle problem using each of the following algorithms:
1. Depth-first search
2. Iterative deepening search 
3. A* search using two different suitable heuristics 
4. comparision of heuristics 
   

How to run

Algorithms

- dfs
- ids
- astar1 (heuristic wrong tile  )
- astar2 (heuristic manhattan distance of all misplaced tile)

### How to run the program
python3 algorithm start_and_goal_state.txt

### Input File 1  (please avoid escape (\\) char before *)
\* 2 3 1 7 5 4 6 8

1 2 3 \* 4 5 6 7 8
  

### Results of different algorithm runs
#### Depth First search

``python homework1.py dfs  start_and_goal_state.tx``

Number of moves 9

Number of states enqueued 693


#### Iterative Deepening Search

``python homework1.py ids  start_and_goal_state.txt``

Number of moves 5

Number of states enqueued 107



#### A* star with wrong tile heuristic
``python homework1.py astar1  start_and_goal_state.txt``

Number of moves 5

Number of states enqueued 7


#### A* star with manhattan heuristic
``python homework1.py astar2  start_and_goal_state.txt``

Number of moves 5

Number of states enqueued 6


#Analysis of heuristic 1 and heuristic 2

We don't much difference in number of nodes enqueued 
when start and goal state are reachable with fewer moves
when comparing heuristic 1  and heuristic 2. But when we 
increase depth limit(12) and change start/goal with more no. of moves
we clearly observe saving time complexity of heuristic 2 than heuristic 1.
We see 69% reduction in number of states enqueued(in this case). 
we also observe heuristic 2 values ranges from(0,11) and heuristic 1
value ranges from (0,7). which proves that larger admissible heuristic is better
than smaller heuristic.

### Input File 2 
\* 2 3 1 7 5 4 6 8

\* 2 5 1 3 4 6 7 8

### Results of different algorithm runs
#### Depth First search

``python homework1.py dfs  start_and_goal_state.tx``

Depth First Search

Unsuccessfull:cutoff reached or Failure


#### Iterative Deepening Search

``python homework1.py ids  start_and_goal_state.txt``

Number of moves 12

Number of states enqueued 5921



#### A* star with wrong tile heuristic
``python homework1.py astar1  start_and_goal_state.txt``

Number of moves 12

Number of states enqueued 94



#### A* star with manhattan heuristic
``python homework1.py astar2  start_and_goal_state.txt``

Number of moves 12

Number of states enqueued 29


References:
 - Linkedin Learning Data structure and algorithms
 - Artificial Intelligence - A Modern Approach (3rd Edition)
