
def logic_not(variable):
    if variable == 1:
        return 0
    else:
        return 1


def logic_then(first_variable: int, second_variable: int):
    if first_variable and not second_variable:
        return 0
    else:
        return 1


def logic_variable_not(variable):
    if type(variable) == str:
        if len(variable) == 2:
            return variable[1]
        else:
            return '!'+variable
    else:
        if variable == 1:
            return 0
        else:
            return 1


def logic_variable_and(first_variable, second_variable):
    if type(first_variable) == str and type(second_variable) == str:
        return first_variable
    elif type(first_variable) == str and second_variable == 1:
        return first_variable
    elif first_variable == 1 and type(second_variable) == str:
        return second_variable
    elif first_variable == 1 and second_variable == 1:
        return 1
    else:
        return 0


def logic_variable_or(first_variable, second_variable):
    if type(first_variable) == str and type(second_variable) == str:
        return first_variable
    elif type(first_variable) == str and type(second_variable) == int:
        return first_variable
    elif type(first_variable) == int and type(second_variable) == str:
        return second_variable
    elif first_variable == 0 and second_variable == 0:
        return 0
    else:
        return 1

