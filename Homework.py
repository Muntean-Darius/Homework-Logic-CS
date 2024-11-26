from copy import deepcopy
import itertools
from idlelib.pyparse import trans

from anytree import Node, RenderTree
import re

l = [
    # '(P⇒Q)∧¬Q∧¬P',
    # '(P⇒Q)⇒((Q⇒S)⇒((P∨Q)⇒R))',
    # '¬(P⇒Q)⇔((P∨R)∧(¬P⇒Q))',
    # '(P⇔Q)⇔(¬(P⇒¬Q))',
    # '((¬F)∨G)'
]

laws = [
    # "(F ⇔ G) ∼ (F ⇒ G) ∧ (G ⇒ F)",
    # "(F ⇒ G) ∼ (¬F ∨ G)",
    # "F ∨ G ∼ G ∨ F",
    # "F ∧ G ∼ G ∧ F",
    # "F ⇔ G ∼ G ⇔ F",
    # "(F ∨ G) ∨ H ∼ F ∨ (G ∨ H)",
    # "(F ∧ G) ∧ H ∼ F ∧ (G ∧ H)",
    # "(F ⇔ G) ⇔ H ∼ F ⇔ (G ⇔ H)",
    # "F ∨ (G ∧ H) ∼ (F ∨ G) ∧ (F ∨ H)",
    # "F ∧ (G ∨ H) ∼ (F ∧ G) ∨ (F ∧ H)",
    # "(F ∨ G) ⇒ H ∼ (F ⇒ H) ∧ (G ⇒ H)",
    # "(F ∧ G) ⇒ H ∼ (F ⇒ H) ∨ (G ⇒ H)",
    # "F ⇒ (G ∨ H) ∼ (F ⇒ G) ∨ (F ⇒ H)",
    # "F ⇒ (G ∧ H) ∼ (F ⇒ G) ∧ (F ⇒ H)",
    # "(F ∧ G) ⇒ H ∼ F ⇒ (G ⇒ H)",
    # "¬⊤ ∼ ⊥",
    # "¬⊥ ∼ ⊤",
    # "F ∨ ⊥ ∼ F",
    # "F ∧ ⊤ ∼ F",
    # "F ∨ ⊤ ∼ ⊤",
    # "F ∧ ⊥ ∼ ⊥",
    # "⊥ ⇒ F ∼ ⊤",
    # "F ⇒ ⊤ ∼ ⊤",
    # "F ∧ F ∼ F",
    # "F ∨ F ∼ F",
    # "F ∨ (F ∧ G) ∼ F",
    # "F ∧ (F ∨ G) ∼ F",
    # "F ∨ ¬F ∼ ⊤",
    # "F ∧ ¬F ∼ ⊥",
    # "F ⇒ F ∼ ⊤",
    # "¬(¬F) ∼ F",
    # "¬(F ∨ G) ∼ ¬F ∧ ¬G",
    # "¬(F ∧ G) ∼ ¬F ∨ ¬G",
    # "¬(F ⇒ G) ∼ F ∧ (¬G)",
    # "¬(F ⇔ G) ∼ F ⇔ (¬G)",
    # "F ⇒ G ∼ F ⇔ (F ∧ G)",
    # "F ⇒ G ∼ G ⇔ (F ∨ G)",
]

consequence_laws=[
    # 'Q ∨ R, Q ⇒ ¬P, ¬(R ∧ P) ⊨ ¬P',
    # # 'P ⇒ Q, Q ⊨ P ∧ Q'
]

arguements=[
    # [0,0,0],[0,1,0],[1,0,0],[1,1,0]
]

transform_to_dnf_cnf=[
    # "(¬P ∨ Q) ∧ (¬Q) ∧ (¬P)",
    # "(¬P ∨ Q) ∨ ((¬Q ∨ S) ∨ ((P ∨ Q) ⇒ R))",
    # "(¬(P ⇒ Q)) ⇔ ((P ∨ Q) ∧ (¬P ⇒ Q))",
    # "(P ⇔ Q) ⇔ (¬(P ⇒ ¬Q))",
    # "(¬P ⇒ (Q ∧ R)) ⇒ ((Q ∨ ¬R) ⇔ P)",
    # "(P ∨ ¬Q ∨ (R ⇔ S)) ⇔ (S ∧ Q)",
    # "(P ⇔ (P ∧ Q)) ⇒ ¬Q",
    # "(¬(¬P ∨ Q ∨ R)) ∨ (Q ⇒ (P ∨ ¬R))",
    # "(¬P ∨ Q ∨ R) ∧ (P ∨ ¬R) ∧ (¬Q ∨ ¬R) ∧ ¬(P ∧ R)",
]

