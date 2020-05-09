from myutils import *

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

    def child_node(self, problem, action): # to make node object of each child
        next_state = problem.result(self.state, action)
        new_cost = problem.path_cost(self.path_cost, self.state,action, next_state)
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
class Graph: # For undirected graphs only
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed

    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
class Problem(object):
    def __init__(self, initial, goal=None):
       self.initial = initial
       self.goal = goal

    def actions(self, state):
         raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:            
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1
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

    def h(self, node):
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))             
        else:
            return infinity






def astar_search(problem): # based on fig 3.24
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    gval = node.path_cost # start to node n
    hval = problem.h(node) # estimated cheapest from n to goal
    #each entry in list represents a dictionary item with key as f-val and value as node    
    nodelist = [{gval+hval:node}]    
    while nodelist:      
        entry_num = closest_node_entry_num(nodelist)        
        min_dist = list(nodelist[entry_num].keys())[0] 
        closest_node = nodelist[entry_num][min_dist] 
        print("Current Nodes : ", nodelist)
        print("min dist = ", min_dist, ", closest_node = ", closest_node)
        input("Press enter to continue...")
        if problem.goal_test(closest_node.state): 
            return closest_node        
        nodelist.pop(entry_num)        
        for child in closest_node.expand(problem):
            gval = child.path_cost
            hval = problem.h(child)
            nodelist.append( {gval+hval : child})    


''' sample entry in nodelist - 
[
 {431: <Node Zerind>},
 {435: <Node Timisoara>}, 
 {630: <Node Arad>}, 
 {654: <Node Oradea>}, 
 {570: <Node Sibiu>}, 
 {450: <Node Bucharest>}, 
 {532: <Node Sibiu>}, 
 {518: <Node Craiova>}, 
 {406: <Node Pitesti>}
]

'''
def closest_node_entry_num(nodelist): 
    min_index=0
    min_dist = list(nodelist[0].keys())[0]
    for n in range(1,len(nodelist)):
        dist = list(nodelist[n].keys())[0]
        if dist < min_dist :
            min_index=n
            min_dist = dist
    return min_index
       









def UndirectedGraph(graph_dict=None):
    return Graph(graph_dict = graph_dict, directed=False)
 
romania_map = UndirectedGraph(
    {'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},     
     'Bucharest': {'Urziceni': 85, 'Pitesti': 101, 'Giurgiu': 90, 'Fagaras': 211},
     'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138},
     'Drobeta': {'Mehadia': 75, 'Craiova': 120},
     'Eforie': {'Hirsova': 86},'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
     'Hirsova': {'Urziceni': 98, 'Eforie': 86},
     'Iasi': {'Vaslui': 92, 'Neamt': 87},
     'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
     'Oradea': {'Zerind': 71, 'Sibiu': 151},
     'Pitesti': {'Rimnicu': 97, 'Bucharest': 101, 'Craiova': 138},
     'Rimnicu': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
     'Urziceni': {'Vaslui': 142, 'Bucharest': 85, 'Hirsova': 98},
     'Zerind': {'Arad': 75, 'Oradea': 71},
     'Sibiu': {'Arad': 140, 'Fagaras': 99, 'Oradea': 151, 'Rimnicu': 80},
     'Timisoara': {'Arad': 118, 'Lugoj': 111},
     'Giurgiu': {'Bucharest': 90}, 'Mehadia': {'Drobeta': 75, 'Lugoj': 70},
     'Vaslui': {'Iasi': 92, 'Urziceni': 142},    'Neamt': {'Iasi': 87}})

romania_map.locations = dict( Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))
    

print("\nSolving for arad to bucharest...")
romania_problem = GraphProblem('Arad','Bucharest', romania_map)
resultnode = astar_search(romania_problem)
print("Path taken :" , resultnode.path())
print("Path Cost :" , resultnode.path_cost)

print("\n\nSolving for drobeta to vaslui....")
romania_problem = GraphProblem('Drobeta','Vaslui', romania_map)
resultnode = astar_search(romania_problem)
print("Path Taken :", resultnode.path())
print("Path Cost :" , resultnode.path_cost)


















