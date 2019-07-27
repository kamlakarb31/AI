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

    def __repr__(self):
        return "<Node {}>".format(self.state)
  
    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))
        return next_node
    
    def solution(self):
        #return [node.action for node in self.path()[1:]]
         return [node.state for node in self.path()]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    

class Graph:
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

  
def UndirectedGraph(graph_dict=None):
    return Graph(graph_dict = graph_dict, directed=False)


class Problem(object):
    def __init__(self, initial, goal=None):
       self.initial = initial
       self.goal = goal

    def actions(self, state):
         raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):#assuming there is a single goal test
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError

class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def actions(self, A):
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)

def depth_limited_search(problem, limit=50):
    return recursive_dls(Node(problem.initial), problem, limit)

def recursive_dls(node, problem, limit):
    if problem.goal_test(node.state):
        return node
    elif limit == 0:
        return 'cutoff'
    else:
        cutoff_occurred = False
        for child in node.expand(problem):
            result = recursive_dls(child, problem, limit - 1)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result is not None:
                return result
        return 'cutoff' if cutoff_occurred else 'Not found'
    

def iterative_deepening_search(problem, limit):
    for depth in range(0,limit):
        print("checking with depth :", depth)
        result = depth_limited_search(problem, depth)
        print("result : ", result)
    return result


# graph with cycles
romania_map = UndirectedGraph(dict( {'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118}, 'Bucharest': {'Urziceni': 85, 'Pitesti': 101, 'Giurgiu': 90, 'Fagaras': 211}, 'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138}, 'Drobeta': {'Mehadia': 75, 'Craiova': 120}, 'Eforie': {'Hirsova': 86}, 'Fagaras': {'Sibiu': 99, 'Bucharest': 211}, 'Hirsova': {'Urziceni': 98, 'Eforie': 86}, 'Iasi': {'Vaslui': 92, 'Neamt': 87}, 'Lugoj': {'Timisoara': 111, 'Mehadia': 70}, 'Oradea': {'Zerind': 71, 'Sibiu': 151}, 'Pitesti': {'Rimnicu': 97, 'Bucharest': 101, 'Craiova': 138}, 'Rimnicu': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97}, 'Urziceni': {'Vaslui': 142, 'Bucharest': 85, 'Hirsova': 98}, 'Zerind': {'Arad': 75, 'Oradea': 71}, 'Sibiu': {'Arad': 140, 'Fagaras': 99, 'Oradea': 151, 'Rimnicu': 80}, 'Timisoara': {'Arad': 118, 'Lugoj': 111}, 'Giurgiu': {'Bucharest': 90}, 'Mehadia': {'Drobeta': 75, 'Lugoj': 70}, 'Vaslui': {'Iasi': 92, 'Urziceni': 142}, 'Neamt': {'Iasi': 87}}))
print("searching from arad to bucharest with level 5...")
romania_problem = GraphProblem('Arad','Bucharest', romania_map)
print(iterative_deepening_search(romania_problem, 5))

print("searching from arad to bucharest with level 2...")
romania_problem = GraphProblem('Arad','Bucharest', romania_map)
print(iterative_deepening_search(romania_problem, 2))

# graph without cycles like a tree
mumbaigraph=Graph({
    'kurla':{'sion':5,'chembur':6},
    'chembur':{'thane':9, 'vashi':2},
    'vashi':{'sion':10,'thane':3},    
    })
print("searching from kurla to borivali with level 7...")
romania_problem = GraphProblem('kurla','borivali', mumbaigraph)
print(iterative_deepening_search(romania_problem, 7))
