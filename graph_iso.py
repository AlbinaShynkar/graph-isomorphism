import copy
import time

from graph_io import *


def get_colors(graph: Graph):
    result = []
    color_to_vertex = {}
    color_occurrence = []
    for current_vertex in graph.vertices:
        if current_vertex.colornum not in color_to_vertex.keys():
            color_to_vertex[current_vertex.colornum] = {current_vertex}
        else:
            color_to_vertex[current_vertex.colornum].add(current_vertex)
        color_occurrence.append(current_vertex.colornum)
    color_occurrence.sort()
    result.append(color_to_vertex)
    result.append(color_occurrence)
    return result


def color_refinement(graph: Graph, colored: bool):
    if not colored:
        for uncolored_vertex in graph.vertices:
            uncolored_vertex.colornum = uncolored_vertex.degree

    coloring = get_colors(graph)
    color_to_vertex = coloring[0]
    color_occurrence = coloring[1]

    next_available_color = max(color_to_vertex) + 1

    for current_color in color_to_vertex:
        updated_colors = {}
        for vertex in color_to_vertex[current_color]:
            vertex_1 = vertex
            vertex_1_neighbours_colors = []
            for neighbours_1 in vertex_1.neighbours:
                vertex_1_neighbours_colors.append(neighbours_1.colornum)
            vertex_1_neighbours_colors.sort()
            break
        for vertex_2 in color_to_vertex[current_color]:
            if vertex_1 != vertex_2:
                vertex_2_neighbours_colors = []
                for neighbours_2 in vertex_2.neighbours:
                    if neighbours_2 in updated_colors.keys():
                        vertex_2_neighbours_colors.append(updated_colors[neighbours_2][0])
                    else:
                        vertex_2_neighbours_colors.append(neighbours_2.colornum)
                vertex_2_neighbours_colors.sort()

                if vertex_1_neighbours_colors != vertex_2_neighbours_colors:
                    if updated_colors:
                        for key in list(updated_colors):
                            check = updated_colors[key]
                            if check[2] == vertex_2_neighbours_colors:
                                updated_colors[vertex_2] = [vertex_2.colornum, check[1], vertex_2_neighbours_colors]
                                vertex_2.colornum = check[1]
                                break
                            elif len(updated_colors) == list(updated_colors).index(key):
                                updated_colors[vertex_2] = [vertex_2.colornum, next_available_color,
                                                            vertex_2_neighbours_colors]
                                vertex_2.colornum = next_available_color
                                next_available_color += 1
                    else:
                        updated_colors[vertex_2] = [vertex_2.colornum, next_available_color,
                                                    vertex_2_neighbours_colors]
                        vertex_2.colornum = next_available_color
                        next_available_color += 1

    updated_color_occurrence = get_colors(graph)[1]
    if color_occurrence == updated_color_occurrence:
        return graph
    else:
        return color_refinement(graph, True)


def balanced(color_to_vertex: {}):
    result = []
    balance = True
    one_bijection = True
    colors_occurred_4_or_more = []

    for current_color in color_to_vertex:
        if len(color_to_vertex[current_color]) % 2 != 0:
            balance = False
            break
        elif len(color_to_vertex[current_color]) != 2:
            one_bijection = False
            colors_occurred_4_or_more.append(current_color)

    result.append(balance)
    result.append(one_bijection)
    result.append(colors_occurred_4_or_more)

    return result


def bijections(graph: Graph):
    coloring_a_and_b = get_colors(graph)
    color_to_vertex = coloring_a_and_b[0]

    balanced_result = balanced(color_to_vertex)
    balance = balanced_result[0]
    one_bijection = balanced_result[1]
    colors_occurred_4_or_more = balanced_result[2]

    if balance:
        if one_bijection:
            return 1
        else:
            number_of_isomorphisms = 0

            vertex_list = color_to_vertex[colors_occurred_4_or_more[0]]
            for vertex_a in vertex_list:
                if vertex_a.label < (len(graph.vertices) / 2):
                    a = vertex_a
                    break

            vertex_list_b = []
            for vertex_b in vertex_list:
                if vertex_b.label >= (len(graph.vertices) / 2):
                    vertex_list_b.append(vertex_b)

            for vertex in vertex_list_b:
                bv = vertex

                refined_a_and_b_copy = copy.deepcopy(graph)
                a_copy = refined_a_and_b_copy.vertices[graph.vertices.index(a)]
                b_copy = refined_a_and_b_copy.vertices[graph.vertices.index(bv)]

                available_color = max(color_to_vertex.keys()) + 1

                a_copy.colornum = available_color
                b_copy.colornum = available_color

                refined_refined_a_and_b_copy = color_refinement(refined_a_and_b_copy, True)
                number_of_isomorphisms += bijections(refined_refined_a_and_b_copy)

            return number_of_isomorphisms

    else:
        return 0


def count_isomorphisms(graph_a: Graph, graph_b: Graph):
    a_and_b = graph_a.__add__(graph_b)
    refined_a_and_b = color_refinement(a_and_b, False)

    if len(graph_a.vertices) == len(graph_b.vertices):
        return bijections(refined_a_and_b)
    else:
        return 0


def count_auto_isomorphisms(graph: Graph):
    a = graph
    b = copy.deepcopy(graph)
    return count_isomorphisms(a, b)


def output_equivalence(exampleGraph):
    with open(exampleGraph) as f:
        a = load_graph(f, read_list=True)

    print(exampleGraph)
    print("equivalence classes:")

    list_occurrence = []

    for graph1 in a[0]:
        for graph2 in a[0]:
            if graph1 != graph2 and (
                    "[" + str(a[0].index(graph1)) + ", " + str(a[0].index(graph2)) + "]") not in list_occurrence:
                graph_1_and_graph_2 = color_refinement(graph1.__add__(graph2), False)
                balanced_output = balanced(get_colors(graph_1_and_graph_2)[0])
                balance = balanced_output[0]
                if balance:
                    print("[" + str(a[0].index(graph1)) + ", " + str(a[0].index(graph2)) + "]")
                    var = "[" + str(a[0].index(graph2)) + ", " + str(a[0].index(graph1)) + "]"
                    list_occurrence.append(var)
    print("\n")


def output_isomorphisms(exampleGraph):

    with open(exampleGraph) as f:
        a = load_graph(f, read_list=True)

    print(exampleGraph)
    print("equivalence classes:")

    list = []

    for graph1 in a[0]:
        for graph2 in a[0]:
            if graph1 != graph2 and (
                    "[" + str(a[0].index(graph1)) + ", " + str(a[0].index(graph2)) + "]") not in list:
                num = count_isomorphisms(graph1, graph2)
                if num >= 1:
                    print("[" + str(a[0].index(graph1)) + ", " + str(a[0].index(graph2)) + "]" + "  " + str(num))
                    var = "[" + str(a[0].index(graph2)) + ", " + str(a[0].index(graph1)) + "]"
                    list.append(var)
    print("\n")


def output_auto_isomorphisms(exampleGraph):

    with open(exampleGraph) as f:
        a = load_graph(f, read_list=True)

    print(exampleGraph)
    print("equivalence classes:")

    list = []
    for graph1 in a[0]:
        for graph2 in a[0]:
            if graph1 != graph2 and (
                    "[" + str(a[0].index(graph1)) + ", " + str(a[0].index(graph2)) + "]") not in list:
                num_1 = count_auto_isomorphisms(graph1)
                num_2 = count_auto_isomorphisms(graph2)
                if num_1 == num_2:
                    print("[" + str(a[0].index(graph1)) + ", " + str(a[0].index(graph2)) + "]" + "  " + str(num_1))
                    var = "[" + str(a[0].index(graph2)) + ", " + str(a[0].index(graph1)) + "]"
                    list.append(var)
    print("\n")


start = time.perf_counter()

output_equivalence('colorref_smallexample_6_15.grl')
output_isomorphisms('torus24.grl')
output_auto_isomorphisms('colorref_smallexample_4_7.grl')

end = time.perf_counter()

print(str(end - start))
