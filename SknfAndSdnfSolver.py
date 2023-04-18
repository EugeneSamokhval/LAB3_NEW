import copy

import LogicOperatins


operation_priority = {"!": 5, '*': 4, '+': 3, '@': 2, '=': 1, '(': 0, ')': 0}
operators = ['*', '+', '!', '=', '@']


def expression_parser(function: list):
    if type(function) == int:
        return function
    for iteration in range(len(function)):
        if not type(function[iteration]) == int:
            if function[iteration].islower():
                function[iteration] = 1
    return function


def variable_processor_sknf(sknf_list, solveable_form, stack):
    for sublist in sknf_list:
        for variable in sublist:
            if len(variable) > 1:
                solveable_form.append(variable[1])
                solveable_form.append("!")
            else:
                solveable_form.append(variable)
            stack.insert(0, '+')
        stack.pop(0)
        if stack.count('*') != 0:
            while stack[0] != '*':
                solveable_form.append(stack.pop(0))
        stack.insert(0, '+')
    stack.pop(0)
    return solveable_form, stack


def variable_processor_sdnf(sdnf_list, solveable_form, stack):
    for sublist in sdnf_list:
        for variable in sublist:
            if len(variable) > 1:
                solveable_form.append(variable[1])
                solveable_form.append("!")
            else:
                solveable_form.append(variable)
            stack.insert(0, '*')
        stack.pop(0)
        if stack.count('*') != 0:
            while stack[0] == '*':
                solveable_form.append(stack.pop(0))
        stack.insert(0, '+')
    stack.pop(0)
    return solveable_form, stack


def empty_list_cleaner(list_of_subformulas):
    output = []
    for subfomula in list_of_subformulas:
        if len(subfomula) != 0:
            output.append(subfomula)
    return output


class Solver:
    def __init__(self):
        self.sknf_prebuilt = []
        self.sdnf_prebuilt = []

    def sdnf_output_list_creation(self, sdnf_list):
        stack = []
        solveable_form = []
        sdnf_list = empty_list_cleaner(sdnf_list)
        if len(sdnf_list) == 0:
            return [0]
        if type(sdnf_list[0][0]) != str:
            solveable_form, stack = variable_processor_sdnf(sdnf_list, solveable_form, stack)
        else:
            for variable in sdnf_list:
                if len(variable) > 1:
                    solveable_form.append(variable[1])
                    solveable_form.append("!")
                else:
                    solveable_form.append(variable)
                stack.insert(0, '*')
            stack.pop(0)
        for operator in stack:
            solveable_form.append(operator)
        return solveable_form

    def sknf_output_list_creation(self, sknf_list):
        stack = []
        solveable_form = []
        if len(sknf_list) == 0:
            return 0
        if len(sknf_list)!= 0:
            if type(sknf_list[0][0]) == str:
                for variable in sknf_list:
                    if len(variable) > 1:
                        solveable_form.append(variable[1])
                        solveable_form.append("!")
                    else:
                        solveable_form.append(variable)
                    stack.insert(0, '+')
                stack.pop(0)
            else:
                solveable_form, stack = variable_processor_sknf(sknf_list, solveable_form, stack)
        for operator in stack:
            solveable_form.append(operator)
        return solveable_form

    def solve(self, postfix_list: list):
        stack = []
        if type(postfix_list) != int:
            if len(postfix_list) == 0:
                return 0
        else:
            return postfix_list
        for char in postfix_list:
            if operators.count(char) == 0:
                stack.insert(0, char)
            else:
                if char == "*":
                    stack[0] = LogicOperatins.logic_variable_and(stack[1], stack[0])
                    stack.pop(1)
                elif char == "!":
                    stack[0] = LogicOperatins.logic_variable_not(stack[0])
                elif char == "+":
                    stack[0] = LogicOperatins.logic_variable_or(stack[1], stack[0])
                    stack.pop(1)
        return stack[0]

    def operand_checkout_sknf(self, operand):
        solvable = self.sknf_output_list_creation(operand)
        solvable = expression_parser(solvable)
        result = self.solve(solvable)
        if result == 0:
            return True
        else:
            return False

    def checkout_sknf_subfunction(self, sknf_list: list, operand: list):
        if not self.operand_checkout_sknf(operand):
            return None
        sknf_copy = sknf_list[:]
        operand_truth_table = []
        sknf_copy.remove(operand)
        for iteration in range(len(operand)):
            if len(operand[iteration]) == 1:
                operand_truth_table.append(True)
            else:
                operand[iteration].strip('!')
                operand_truth_table.append(False)
        if len(sknf_copy) != 0:
            sknf_copy = self.sknf_output_list_creation(sknf_copy)
        for first_iterator in range(len(sknf_copy)):
            if operand.count(sknf_copy[first_iterator]) != 0:
                if operand_truth_table[operand.index(sknf_copy[first_iterator])]:
                    sknf_copy[first_iterator] = 1
                else:
                    sknf_copy[first_iterator] = 0
        if len(sknf_copy) != 0:
            result = self.solve(sknf_copy)
        else:
            result = None
        return result

    def operand_checkout_sdnf(self, operand: list):
        solvable = self.sdnf_output_list_creation(operand)
        solvable = expression_parser(solvable)
        result = self.solve(solvable)
        if result == 1:
            return True
        else:
            return False

    def checkout_sdnf_subfunction(self, sdnf_list: list, operand: list):
        if not self.operand_checkout_sdnf(operand):
            return None
        sdnf_copy =copy.deepcopy(sdnf_list)
        sdnf_copy.remove(operand)
        operand_truth_table = []
        for iteration in range(len(operand)):
            if len(operand[iteration]) == 1:
                operand_truth_table.append(True)
            else:
                operand[iteration].strip('!')
                operand_truth_table.append(False)
        if len(sdnf_copy) != 0:
            sdnf_copy = self.sdnf_output_list_creation(sdnf_copy)
        for first_iterator in range(len(sdnf_copy)):
            if operand.count(sdnf_copy[first_iterator]) != 0:
                if operand_truth_table[operand.index(sdnf_copy[first_iterator])]:
                    sdnf_copy[first_iterator] = 1
                else:
                    sdnf_copy[first_iterator] = 0
        if len(sdnf_copy) != 0:
            result = self.solve(sdnf_copy)
        else:
            result = None
        return result

    def checkout_function(self, sknf_list, sdnf_list):
        sknf_useless_list = []
        for operands in range(len(sknf_list)):
            temp_result = self.checkout_sknf_subfunction(sknf_list, sknf_list[operands])
            if type(temp_result) == int:
                sknf_useless_list.append(operands)
        sdnf_useless_list = []
        for operands in range(len(sdnf_list)):
            temp_result = self.checkout_sdnf_subfunction(sdnf_list, sdnf_list[operands])
            if type(temp_result) == int:
                sdnf_useless_list.append(operands)
        return sdnf_useless_list, sknf_useless_list