correct_propositions=[]

def wff(p):
    k = 0
    if len(p) == 1:
        print("Arrangement is correct")
        print("The proposition is a well formed propositional formulae")
        root = tree(p)
        if root:
            for pre, fill, node in RenderTree(root):
                print(f"{pre}{node.name}")
        print()
        return
    for i in range(0, len(p)):
        if i == 0 and p[i] != "(":
            print("First character is not a open parenthesis")
            print("Arrangement is incorrect")
            print("The proposition is not a well formed propositional formulae")
            print()
            k += 1
            break
        if i == len(p) - 1 and p[i] != ")":
            print("Last character is not a closed parenthesis")
            print("Arrangement is incorrect")
            print("The proposition is not a well formed propositional formulae")
            print()
            k += 1
            break
        if (p[i].isalpha() and p[i].isupper()) or p[i]=='⊤' or p[i]=='⊥':
            if i < len(p) and p[i + 1] not in ["⇒", "∨", "⇔", "∧"] and p[i + 1] != ')':
                print("Expected operation or closed parenthesis after variable")
                print("Arrangement is incorrect")
                print("The proposition is not a well formed propositional formulae")
                print()
                k += 1
                break
        if p[i] == "¬":
            if p[i - 1] == '(' and (
                    (((p[i + 1].isalpha() and p[i + 1].isupper()) or p[i+1]=='⊥' or p[i+1]=='⊤') and p[i + 2] == ')') or (p[i + 1] == "(")) == 0:
                print("Format of negation is flawed")
                print("Arrangement is incorrect")
                print("The proposition is not a well formed propositional formulae")
                print()
                k += 1
                break
        if p[i] in ["⇒", "∨", "⇔", "∧"]:
            if p[i + 1] == ")" or p[i - 2] in ["⇒", "∨", "⇔", "∧"] or p[i - 1] == "(":
                print("Format of binary operation is flawed")
                print("Arrangement is incorrect")
                print("The proposition is not a well formed propositional formulae")
                print()
                k += 1
                break
    if k == 0:
        print("Arrangement is correct")
        print("The proposition is a well formed propositional formulae")
        correct_propositions.append(p)
        tree(p)
        print()
        variables, operations = truth_table(p)
        create_truth_table(variables, operations)
        print()

def find_matching_paren(expression, start):
    count = 0
    for i in range(start, len(expression)):
        if expression[i] == "(":
            count += 1
        elif expression[i] == ")":
            count -= 1
            if count == 0:
                return i

def find_matching_open_paren(expression, start):
    count = 0
    for i in range(start,0,-1):
        if expression[i] == ")":
            count += 1
        elif expression[i] == "(":
            count -= 1
            if count == 0:
                return i

def tree(p):
    if p == 0:
        return None

    if len(p) == 1 and ((p.isalpha() and p.isupper()) or p=='⊥' or p=='⊤'):
        return Node(p)

    i = 0
    while i < len(p):
        if p[i] == "¬":
            root = Node("¬")
            if p[i + 1] == "(":
                closing_index = find_matching_paren(p, i + 1)
                right_subtree = tree(p[i + 2: closing_index])
                if right_subtree:
                    right_subtree.parent = root
                i = closing_index
            elif (p[i + 1].isalpha() and p[i + 1].isupper()) or p[i+1]=='⊥' or p[i+1]=='⊤':
                Node(p[i + 1], parent=root)
                i += 1

        elif p[i] in ["⇒", "∨", "⇔", "∧"]:
            root = Node(p[i])
            if p[i - 1] == ")":
                opening_index = p.rfind("(", 0, 2)
                left_subtree = tree(p[opening_index + 1: i - 1])
                if left_subtree:
                    left_subtree.parent = root
            elif (p[i - 1].isalpha() and p[i - 1].isupper()) or p[i-1]=='⊥' or p[i-1]=='⊤':
                Node(p[i - 1], parent=root)

            if p[i + 1] == "(":
                closing_index = find_matching_paren(p, i + 1)
                right_subtree = tree(p[i + 2: closing_index])
                if right_subtree:
                    right_subtree.parent = root
                i = closing_index
            elif (p[i + 1].isalpha() and p[i + 1].isupper()) or p[i+1]=='⊥' or p[i+1]=='⊤':
                Node(p[i + 1], parent=root)
                i += 1

        i += 1
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")
    return root

