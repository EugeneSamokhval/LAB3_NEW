import copy

import Parser
import SCNFandSDNF
import counting_method_simplifier
import table_method_simplifier
import map_sipflication


def variables_list_constructor(formula_string: str):
    variables_list = []
    for char in formula_string:
        if variables_list.count(char)==0 and (char.islower() or char.isupper()):
            variables_list.append(char)
    return variables_list


def variables_connector_sdnf(variables_list: list, logic_operation_list: list)->list:
    output_list = [[] for sublist in logic_operation_list]
    if not logic_operation_list[0]:
        return []
    for sublist_iterator in range(len(logic_operation_list)):
        for variable_iterator in range(len(variables_list)):
            if logic_operation_list[sublist_iterator][variable_iterator] == '0':
                output_list[sublist_iterator].append("!" + variables_list[variable_iterator])
            else:
                output_list[sublist_iterator].append(variables_list[variable_iterator])
    return output_list


def variable_connector_sknf(variables_list: list, logic_operation_list: list)->list:
    output_list = [[] for sublist in logic_operation_list]
    if not logic_operation_list[0]:
        return []
    for sublist_iterator in range(len(logic_operation_list)):
        for variable_iterator in range(len(variables_list)):
            if logic_operation_list[sublist_iterator][variable_iterator] == '0':
                output_list[sublist_iterator].append(variables_list[variable_iterator])
            else:
                output_list[sublist_iterator].append("!" + variables_list[variable_iterator])
    return output_list


def sdnf_decoration(sdnf_list: list):
    if [] in sdnf_list:
        sdnf_list.remove([])
    result_str = ''
    for sublist in sdnf_list:
        result_str+='('
        for sign in sublist:
            result_str +=sign+'*'
        result_str = result_str.removesuffix('*')
        result_str+=')+'
    return result_str.removesuffix('+')


def sknf_decoration(sknf_list: list):
    if [] in sknf_list:
        sknf_list.remove([])
    result_str = ''
    for sublist in sknf_list:
        result_str+='('
        for sign in sublist:
            result_str+= sign+'+'
        result_str = result_str.removesuffix('+')
        result_str+=')*'
    return result_str.removesuffix('*')


def table_of_truth_decorator(table_of_truth: list):
    for row in table_of_truth:
        print(row, end='\n')


def main():
    input_function = input()
    variables_list = variables_list_constructor(input_function)
    logic_object = Parser.Formula(input_function)
    output_list, table_of_variables = logic_object.output_logic_list()
    sdnf_string, sknf_string, out_table = SCNFandSDNF.separator_of_logic_solutions(output_list, table_of_variables)
    filled_sknf_list = variable_connector_sknf(variables_list, sknf_string)
    filled_sdnf_list = variables_connector_sdnf(variables_list, sdnf_string)
    counting_method = counting_method_simplifier.Counting(filled_sknf_list, filled_sdnf_list)
    counting_sdnf, counting_sknf = counting_method.use_simplification()
    table_simplfication = table_method_simplifier.Table(filled_sknf_list, filled_sdnf_list)
    table_sdnf, table_sknf = table_simplfication.calculate()
    map_simplifier = map_sipflication.Map(out_table, variables_list)
    map_simplification_result = map_simplifier.miniterm_union()
    print(sdnf_decoration(filled_sdnf_list), sknf_decoration(filled_sknf_list), "Расчётный метод:",
          sdnf_decoration(counting_sdnf), sknf_decoration(counting_sknf), "Табличный метод:",
          sdnf_decoration(table_sdnf), sknf_decoration(table_sknf),
          "Карта карно:", sdnf_decoration(map_simplification_result),
          sep="\n")
    table_of_truth_decorator(out_table)


if __name__ == "__main__":
    main()
