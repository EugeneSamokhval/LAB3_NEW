import copy
import SknfAndSdnfSolver


def union_conditions(first_operand, second_operand)->bool:
    if len(first_operand) != len(second_operand):
        return False
    flag = False
    for iterator in range(len(first_operand)):
        if first_operand[iterator] != second_operand[iterator] and not flag:
            if len(first_operand[iterator]) == 2 and len(second_operand[iterator]) == 2:
                if first_operand[iterator][1] == second_operand[iterator][1]:
                    flag = True
            elif len(first_operand[iterator]) == 1 and len(second_operand[iterator]) == 2:
                if first_operand[iterator][0] == second_operand[iterator][1]:
                    flag = True
            elif len(first_operand[iterator]) == 2 and len(second_operand[iterator]) == 1:
                if first_operand[iterator][1] == second_operand[iterator][0]:
                    flag = True
        elif first_operand[iterator] != second_operand[iterator] and flag:
            return False
    return flag


def sdnf_simplification(operatable_function: list):
    result_list = []
    iteration = 0
    checkbox = [False for operand in operatable_function]
    for first_iterator in range(len(operatable_function)):
        if checkbox.count(True) == len(checkbox):
            break
        for second_iterator in range(len(operatable_function)):
            if union_conditions(operatable_function[first_iterator], operatable_function[second_iterator])\
                    and not checkbox[first_iterator] and not checkbox[second_iterator]:
                checkbox[first_iterator] = True
                checkbox[second_iterator] = True
                result_list.append(sdnf_connector(operatable_function[first_iterator],
                                                  operatable_function[second_iterator]))
                iteration+=1
    for flag in range(len(checkbox)):
        if not checkbox[flag]:
            result_list.append(operatable_function[flag])
    if iteration == 0:
        result_list = operatable_function[:]
    return result_list, iteration


def sdnf_connector(first_operand, second_operand):
    output_list = []
    for iterator in range(len(first_operand)):
        if first_operand[iterator] == second_operand[iterator]:
            output_list.append(first_operand[iterator])
    return output_list


class Counting:
    def __init__(self, sknf_list_to_simplify, sdnf_list_to_simplify):
        self.sknf_origin = sknf_list_to_simplify
        self.sdnf_origin = sdnf_list_to_simplify

    def use_simplification(self):
        iteration = 1
        sdnf_result = copy.deepcopy(self.sdnf_origin)
        sknf_result = copy.deepcopy(self.sknf_origin)
        while iteration != 0:
            sknf_result, iteration = sdnf_simplification(sknf_result)
        iteration = 1
        while iteration != 0:
            sdnf_result, iteration = sdnf_simplification(sdnf_result)
        final_result = SknfAndSdnfSolver.Solver()
        sknf_useless, sdnf_useless = final_result.checkout_function(sknf_result, sdnf_result)
        sdnf_optimised = []
        for iterator in range(len(sdnf_result)):
            if sdnf_useless.count(iterator) == 0:
                sdnf_optimised.append(sdnf_result[iterator])
        sknf_optimised = []
        for iterator in range(len(sknf_result)):
            if sknf_useless.count(iterator) == 0:
                sknf_optimised.append(sknf_result[iterator])
        return sdnf_optimised, sknf_optimised