def copy_tree(root):
    return deepcopy(root)

def interpretation(I, root):
    copied_root = copy_tree(root)

    print('We introduce the truth values into the tree')

    for pre, fill, node in RenderTree(copied_root):
        if (node.name.isalpha() and node.name.isupper()) or node.name=='⊥' or node.name=='⊤':
            node.name = I[node.name]
        print(f"{pre}{node.name}")

    def evaluate_node(node):
        if node is None:
            return

        if len(node.children) > 0:
            evaluate_node(node.children[0])
        if len(node.children) > 1:
            evaluate_node(node.children[1])

        if node.name == '⇒':
            node.name = not node.children[0].name or node.children[1].name

        elif node.name == '∨':
            node.name = node.children[0].name or node.children[1].name

        elif node.name == '⇔':
            node.name = node.children[0].name == node.children[1].name

        elif node.name == '∧':
            node.name = node.children[0].name and node.children[1].name

        elif node.name == '¬':
            node.name = not node.children[0].name

    evaluate_node(copied_root)

    print(f'The value of the proposition is {copied_root.name} for the interpretation: {I}\n')

def truth_table(p):
    operations=[]
    variables=[]
    if len(p)==1:
        variables.append(p)
        operations.append(p)
    else:
        for i in range(len(p)-1):
            if ((p[i].isalpha() and p[i].isupper()) or p[i]=='⊥' or p[i]=='⊤') and p[i] not in variables:
                variables.append(p[i])

            if p[i]=='¬':
                if (p[i+1].isalpha() and p[i+1].isupper()) or p[i+1]=='⊥' or p[i+1]=='⊤':
                    operations.append(p[i]+p[i+1])
                elif p[i+1]=='(':
                    closing_index=find_matching_paren(p,i+1)
                    operations.append(p[i]+p[i+1 : closing_index]+")")

            if p[i] in ["⇒", "∨", "⇔", "∧"]:
                if ((p[i-1].isalpha() and p[i-1].isupper()) or p[i-1]=='⊥' or p[i-1]=='⊤') and ((p[i+1].isupper() and p[i+1].isalpha()) or p[i+1]=='⊥' or p[i+1]=='⊤'):
                    operations.append('('+p[i-1]+p[i]+p[i+1]+')')
                elif ((p[i-1].isalpha() and p[i-1].isupper()) or p[i-1]=='⊥' or p[i-1]=='⊤') and p[i+1]=='(':
                    closing_index=find_matching_paren(p,i+1)
                    operations.append(p[i-1]+p[i]+p[i+1 : closing_index]+")")
                elif p[i-1]==')' and ((p[i+1].isalpha() and p[i+1].isupper()) or p[i+1]=='⊥' or p[i+1]=='⊤'):
                    opening_index=find_matching_open_paren(p,i-1)
                    operations.append('('+p[opening_index : i-1]+')'+p[i]+p[i+1]+")")
                elif p[i-1]==")" and p[i+1]=="(":
                    opening_index=find_matching_open_paren(p,i-1)
                    closing_index=find_matching_paren(p,i+1)
                    operations.append(p[opening_index : closing_index]+")")
    operations.sort(key=len)
    variables.sort()
    return variables, operations

def evaluate_operation(operation, values):
    operation = operation.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ")
    operation = operation.replace("⇒", " <= ").replace("⇔", " == ")
    operation = operation.replace("⊥", "False").replace("⊤", "True")
    return eval(operation, {}, values)

