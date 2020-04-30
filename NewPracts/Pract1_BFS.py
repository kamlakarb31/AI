"""
@author: Kamlakar Bhopatkar
"""
from collections import deque
infinity = float('inf')   




class Graph: 
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed        
    def nodes(self):        
        return list(self.graph_dict.keys())    
    def get(self, a, b=None):
        links = self.graph_dict.get(a) 
        if b is None:
            return links
        else:
            cost = links.get(b)
            return cost     
       
class Problem: 
    def __init__(self, initial, goal=None):
       self.initial = initial
       self.goal = goal

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def actions(self, state):
         raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError
            
    def value(self, state):
        raise NotImplementedError
  
   
class GraphProblem(Problem):   #...   
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph
    def actions(self, A):        
        return self.graph.get(A)
    def result(self, state, action):
        return action
    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)       

class Node: 
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action 
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    def __repr__(self): 
        return "<Node "+ self.state + ">"
    def expand(self, problem): 
        children = []
        for action in problem.actions(self.state):
            x=self.child_node(problem,action)
            children.append(x)
        return children
    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        new_cost = problem.path_cost(self.path_cost, self.state,action,next_state)        
        next_node = Node(next_state, self, action,new_cost )   
        return next_node   
    def path(self): 
        node, path_back = self, []
        while node: 
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back)) 
    def solution(self): 
        return [node.state for node in self.path()]

def breadth_first_search(problem): # algorithm 3.11
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None

mumbaigraph=  Graph({'kurla':{'sion':5,'chembur':6},
    'chembur':{'kurla':6,'thane':9, 'vashi':2},
    'vashi':{'sion':10,'chembur':2,'thane':3},
    'sion':{'kurla':5,'vashi':10},
    'thane':{'chembur':9,'vashi':3}  }, False)

print("Nodes in graphs are :", mumbaigraph.nodes())
print("The connections are :", mumbaigraph.get('thane'))
print("The cost of connection is :", mumbaigraph.get('thane','chembur'))
mumbaigraph_problem = GraphProblem('kurla','thane', mumbaigraph)
print("Actions of sion are :", mumbaigraph_problem.actions( 'sion'))

print("---BFS----")
finalnode = breadth_first_search(mumbaigraph_problem)
if (finalnode is not None ) : 
    print("solution of ", mumbaigraph_problem.initial, " to ", mumbaigraph_problem.goal, finalnode.solution())
    print("path cost of final node =", finalnode.path_cost)
else:
    print("path does not exists")
    




















