import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from Graf_zaleznosci.main import create_word_graph, create_final_graph, draw_final_graph, create_FNF
from copy import deepcopy


def create_alphabet_and_sequence(N: int) -> tuple[list[str], list[str]]:
    alphabet = []
    for i in range(1, N+1):
        for k in range(i+1, N+1):
            alphabet.append(f'A_{i},{k}')
            for j in range(i, N+2):
                alphabet.append(f'B_{i},{j},{k}')
                alphabet.append(f'C_{i},{j},{k}')
    sequence = deepcopy(alphabet)
    alphabet.sort()
    return alphabet, sequence
# end def


def create_dependent_relations(N: int, alphabet: list[str]) -> list[tuple[str, str]]:
    dep_relations = []
    # D1 relations
    for i in range(1, N+1):
        for k in range(1, N+1):
            for j in range(1, N+2):
                if f'A_{i},{k}' in alphabet and f'B_{i},{j},{k}' in alphabet:
                    dep_relations.append((f'A_{i},{k}', f'B_{i},{j},{k}'))
    # D2 relations
    for i in range(1, N+1):
        for k in range(1, N+1):
            for j in range(1, N+2):
                if f'B_{i},{j},{k}' in alphabet and f'C_{i},{j},{k}' in alphabet:
                    dep_relations.append((f'B_{i},{j},{k}', f'C_{i},{j},{k}'))
    # D3 relations
    for i in range(1, N+1):
        for k in range(1, N+1):
            for j in range(1, N+2):
                for l in range(1, N+1):
                    if j == i+1 and f'C_{i},{j},{l}' in alphabet and f'A_{j},{k}' in alphabet:
                        dep_relations.append((f'C_{i},{j},{l}', f'A_{j},{k}'))
    # D4 relations
    for i in range(1, N+1):
        for k in range(1, N+1):
            for j in range(1, N+2):
                if f'C_{i},{j},{k}' in alphabet and f'B_{i+1},{j},{k+1}' in alphabet:
                    dep_relations.append((f'C_{i},{j},{k}', f'B_{i+1},{j},{k+1}'))
    # D5 relations
    for i in range(1, N+1):
        for k in range(1, N+1):
            for j in range(1, N+2):
                for l in range(i+1, N+1):
                    if f'C_{i},{j},{k}' in alphabet and f'C_{l},{j},{k}' in alphabet:
                        dep_relations.append((f'C_{i},{j},{k}', f'C_{l},{j},{k}'))
    return dep_relations
# end def


def provide_levels(foat_list: list[set]) -> list[int]:
    max_no_elements = 0
    for level in foat_list:
        max_no_elements += len(level)
    nodes_levels = [-1 for _ in range(max_no_elements)]
    for i, level in enumerate(foat_list):
        for el in level:
            nodes_levels[el] = i
    return nodes_levels
# end def

# def create_sequence(N: int, alphabet: )
N = 3
alphabet, sequence = create_alphabet_and_sequence(N)
dep_relations = create_dependent_relations(N, alphabet)
print(alphabet)
print(sequence)
print(dep_relations)

graph = create_word_graph(dep_relations, sequence)
final_graph = create_final_graph(graph)
draw_final_graph(final_graph, sequence, 'test')
fnf = create_FNF(final_graph, sequence)
print(fnf)
