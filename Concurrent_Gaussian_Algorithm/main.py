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

# N = 3
# alphabet, sequence = create_alphabet_and_sequence(N)
# dep_relations = create_dependent_relations(N, alphabet)
# print(alphabet)
# print(sequence)
# print(dep_relations)
#
# graph = create_word_graph(dep_relations, sequence)
# final_graph = create_final_graph(graph)
# draw_final_graph(final_graph, sequence, 'test')
# fnf = create_FNF(final_graph, sequence)
# print(fnf)


# Matrix operations


def A(matrix: list[list[float]], i: int, k: int):
    print("A: ", k, i, matrix[k][i], matrix[i][i])
    mul[k][i] = matrix[k][i] / matrix[i][i]
# end def


def B(matrix: list[list[float]], i: int, j: int, k: int, multiplier: float):
    print("B: ", i, j, k, matrix[i][j] * multiplier)
    diff[i][j][k] = matrix[i][j] * multiplier
# end def


def C(matrix: list[list[float]], i: int, j: int, k: int, value: float):
    print("C: ", i, j, k, value, matrix[k][i], matrix[k][j] - value)
    matrix[k][j] -= value
# end def


def get_and_form_data(filename: str) -> tuple[int, list[list[float]], list[list[list[float]]], list[list[float]]]:
    file = open(filename, 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()

    N = int(lines[0])
    matrix = []
    for i in range(1, N+1):
        row = lines[i].strip().split(sep=' ')
        matrix.append(row)
    y = lines[N+1].strip().split(sep=' ')
    for i in range(N):
        matrix[i].append(y[i])
    for i in range(N):
        for j in range(N+1):
            matrix[i][j] = float(matrix[i][j])
    diff = [[[0 for k in range(N)] for j in range(N + 1)] for i in range(N)]
    mul = [[0 for k in range(N)] for i in range(N)]
    return N, matrix, diff, mul
# end def


def reduce_foat_list(foat_list: list[set[int]]):
    already_used = []
    new_foat = deepcopy(foat_list)
    for i in range(len(new_foat) - 1, -1, -1):
        level = new_foat[i]
        for el in level:
            if el in already_used:
                foat_list[i].remove(el)
            else:
                already_used.append(el)


# N, matrix, diff, mul = get_and_form_data('Examples/in_1.txt')
# al, seq = create_alphabet_and_sequence(N)
# final_graph = create_final_graph(
#     create_word_graph(
#         create_dependent_relations(
#             N,
#             al
#         ),
#         seq
#     )
# )
# fnf, foat_list = create_FNF(final_graph, seq)
# print(foat_list)
# reduce_foat_list(foat_list)
# print(seq)
# print(foat_list)

from threading import Thread


def multithread(matrix: list[list[float]], foat_list: list[set[int]], seq: list[str], N: int) -> list[list[float]]:
    print(matrix)
    for level in foat_list:
        threads = []
        for el in level:
            action = seq[el]
            print(action)
            match action[0]:
                case 'A':
                    i = int(action[2]) - 1
                    k = int(action[4]) - 1
                    thread = Thread(target=A, args=(matrix, i, k))
                    thread.start()
                    # A(matrix, i, k)
                case 'B':
                    i = int(action[2]) - 1
                    j = int(action[4]) - 1
                    k = int(action[6]) - 1
                    thread = Thread(target=B, args=(matrix, i, j, k, mul[k][i]))
                    thread.start()
                    # B(matrix, i, j, k, mul[i][k])
                case 'C':
                    i = int(action[2]) - 1
                    j = int(action[4]) - 1
                    k = int(action[6]) - 1
                    thread = Thread(target=C, args=(matrix, i, j, k, diff[i][j][k]))
                    thread.start()
                    # C(matrix, i, j, k, diff[i][j][k])
            #print(matrix, mul, diff)
            print(mul)
            print(diff)
            threads.append(thread)
        for thread in threads:
            thread.join()
    return matrix
# end def

# print(multithread(matrix, foat_list, seq, N))


def solve_triangular_matrix(matrix: list[list[float]], N: int) -> list[float]:
    x = [float("inf") for _ in range(N)]
    for i in range(N-1, -1, -1):
        for j in range(N-1, i, -1):
            matrix[i][N] -= matrix[i][j] * matrix[j][N]
        matrix[i][N] /= matrix[i][i]
        x[i] = matrix[i][N]
    return x
# end def


def solve(filename: str) -> list[float]:
    N, matrix, diff, mul = get_and_form_data(filename)
    print(matrix)
    al, seq = create_alphabet_and_sequence(N)
    final_graph = create_final_graph(
        create_word_graph(
            create_dependent_relations(
                N,
                al
            ),
            seq
        )
    )
    fnf, foat_list = create_FNF(final_graph, seq)
    matrix = multithread(matrix, foat_list, seq, N)
    x = solve_triangular_matrix(matrix, N)
    return x
# end def


print("x: ", solve('Examples/in.txt'))

# for level in foat_list:
