from datastructures import *

#----------------------------------------------------------------------

class Node:

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        if other:
            return self.state == other.state
        else:
            return False

    def expand(self):
        successors = []
        for (newState, action) in self.state.next_states():
            newNode = Node(newState, self, action)
            successors.append(newNode)
        return successors

#----------------------------------------------------------------------

def uninformed_search(initial_state, goal_state, frontier):

    initial_node = Node(initial_state, None, None)
    nodo_explorado = None
    nuevos_expandidos = None
    expanded = 0
    generated = 0
    
    explorados = Queue()
    # Cola vacia para los nodos explorados.
    frontier.insert(initial_node)

    while True:
        if frontier.is_empty():
            return (None, expanded, generated)
        nodo_explorado = frontier.remove()
        # Quitamos el primero de la frontera y se lo asignamos al nodo actual.

        if nodo_explorado.state == goal_state:
            # Aqui el __eq__ haria lo mismo no?
            return (nodo_explorado, expanded, generated)

        explorados.insert(nodo_explorado)
        # A los explorados le insertamos el nodo explorado.
        nuevos_expandidos = nodo_explorado.expand()
        # En nuevos_expandidos guardamos el nodo expandido.
        expanded = expanded + 1
        # Actualizamos los expanded.
       
        for nodo_nuevo in range (len(nuevos_expandidos)):
            if not frontier.contains(nuevos_expandidos[nodo_nuevo]) and not explorados.contains(nuevos_expandidos[nodo_nuevo]):
                generated = generated + 1
                frontier.insert(nuevos_expandidos[nodo_nuevo])               
    return (None, expanded, generated)

#----------------------------------------------------------------------
# Test functions for uninformed search

def breadth_first(initial_state, goal_state):
    frontier = Queue()
    return uninformed_search(initial_state, goal_state, frontier)

def depth_first(initial_state, goal_state):
    frontier = Stack()
    return uninformed_search(initial_state, goal_state, frontier)

def uniform_cost(initial_state, goal_state):
    frontier = PriorityQueue(lambda x: x.g)
    return uninformed_search(initial_state, goal_state, frontier)

#----------------------------------------------------------------------

def informed_search(initial_state, goal_state, frontier, heuristic):

    initial_node = Node(initial_state, None, None)
    expanded = 0
    generated = 0
    nodo_explorado = None
    nuevos_expandidos = None

    explorados = Queue()
    frontier.insert(initial_node)

    while True:
        if frontier.is_empty():
            return None
        nodo_explorado = frontier.remove()
        if nodo_explorado.state == goal_state:
            return (nodo_explorado, expanded, generated)

        explorados.insert(nodo_explorado)
        nuevos_expandidos = nodo_explorado.expand()
        expanded = expanded + 1
        explorados.insert(nodo_explorado)

        for nodo_nuevo in range(len(nuevos_expandidos)):
            if not frontier.contains(nuevos_expandidos[nodo_nuevo]) and not explorados.contains(nuevos_expandidos[nodo_nuevo]):
                generated = generated + 1
                #.g es el coste desde el nodo inicial hasta el nodo en cuestion
                nuevos_expandidos[nodo_nuevo].g = nodo_explorado.g + nodo_explorado.h
                #.h es el coste heuristico desde el nodo en cuestion al nodo objetivo
                nuevos_expandidos[nodo_nuevo].h = heuristic(nuevos_expandidos[nodo_nuevo].state, goal_state)
                frontier.insert(nuevos_expandidos[nodo_nuevo])
        
    return (None, expanded, generated)

#----------------------------------------------------------------------
# Test functions for informed search

def greedy(initial_state, goal_state, heuristic):
    frontier = PriorityQueue(lambda x: x.g)
    return informed_search(initial_state, goal_state, frontier, heuristic)

def a_star(initial_state, goal_state, heuristic):
    frontier = PriorityQueue(lambda x: x.g + x.h)
    return informed_search(initial_state, goal_state, frontier, heuristic)

#---------------------------------------------------------------------
# Heuristic functions

def h1(current_state, goal_state):
    #heuristica basada en el numero de personas que faltan por pasar a la orilla final
    return 6 - current_state.miss[1] - current_state.cann[1]

def h2(current_state, goal_state):
    if current_state.boat_position == 'left':
        viaje = 1
    else:
        viaje = 0
    return 2*((current_state.miss[0] + current_state.cann[0] + viaje))
#----------------------------------------------------------------------

def show_solution(node, expanded, generated):
    path = []
    while node != None:
        path.insert(0, node)
        node = node.parent
    if path:
        print "Solution took %d steps" % (len(path) - 1)
        print path[0].state
        for n in path[1:]:
            print '%s %s %s' % (n.action[0], n.action[1], n.action[2])
            print n.state
    print "Nodes expanded:  %s" % expanded
    print "Nodes generated: %s\n" % generated