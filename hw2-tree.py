from anytree import Node, RenderTree

l = [
    '(((P⇒Q)∨S)⇔T)',
    '((P⇒(Q∧(S⇒T))))',
    '(¬(B(¬Q))∧R)',
    '((P⇒Q)∧((¬Q)∧P))',
    '((P⇒Q)⇒(Q⇒P))',
    '((¬(P∨Q))∧(¬Q))'
]


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
        if p[i].isalpha() and p[i].isupper():
            if i < len(p) and p[i + 1] not in ["⇒", "∨", "⇔", "∧"] and p[i + 1] != ')':
                print("Expected operation or closed parenthesis after variable")
                print("Arrangement is incorrect")
                print("The proposition is not a well formed propositional formulae")
                print()
                k += 1
                break
        if p[i] == "¬":
            if p[i - 1] == '(' and (
                    (p[i + 1].isalpha() and p[i + 1].isupper() and p[i + 2] == ')') or (p[i + 1] == "(")) == 0:
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
        root = tree(p)
        if root:
            for pre, fill, node in RenderTree(root):
                print(f"{pre}{node.name}")
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


def tree(p):
    if p == 0:
        return None

    if len(p) == 1 and p.isalpha() and p.isupper():
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
            elif p[i + 1].isalpha() and p[i + 1].isupper():
                Node(p[i + 1], parent=root)
                i += 1

        elif p[i] in ["⇒", "∨", "⇔", "∧"]:
            root = Node(p[i])
            if p[i - 1] == ")":
                opening_index = p.rfind("(", 0, 2)
                left_subtree = tree(p[opening_index + 1: i - 1])
                if left_subtree:
                    left_subtree.parent = root
            elif p[i - 1].isalpha() and p[i - 1].isupper():
                Node(p[i - 1], parent=root)

            if p[i + 1] == "(":
                closing_index = find_matching_paren(p, i + 1)
                right_subtree = tree(p[i + 2: closing_index])
                if right_subtree:
                    right_subtree.parent = root
                i = closing_index
            elif p[i + 1].isalpha() and p[i + 1].isupper():
                Node(p[i + 1], parent=root)
                i += 1

        i += 1
    return root

for i in l:
    print()
    print(f"{i}: ")
    nr_variables = 0
    nr_binary_op = 0
    for j in i:
        if j.isalpha() and j.isupper():
            nr_variables += 1
        if j in ["⇒", "∨", "⇔", "∧"]:
            nr_binary_op += 1
    nr_unary_op = i.count('¬')
    open_parenthesis = i.count('(')
    close_parenthesis = i.count(')')
    if i == "":
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
        wff(i)
