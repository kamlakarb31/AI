from collections import deque

infinity = float('inf')

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action 
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self): # to print node objects
        return "<Node "+ self.state + ">"

    def expand(self, problem): # to extract children
        children = []
        for action in problem.actions(self.state):
            x=self.child_node(problem,action)
            children.append(x)
        return children
        '''return [self.child_node(problem, action) for action in problem.actions(self.state)]
        #This is similar to the following
        print( [i for i in range(1,10)] )
        print( [i*i for i in range(1,10)] )
        print( [someformula(i) for i in range(1,10)] )
        '''
        

    def child_node(self, problem, action): # to make node object of each child
        next_state = problem.result(self.state, action)
        new_cost = problem.path_cost(self.path_cost, self.state,action, next_state)
        print("Current State = ", self.state, ",New Child = ", next_state,  ". Original path cost = ", self.path_cost, ", New path cost ", new_cost)
        next_node = Node(next_state, self, action,new_cost )      
        return next_node
    
    def solution(self): # extracts the path of solution
        return [node.state for node in self.path()]

    def path(self): # extracts the path of any node starting from current to source
        node, path_back = self, []
        while node: 
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back)) # order changed to show from source to current


class Problem(object): # same as given in theory
    def __init__(self, initial, goal=None):
       self.initial = initial
       self.goal = goal

    def actions(self, state):
         raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError


class GraphProblem(Problem): # subclass of problem, few functions overriden
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def actions(self, A):
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)

      
class Graph: # to represent graph 
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def get(self, a, b=None):
        links = self.graph_dict.get(a) 
        if b is None:
            return links
        else:
            cost = links.get(b)
            return cost

    def nodes(self):        
        nodelist = list()              
        for key in self.graph_dict.keys() :
            nodelist.append(key)
        return nodelist
    

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


#we are giving full description of undireced graph through dictionary.  the Graph class is not building any additional links

mumbaigraph=Graph({
    'kurla':{'sion':5,'chembur':6},
    'chembur':{'kurla':6,'thane':9, 'vashi':2},
    'vashi':{'sion':10,'chembur':2,'thane':3},
    'sion':{'kurla':5,'vashi':10},
    'thane':{'chembur':9,'vashi':3}
    })

print("after construcing graph - ")
print(mumbaigraph.graph_dict)
print("------")
print(mumbaigraph.nodes() )
print("Children of Kurla ", mumbaigraph.get('kurla'))
print("distance from kurla to chembur= ",mumbaigraph.get('kurla','chembur'))

print("=============== BFS Algo ====================")
mumbaigraph_problem = GraphProblem('kurla','thane', mumbaigraph)
print("Keys of kurla ", mumbaigraph_problem.actions( 'thane'))
finalnode = breadth_first_search(mumbaigraph_problem)
print("solution of ", mumbaigraph_problem.initial, " to ", mumbaigraph_problem.goal, finalnode.solution())
print("path cost of final node =", finalnode.path_cost)
print(mumbaigraph_problem.actions("sion"))