def create_truth_table(variables, operations):
    final_values=[]
    include_false = '⊥' in variables
    include_true = '⊤' in variables
    real_variables = [var for var in variables if var not in ['⊥', '⊤']]
    num_vars = len(real_variables)
    truth_values = list(itertools.product([False, True], repeat=num_vars))

    table = []
    for values in truth_values:
        values_dict = dict(zip(real_variables, values))

        if include_false:
            values_dict['⊥'] = False
        if include_true:
            values_dict['⊤'] = True

        row = []
        if include_false:
            row.append(False)
        if include_true:
            row.append(True)
        row.extend(values)

        for operation in operations:
            row.append(evaluate_operation(operation, values_dict))
            if operation==operations[-1]:
                final_values.append(evaluate_operation(operation, values_dict))

        table.append(row)

    headers=[]
    if include_false:
        headers.append('⊥')
    if include_true:
        headers.append('⊤')
    headers.extend(real_variables)
    headers.extend(operations)
    col_widths = [max(len(str(val)) for val in [header] + [row[i] for row in table]) for i, header in
                  enumerate(headers)]

    header_row = " | ".join(f"{header:{col_widths[i]}}" for i, header in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    for row in table:
        row_str = " | ".join(f"{str(val):{col_widths[i]}}" for i, val in enumerate(row))
        print(row_str)
    return final_values

def precedence(op):
    if op == '¬':
        return 4
    elif op == '∧':
        return 3
    elif op == '∨':
        return 2
    elif op == '⇒':
        return 1
    elif op == '⇔':
        return 0
    return -1

def is_right_associative(op):
    return op == '¬'

def shunting_yard(p):
    output = []
    operators = []
    i = 0

    while i < len(p):
        token = p[i]

        if (token.isalpha() and token.isupper()) or token=='⊥' or token=='⊤':
            var = token
            i += 1
            while i < len(p) and ((p[i].isalpha() and p[i].isupper()) or p[i]=='⊥' or p[i]=='⊤'):
                var += p[i]
                i += 1
            output.append(var)
            continue

        elif token in ['¬', '∧', '∨', '⇒', '⇔']:
            while (operators and operators[-1] != '(' and
                   (precedence(operators[-1]) > precedence(token) or
                    (precedence(operators[-1]) == precedence(token) and not is_right_associative(token)))):
                output.append(operators.pop())
            operators.append(token)

        elif token == '(':
            operators.append(token)

        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()

        i += 1

    while operators:
        output.append(operators.pop())

    return ' '.join(output)

def relaxed_to_strict(p):
    stack = []

    for token in p:
        if (token.isalpha() and token.isupper()) or token=='⊥' or token=='⊤':
            stack.append(token)
        elif token in ['¬', '∧', '∨', '⇒', '⇔']:
            if token == '¬':
                operand = stack.pop()
                stack.append(f'(¬{operand})')
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(f'({left}{token}{right})')

    if len(stack) == 1:
        return stack[0]
    else:
        return "Doesn't have the correct ratio of variables and operators"

def analize_logical_propositions(l):
    for i in range(len(l)):
        print()
        print(f"Relaxed syntax: {l[i]}")
        l[i]=relaxed_to_strict(shunting_yard(l[i]))
        if l[i]=="Doesn't have the correct ratio of variables and operators":
            print(l[i])
            continue;
        print(f"Strict syntax: {l[i]}")
        nr_variables = 0
        nr_binary_op = 0
        for j in l[i]:
            if (j.isalpha() and j.isupper()) or j=='⊥' or j=='⊤':
                nr_variables += 1
            if j in ["⇒", "∨", "⇔", "∧"]:
                nr_binary_op += 1
        nr_unary_op = l[i].count('¬')
        open_parenthesis = l[i].count('(')
        close_parenthesis = l[i].count(')')
        if l[i] == "":
            print("Empty string is not a well formed propositional formulae")
            print()
        else:
            print("We check if it has the correct number of binary operators for the number of variables")
            print()
            if (nr_variables - 1) < nr_binary_op:
                print(
                    f"is not a well formed propositional formulae because it has too many operations: {nr_variables} variables, {nr_binary_op} binary operators and {nr_unary_op} unary operators")
                print()
                continue
            elif (nr_variables - 1) > nr_binary_op:
                print(
                    f"is not a well formed propositional formulae because it has too few operations: {nr_variables} variables, {nr_binary_op} binary operators and {nr_unary_op} unary operators")
                print()
                continue
            else:
                print(
                    f"This proposition has the correct number of binary operators: {nr_variables} variables and {nr_binary_op} binary operators")
                print()

            print("We check if it has the correct number of parentheses for the number of variables")
            print()
            if open_parenthesis != close_parenthesis:
                print(
                    f"is not a well formed propositional formulae because it does not have an equal number of open and closed parentheses:'('-{open_parenthesis} ')'-{close_parenthesis}")
                print()
            else:
                if (nr_variables - 1 + nr_unary_op) < open_parenthesis:
                    print(
                        f"is not a well formed propositional formulae because it has too many parentheses: '()'-{open_parenthesis} and {nr_unary_op + nr_binary_op} operators")
                    print()
                    continue
                elif (nr_variables - 1 + nr_unary_op) > open_parenthesis:
                    print(
                        f"is not a well formed propositional formulae because it has too few parentheses: '()'-{open_parenthesis} and {nr_unary_op + nr_binary_op} operators")
                    print()
                    continue
                else:
                    print(
                        f"This proposition has the correct number of parentheses: '()'-{open_parenthesis} and {nr_unary_op + nr_binary_op} operators")
                    print()

            print("We check if the proposition has the correct arrangement of elements")
            print()
            wff(l[i])


def equivalence(p):
    print(p)
    p = p.split('∼')
    compare = []

    for i in range(len(p)):
        p[i] = relaxed_to_strict(shunting_yard(p[i]))
        print(p[i])

        if len(p[i]) > 1:
            variables, operations = truth_table(p[i])
            truth_values = create_truth_table(variables, operations)
            compare.append(truth_values)
        elif p[i] == '⊥':
            compare.append([False] * len(compare[0]) if len(compare) > 0 else [False])
        elif p[i] == '⊤':
            compare.append([True] * len(compare[0]) if len(compare) > 0 else [True])
        else:
            compare.append([False, True])

    max_len = max(len(compare[0]), len(compare[1]))

    for i in range(len(compare)):
        if len(compare[i]) < max_len:
            new_list = []
            for value in compare[i]:
                new_list.extend([value] * (max_len // len(compare[i])))
            compare[i] = new_list[:max_len]

    if compare[0] == compare[1]:
        print("The equivalence is True")
    else:
        print("The equivalence is False")
    print()

def check_consequence(left_propositions, right_proposition):

    all_propositions = left_propositions + [right_proposition]
    all_variables = set()
    all_operations = []

    for prop in all_propositions:
        variables, operations = truth_table(prop)
        create_truth_table(variables, operations)
        all_variables.update(variables)
        all_operations.append(operations)

    all_variables = sorted(all_variables)

    num_vars = len(all_variables)
    truth_values = list(itertools.product([False, True], repeat=num_vars))

    all_true = True
    for values in truth_values:
        values_dict = dict(zip(all_variables, values))

        left_true = all(evaluate_operation(operation, values_dict)
                        for left_operations in all_operations[:-1]
                        for operation in left_operations)

        if left_true:
            right_true = all(evaluate_operation(operation, values_dict)
                             for operation in all_operations[-1])
            if not right_true:
                all_true = False
                break

    if all_true:
        print(
            "The consequence holds: all interpretations that satisfy the left propositions also satisfy the right proposition.")
    else:
        print(
            "The consequence does not hold: there is at least one interpretation that satisfies the left propositions but not the right proposition.")


def consequence(p):
    print(p)
    p=p.split('⊨')
    p[0]=p[0].split(',')
    for i in range(len(p[0])):
        p[0][i]=relaxed_to_strict(shunting_yard(p[0][i]))

    p[1]=relaxed_to_strict(shunting_yard(p[1]))
    check_consequence(p[0], p[1])

def truth_to_formula(n,arguements):
    formula = []
    for i in arguements:
        variables=[]
        for j in range(n):
            if i[j]==1:
                variables.append(f"{chr(65+j)}")
            else:
                variables.append(f"¬{chr(65+j)}")
        formula.append("(" + "∧".join(variables) + ")")

    if formula:
        return "∨".join(formula)

def duplicate_node(node):
    new_node = deepcopy(node)
    return new_node

def get_node_expression(node):
    if node.is_leaf:
        return node.name
    elif node.name == "¬":
        return f"(¬{get_node_expression(node.children[0])})"
    elif node.name in ["∧", "∨"]:
        child_expressions = [get_node_expression(child) for child in node.children]
        return f"({f'{node.name}'.join(child_expressions)})"
    elif node.name in ["⇒", "⇔"]:
        left_expr = get_node_expression(node.children[0])
        right_expr = get_node_expression(node.children[1])
        return f"({left_expr}{node.name}{right_expr})"
    return node.name


def transform_to_nnf(node):
    if node.name == "¬":
        child = node.children[0]

        if child.name == "¬":
            print("Transformed this formula:")
            print(f"{get_node_expression(node)}")
            print("Into its equivalent:")
            print(f"{get_node_expression(child.children[0])}")
            return transform_to_nnf(child.children[0])

        elif child.name == "∧":
            new_node = Node("∨", parent=node.parent)
            for grandchild in child.children:
                negated_child = Node("¬", parent=new_node)
                negated_child.children = [transform_to_nnf(grandchild)]
            print("Transformed this formula:")
            print(f"{get_node_expression(node)}")
            print("Into its equivalent:")
            print(f"{get_node_expression(new_node)}")
            return transform_to_nnf(new_node)

        elif child.name == "∨":
            new_node = Node("∧", parent=node.parent)
            for grandchild in child.children:
                negated_child = Node("¬", parent=new_node)
                negated_child.children = [transform_to_nnf(grandchild)]
            print("Transformed this formula:")
            print(f"{get_node_expression(node)}")
            print("Into its equivalent:")
            print(f"{get_node_expression(new_node)}")
            return transform_to_nnf(new_node)

        elif child.name == "⇒":
            left, right = child.children
            new_node = Node("∧", parent=node.parent)
            negated_right = Node("¬", parent=new_node, children=[transform_to_nnf(duplicate_node(right))])
            new_node.children = [transform_to_nnf(duplicate_node(left)), negated_right]
            print("Transformed this formula:")
            print(f"{get_node_expression(node)}")
            print("Into its equivalent:")
            print(f"{get_node_expression(new_node)}")
            return transform_to_nnf(new_node)

        elif child.name == "⇔":
            left, right = child.children
            left_neg = Node("¬", parent=node.parent, children=[transform_to_nnf(duplicate_node(left))])
            right_neg = Node("¬", parent=node.parent, children=[transform_to_nnf(duplicate_node(right))])
            new_node = Node("∨", parent=node.parent)
            new_node.children = [
                Node("∧", parent=node.parent, children=[transform_to_nnf(duplicate_node(left)), right_neg]),
                Node("∧", parent=node.parent, children=[left_neg, transform_to_nnf(duplicate_node(right))]),
            ]
            print("Transformed this formula:")
            print(f"{get_node_expression(node)}")
            print("Into its equivalent:")
            print(f"{get_node_expression(new_node)}")
            return transform_to_nnf(new_node)

        else:
            return duplicate_node(node)

    elif node.name == "⇒":
        left, right = node.children
        new_node = Node("∨", parent=node.parent)
        negated_left = Node("¬", parent=new_node, children=[transform_to_nnf(duplicate_node(left))])
        new_node.children = [negated_left, transform_to_nnf(duplicate_node(right))]
        print("Transformed this formula:")
        print(f"{get_node_expression(node)}")
        print("Into its equivalent:")
        print(f"{get_node_expression(new_node)}")
        return transform_to_nnf(new_node)

    elif node.name == "⇔":
        left, right = node.children
        left_impl = Node("⇒", parent=node.parent, children=[duplicate_node(left), duplicate_node(right)])
        right_impl = Node("⇒", parent=node.parent, children=[duplicate_node(right), duplicate_node(left)])
        new_node = Node("∧", parent=node.parent, children=[left_impl, right_impl])
        print("Transformed this formula:")
        print(f"{get_node_expression(node)}")
        print("Into its equivalent:")
        print(f"{get_node_expression(new_node)}")
        return transform_to_nnf(new_node)

    elif node.name in ["∧", "∨"]:
        node.children = [transform_to_nnf(child) for child in node.children]

    return simplify_tree(Node(node.name, parent=node.parent, children=node.children))


def transform_to_dnf(node):
    op_list = ["∧", "∨"]

    def convert(node):
        if node is None:
            return None
        if node.name == op_list[0]:
            if op_list[1] in [child.name for child in node.children]:
                all_children = [[grandchild for grandchild in child.children] if child.children else [child] for child in node.children]
                distributed_children = list(itertools.product(*all_children))
                node.name = op_list[1]
                node.children = []
                for children in distributed_children:
                    print(f"Distributed {op_list[0]} over {op_list[1]}:")
                    n = Node(op_list[0], children=[duplicate_node(child) for child in children])
                    print(get_node_expression(n))
                    simplified_n = simplify_tree(deepcopy(n))
                    if get_node_expression(simplified_n) != get_node_expression(n):
                        print("Which simplifies to:")
                        print(get_node_expression(simplified_n))
                    simplified_n.parent = node
                    print("Equivalent formula so far:")
                    print(get_node_expression(simplify_tree(deepcopy(node))))



        for child in node.children[:]:
            convert(child)
        return node

    node = convert(node)
    node = simplify_tree(node)

    return node

def transform_to_cnf(node):
    p=get_node_expression(node)
    p = list(p)

    for i in range(len(p)):
        if p[i] == '∧':
            p[i] = '∨'
        elif p[i] == '∨':
            p[i] = '∧'

    return ''.join(p)

def simplify_tree(node):
    if node is None:
        return None

    children_to_remove = []
    for child in node.children[:]:
        simplified_child = simplify_tree(child)
        if simplified_child is None:
            children_to_remove.append(child)

    for child in children_to_remove:
        node.children.remove(child)

    if node.name in {"∨", "∧"}:
        new_children = []
        for child in node.children:
            if child.name == node.name:
                new_children.extend(child.children)
            else:
                new_children.append(child)
        node.children = new_children

    if node.name == "∨":
        literals = set()
        negations = set()
        for child in node.children:
            if child.name == "¬" and child.children:
                negations.add(child.children[0].name)
            elif child.name:
                literals.add(child.name)

        if literals & negations:
            node.name = "⊤"
            node.children = []
            return node

    elif node.name == "∧":
        literals = set()
        negations = set()
        for child in node.children:
            if child.name == "¬" and child.children:
                negations.add(child.children[0].name)
            elif child.name:
                literals.add(child.name)

        if literals & negations:
            node.name = "⊥"
            node.children = []
            return node

    if node.name == "¬" and node.children:
        child = node.children[0]
        if child.name == "⊤":
            node.name = "⊥"
            node.children = []
        elif child.name == "⊥":
            node.name = "⊤"
            node.children = []

    elif node.name == "∧":
        new_children = []
        for child in node.children:
            if child.name == "⊤":
                continue
            elif child.name == "⊥":
                node.name = "⊥"
                node.children = []
                return node
            else:
                new_children.append(child)
        node.children = new_children
        if len(node.children) == 0:
            node.name = "⊤"
            node.children = []
            return node
        if len(node.children) == 1:
            node = node.children[0]

    elif node.name == "∨":
        new_children = []
        for child in node.children:
            if child.name == "⊥":
                continue
            elif child.name == "⊤":
                node.name = "⊤"
                node.children = []
                return node
            else:
                new_children.append(child)
        node.children = new_children
        if len(node.children) == 0:
            node.name = "⊥"
            node.children = []
            return node
        if len(node.children) == 1:
            node = node.children[0]

    return node

analize_logical_propositions(l)
for i in laws:
    equivalence(i)
for i in consequence_laws:
    consequence(i)

print(truth_to_formula(3,arguements))

for i in transform_to_dnf_cnf:
    i=relaxed_to_strict(shunting_yard(i))
    print(f"Strict syntax:{i}")
    root=tree(i)
    negation=Node('¬',children=[deepcopy(root)])
    nnf = transform_to_nnf(root)
    nnf_2=transform_to_nnf(negation)
    print()
    print(f"NNF: {get_node_expression(nnf)}")
    print()
    dnf = transform_to_dnf(nnf)
    dnf_2=transform_to_dnf(nnf_2)
    print(f"DNF: {get_node_expression(dnf)}")
    print()
    print(f"CNF: {transform_to_cnf(dnf_2)}")
