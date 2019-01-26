from Parser import remove_extra_parenthesis, preprocess

hypothesis = set()
comb_count = 0
operation = {}


def populate_hypothesis(simple_expr):
    simple_expr = remove_extra_parenthesis(simple_expr)
    implies_pos = [pos for pos, char in enumerate(simple_expr) if char == '-']
    if len(implies_pos) == 0:
        if 'F' not in simple_expr:
            hypothesis.add(simple_expr + "->F")
            return
    for pos in implies_pos:
        stack = []
        c_pos = pos
        cnt, flag = 0, 0
        flag = left_balanced_paren(c_pos, flag, simple_expr, stack)
        if len(stack) == 0 and flag == 0:
            hypothesis.add(remove_extra_parenthesis(simple_expr[cnt:pos]))
            populate_hypothesis(simple_expr[pos + 2:])
            break


def modus_ponens(param, param1):
    if len(param) < len(param1):
        param, param1 = param1, param
    implies_pos = [pos for pos, char in enumerate(param) if char == '-']
    for pos in implies_pos:
        stack = []
        c_pos = pos
        cnt, flag = 0, 0
        flag = left_balanced_paren(c_pos, flag, param, stack)
        if len(stack) == 0 and flag == 0:
            if remove_extra_parenthesis(param1) == remove_extra_parenthesis(param[cnt:pos]):
                operation[remove_extra_parenthesis(param[pos + 2:])] = "{0}*{1}".format(param, param1)
                return remove_extra_parenthesis(param[pos + 2:])
    return ""


def left_balanced_paren(c_pos, flag, param, stack):
    while c_pos >= 0:
        if param[c_pos] == ')':
            stack.append(')')
        elif param[c_pos] == '(':
            if len(stack) == 0:
                flag = 1
                break
            stack.pop()
        c_pos -= 1
    return flag


def display_rule(param):
    if param not in operation:
        print("Hypothesis :{}".format(param))
        return
    parent_hypothesis = operation[param].split('*')
    for hypothesis in parent_hypothesis:
        display_rule(hypothesis)
    print("Modus Ponens {} and {} gives {}".format(parent_hypothesis[0], parent_hypothesis[1], param))


def hypothesis_combination(desired_result):
    global comb_count, hypothesis
    comb_count += 1
    hypothesis_list = list(hypothesis)
    for i in range(len(hypothesis) - 1):
        for j in range(i + 1, len(hypothesis)):
            if j == len(hypothesis_list):
                continue
            res_hypothesis = modus_ponens(hypothesis_list[i], hypothesis_list[j])
            if res_hypothesis != '' and res_hypothesis not in hypothesis:
                if res_hypothesis == desired_result:
                    display_rule(desired_result)
                    return -1
                hypothesis_list.append(res_hypothesis)
    hypothesis = set(hypothesis_list)
    return comb_count


def feed_cool_hypothesis_to_dumb_ai():
    val = int(input("Enter number of information you want to share"))
    while val > 0:
        info = str(input("Feed info {}".format(val)))
        hypothesis.add(preprocess(info))
        val -= 1


def main():
    expr = input("Enter the expression to check it's a Theorem or Not\n")
    simple_expr = preprocess(expr)
    print("Simplified Expresssion : ",simple_expr)
    populate_hypothesis(simple_expr)
    print(hypothesis)
    desired_result = 'F'
    is_goal_achieved = False
    human_interaction_count = 0
    while is_goal_achieved != -1:
        prev_hypothesis = hypothesis
        is_goal_achieved = hypothesis_combination(desired_result)
        if is_goal_achieved == -1:
            break
        if prev_hypothesis == hypothesis and human_interaction_count < 2:
            human_interaction_count += 1
            print("Known Hypothesis before human interaction: ",hypothesis)
            print("Hey! Human give me some intelligent hypothesis")
            feed_cool_hypothesis_to_dumb_ai()
            print("Known Hypothesis after human Interaction : ",hypothesis)
        if is_goal_achieved == 25:
            print("This {} is not a Theorem".format(expr))
            return
    print("This {} is a Theorem".format(expr))
    return


if __name__ == '__main__':
    main()
