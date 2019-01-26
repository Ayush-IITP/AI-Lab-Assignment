def replace_or(expr, or_pos):
    itr = 0
    for pos in or_pos:
        pos += itr
        expr = expr[:pos] + '->' + expr[pos + 1:]
        if pos - 1 >= 0 and expr[pos - 1] != ')':
            expr = expr[:pos - 1] + '~' + expr[pos - 1:]
        else:
            stack = [')']
            n_pos = pos - 2
            n_pos = check_left_balanced(expr, n_pos, stack)
            expr = expr[:n_pos + 1] + '~' + expr[n_pos + 1:]
        itr += 2
    return expr


def replace_and(expr, and_pos):
    itr = 0
    for pos in and_pos:
        pos += itr
        expr = expr[:pos] + '->~' + expr[pos + 1:]
        if pos - 1 >= 0 and expr[pos - 1] != ')':
            expr = expr[:pos - 2] + '~' + expr[pos - 2:]
        else:
            stack = [')']
            n_pos = pos - 2
            n_pos = check_left_balanced(expr, n_pos, stack)
            expr = expr[:n_pos] + '~' + expr[n_pos:]
        itr += 3
    return expr


def check_left_balanced(expr, n_pos, stack):
    while n_pos >= 0 and len(stack) > 0:
        if expr[n_pos] == ')':
            stack.append(')')
        elif expr[n_pos] == '(':
            stack.pop()
        n_pos -= 1
    return n_pos


def replaced_negation(expr, neg_pos):
    itr = 0
    for pos in reversed(neg_pos):
        expr = expr[:pos] + '(' + expr[pos + 1:]
        if pos + 1 < len(expr) and expr[pos + 1] != '(':
            expr = expr[:pos + 2] + '->F)' + expr[pos + 2:]
        else:
            stack = ['(']
            n_pos = pos + 2
            while n_pos < len(expr) and len(stack) > 0:
                if expr[n_pos] == '(':
                    stack.append('(')
                elif expr[n_pos] == ')':
                    stack.pop()
                n_pos += 1
            expr = expr[:n_pos] + '->F)' + expr[n_pos:]
    return expr


def preprocess(expr):
    or_pos = [pos for pos, char in enumerate(expr) if char == '|']
    or_replaced_expr = replace_or(expr, or_pos)
    and_pos = [pos for pos, char in enumerate(or_replaced_expr) if char == '&']
    and_replaced_expr = replace_and(or_replaced_expr, and_pos)
    print(and_replaced_expr)
    neg_pos = [pos for pos, char in enumerate(and_replaced_expr) if char == '~']
    negation_replaced_expr = replaced_negation(and_replaced_expr, neg_pos)
    return negation_replaced_expr


def remove_extra_parenthesis(simple_expr):
    while True:
        stack = check_if_parenthesis_balanced(simple_expr)
        if len(stack) == 0 and simple_expr[0] == '(':
            simple_expr = simple_expr[1:len(simple_expr) - 1]
        else:
            return simple_expr


def check_if_parenthesis_balanced(simple_expr):
    stack = []
    for pos, symbol in enumerate(simple_expr):
        if symbol == '(':
            stack.append('(')
        elif symbol == ')':
            stack.pop()
        if len(stack) == 0 and pos != len(simple_expr) - 1:
            stack.append('a')
            return stack
    return stack
