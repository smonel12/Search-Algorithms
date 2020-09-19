# MIT 6.034 Lab 1: Search
# Written by 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs
from functools import reduce

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


# Please see wiki lab page for full description of functions and API.

#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    if len(path) == 1:
        return 0
    else:
        edge_widths = []
        for x in range(len(path) - 1):
            edge_widths.append(graph.get_edge(path[x], path[x + 1]).length)
        return sum(edge_widths)


def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    checks_loop = []
    for a in range(len(path) - 1):
        for x in path[a + 1:]:
            if path[a] == x:
                checks_loop.append(True)
    if len(checks_loop) != 0:
        return True
    else:
        return False


def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    list_of_paths = []
    oneNode_extensions = graph.get_neighbors(path[-1])
    for ext in oneNode_extensions:
        extended_path = [x for x in path]
        extended_path.append(ext)
        list_of_paths.append(extended_path)
    for x in list_of_paths:
        if has_loops(x):
            list_of_paths.remove(x)
    return list_of_paths


def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a smaller heuristic value to be "better" because it represents a
    shorter potential path to the goal. Break ties lexicographically by 
    node name."""
    lexi_sort = sorted(nodes)
    heuristic_sort = sorted(lexi_sort, key=lambda x: graph.get_heuristic_value(x, goalNode))
    return heuristic_sort


# You can ignore the following line.  It allows generic_search (PART 3) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Basic Search ######################################################

def basic_dfs(graph, startNode, goalNode):
    """
    Performs a depth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    Uses backtracking, but does not use an extended set.
    """
    if type(startNode) != list:
        startNode = extensions(graph, startNode)
        return basic_dfs(graph, startNode, goalNode)
    else:
        if len(startNode) == 0:
            return None
        if goalNode not in startNode[0]:
            start = startNode.pop(0)
            extended_path = extensions(graph, start)
            if len(extended_path) == 0:
                pass
            else:
                for x in reversed(extended_path):
                    startNode.insert(0, x)
            for y in startNode:
                if has_loops(y):
                    startNode.remove(y)
            return basic_dfs(graph, startNode, goalNode)
        else:
            return startNode[0]


def basic_bfs(graph, startNode, goalNode):
    """
    Performs a breadth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    """
    if type(startNode) != list:
        startNode = extensions(graph, startNode)
        return basic_bfs(graph, startNode, goalNode)
    else:
        if len(startNode) == 0:
            return None
        if goalNode not in startNode[0]:
            start = startNode.pop(0)
            extended_path = extensions(graph, start)
            if len(extended_path) == 0:
                pass
            else:
                for x in extended_path:
                    startNode.append(x)
            for y in startNode:
                if has_loops(y):
                    startNode.remove(y)
            return basic_bfs(graph, startNode, goalNode)
        else:
            return startNode[0]


#### PART 3: Generic Search ####################################################

# Generic search requires four arguments (see wiki for more details):
# sort_new_paths_fn: a function that sorts new paths that are added to the agenda
# add_paths_to_front_of_agenda: True if new paths should be added to the front of the agenda
# sort_agenda_fn: function to sort the agenda after adding all new paths 
# use_extended_set: True if the algorithm should utilize an extended set


# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:
def my_sorting_fn(graph, goalNode, paths):
    sorted_paths = sorted(paths, key=lambda x: graph.get_heuristic_value(paths[paths.index(x)][-1], goalNode))
    return sorted_paths


def sort_branch(graph, goalNode, paths):
    paths = sorted(paths, key=lambda x: graph.get_heuristic_value(paths[paths.index(x)][-1], goalNode))
    sorted_path = sorted(paths, key=lambda x: path_length(graph, x))
    return sorted_path


def sort_branch_h(graph, goalNode, paths):
    sorted_path = sorted(paths,
                         key=lambda x: path_length(graph, x) + graph.get_heuristic_value(paths[paths.index(x)][-1],
                                                                                         goalNode))
    return sorted_path


generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [my_sorting_fn, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, False, my_sorting_fn, False]

generic_branch_and_bound = [do_nothing_fn, True, sort_branch, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, True, sort_branch_h, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, True, sort_branch, True]

generic_a_star = [do_nothing_fn, True, sort_branch_h, True]

# Here is an example of how to call generic_search (uncomment to run):
# my_dfs_fn = generic_search(*generic_dfs)
# my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
# print(my_dfs_path)

# Or, combining the first two steps:
# my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
# print(my_dfs_path)


### OPTIONAL: Generic Beam Search

# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

generic_beam = [None, None, None, None]


# Uncomment this to test your generic_beam search:
# print(generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2))


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    heuristic = True
    for x in graph.nodes:
        value = graph.get_heuristic_value(x, goalNode)
        my_star_fn = generic_search(*generic_branch_and_bound_with_heuristic)
        my_star_path = my_star_fn(graph, x, goalNode)
        if value > path_length(graph, my_star_path):
            heuristic = False
    return heuristic


def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    heuristic = True
    for x in graph.edges:
        length = x.length
        start = graph.get_heuristic_value(x.startNode, goalNode)
        end = graph.get_heuristic_value(x.endNode, goalNode)
        if length < abs(start-end):
            heuristic = False
    return heuristic


### OPTIONAL: Picking Heuristics

# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True.
#  Note that you MUST have completed generic a_star in order to do this:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G

# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G

# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G

# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G

##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'

#### SURVEY ####################################################################

NAME = "Shawn Monel"
COLLABORATORS = "None"
HOW_MANY_HOURS_THIS_LAB_TOOK = 15
WHAT_I_FOUND_INTERESTING = "I found implementing the bfs and dfs using recursion to be really interesting as I could " \
                           "see the reasoning more clearly than explained in class. "
WHAT_I_FOUND_BORING = "I didn't find anything boring as it all helped my understanding of the search algorithms."
SUGGESTIONS = "I would suggest telling students to reach the search.py file in the lab wiki. It took me a while to " \
              "start the lab because I didn't know about this file. "

###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]

# Creates the beam search using generic beam args, for optional beam tests
beam = generic_search(*generic_beam) if TEST_GENERIC_BEAM else None

# Creates the A* algorithm for use in testing the optional heuristics
if TEST_HEURISTICS:
    a_star = generic_search(*generic_a_star)
