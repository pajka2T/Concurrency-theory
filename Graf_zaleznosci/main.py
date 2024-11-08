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
    alphabet = lines[-2][i+1:-2].split(sep=", ")

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


equations, alphabet, word = get_and_form_data('case3.txt')
dep_relations, indep_relations = create_relations(equations)
print(dep_relations)
print(indep_relations)