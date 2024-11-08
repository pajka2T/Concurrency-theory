import copy
import graphviz


def get_and_form_data(filename: str) -> (list[str], str, str):
    """
    Reads data from specified file.
    :param filename: name of file.
    :return: List of formatted equations, alphabet as string, specified word.
    """
    file = open(f'Examples/{filename}', 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()

    # Equations
    list_of_equations = []
    for line in lines[:-2]:
        if line[0] == '(':
            list_of_equations.append([line[1]])
            for char in line[3:]:
                if char.isalpha():
                    list_of_equations[lines.index(line)].append(char)

    for equation in list_of_equations:
        concat_variables = ''
        for var in equation[2:]:
            concat_variables += var
        equation[2:] = [concat_variables]

    # Alphabet
    i = 0
    while lines[-2][i] != '{':
        i += 1
    alphabet = lines[-2][i+1:-2].split(sep=",")
    for char in alphabet:
        if len(char) > 1:
            alphabet[alphabet.index(char)] = char[1]

    # Removing equations for characters not mentioned in the alphabet
    for equation in list_of_equations:
        if equation[0] not in alphabet:
            list_of_equations.remove(equation)

    # Get word
    i = 0
    while lines[-1][i] != '=':
        i += 1
    word = lines[-1][i+2:]

    return list_of_equations, alphabet, word
# end def


def create_relations(list_of_equations: list[str]) -> (list[tuple[str, str]], list[tuple[str, str]]):
    """
    Creates relations for specified list of equations.
    :param list_of_equations: List of equations as list.
    :return: List of dependent relations and list of independent relations.
    """
    dependent_relations = []
    independent_relations = []
    for equation in list_of_equations:
        dependent_relations.append((equation[0], equation[0]))
        char_changed = equation[1]
        for check_equation in list_of_equations[list_of_equations.index(equation)+1:]:
            if char_changed in check_equation[2] or check_equation[1] in equation[2]:
                dependent_relations.append((equation[0], check_equation[0]))
            else:
                independent_relations.append((equation[0], check_equation[0]))

    for relation in dependent_relations:
        if relation[0] < relation[1]:
            dependent_relations.append((relation[1], relation[0]))
    for relation in independent_relations:
        if relation[0] < relation[1]:
            independent_relations.append((relation[1], relation[0]))

    return sorted(dependent_relations), sorted(independent_relations)
# end def


def create_word_graph(dependent_relations: list[tuple[str, str]], word: str) -> list[list[int]]:
    """
    Creates word graph with all edges.
    :param dependent_relations: Dependent relations between all chars.
    :param word: Word witch graph will be returned.
    :return: Graph of specified word with all edges, where numbers accord to index of character in word.
    """
    graph = [[] for _ in range(len(word))]
    for i in range(len(word)):
        curr_char = word[i]
        for j in range(i+1, len(word)):
            next_char = word[j]
            if (curr_char, next_char) in dependent_relations:
                graph[i].append(j)
    return graph
# end def


def create_final_graph(graph: list[list[int]]) -> list[list[int]]:
    """
    For specified word's graph creates its equivalent version without redundant edges.
    :param graph: Word's graph.
    :return: Graph without redundant edges.
    """
    edges = []
    for v in range(len(graph)):
        for u in graph[v]:
            edges.append((v, u))
    # print(edges)

    removed = 0
    edges_copy = copy.deepcopy(edges)
    i = 0
    while i < len(edges):
        right_vertex = edges[i][1]
        j = 0
        while j < len(edges):
            left_vertex = edges[j][0]
            # print(right_vertex, left_vertex)
            if right_vertex == left_vertex:
                new_edge = (edges[i][0], edges[j][1])
                edges.append(new_edge)
                # print(edges)
                count = edges.count(new_edge)
                # print(count)
                if count > 1:
                    # print(edges_copy, new_edge)
                    if new_edge in edges_copy:
                        edges_copy.remove(new_edge)
                        removed += 1
                    # print(edges, removed)
                    # print(edges_copy)
            j += 1
        i += 1
    final_graph = [[] for _ in range(len(graph))]
    for edge in edges_copy:
        final_graph[edge[0]].append(edge[1])
    return final_graph
# end def


def draw_final_graph(final_graph: list[list[int]], word: str, filename: str):
    """
    Creates .png file presenting final word's graph in Examples/ directory.
    :param final_graph: Final version of word's graph.
    :param word: Specified word.
    :param filename: Name of the file, where .png file should be placed
    :return:
    """
    view = graphviz.Digraph(name=f'Examples/{filename}', format='png')
    for v in range(len(final_graph)):
        for u in final_graph[v]:
            view.edge(str(v), str(u))
        view.node(str(v), label=word[v])
    view.render(view=True)
# end def


equations, alphabet, word = get_and_form_data('case1.txt')
dep_relations, indep_relations = create_relations(equations)
print(dep_relations)
print(indep_relations)
graph = create_word_graph(dep_relations, word)
print(graph)
final_graph = create_final_graph(graph)
print(word)
draw_final_graph(final_graph, word, 'case1')
