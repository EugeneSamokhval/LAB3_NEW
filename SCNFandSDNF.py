import copy


def binary_to_int(binary: str):
    output_decimal = 0
    counter = len(binary)-1
    for sign in binary:
        if sign == "1":
            output_decimal+= 2 ** counter
        counter-=1
    return output_decimal


def inner_logic_sknf(variant: int, sknf_output: str):
    if variant == 1:
        sknf_output+="1"
    else:
        sknf_output+="0"
    return sknf_output


def inner_logic_sdnf(variant: int, sdnf_output: list):
    if variant == 0:
        sdnf_output+="0"
    else:
        sdnf_output+="1"
    return sdnf_output


def sknf(variations: list):
    sknf_output = ''
    for situation in variations:
        for variant in situation:
            sknf_output = inner_logic_sknf(variant, sknf_output)
        sknf_output+="*"
    sknf_output = sknf_output.removesuffix("*")
    return sknf_output


def sdnf(variations: list):
    sdnf_output = ''
    for situation in variations:
        for variant in situation:
            sdnf_output = inner_logic_sdnf(variant, sdnf_output)
        sdnf_output+="+"
    sdnf_output = sdnf_output.removesuffix("+")
    return sdnf_output


def sknf_processor(sknf: str):
    list_of_binary = sknf.split("*")
    sknf_decimal_list = []
    for binary in list_of_binary:
        sknf_decimal_list.append(binary_to_int(binary))
    return sknf_decimal_list


def sdnf_processor(sdnf: str):
    list_of_binary = sdnf.split("+")
    sdnf_decimal_list = []
    for binary in list_of_binary:
        sdnf_decimal_list.append(binary_to_int(binary))
    return sdnf_decimal_list


def list_to_string(table: list):
    table_of_char = []
    for number in table:
        table_of_char.append(str(number))
    output_string = ''
    for char in table_of_char:
        output_string+=char
    return output_string


def sknf_string_to_list_of_vars(sknf_string: str):
    sknf_list = sknf_string.split("*")
    iterator = 0
    sknf_vars_list = []
    while iterator < len(sknf_list):
        sknf_vars_list.append([variable for variable in sknf_list[iterator]])
        iterator+=1
    return sknf_vars_list


def sdnf_string_to_list_of_vars(sdnf_string: str):
    sdnf_list = sdnf_string.split("+")
    iterator = 0
    sdnf_vars_list = []
    while iterator < len(sdnf_list):
        sdnf_vars_list.append([variable for variable in sdnf_list[iterator]])
        iterator += 1
    return sdnf_vars_list


def separator_of_logic_solutions(logic_object: list, table_of_variables: list):
    counter = 0
    variations_for_sdnf = []
    variations_for_sknf = []
    while counter != len(logic_object):
        if logic_object[counter] == 1:
            variations_for_sdnf.append(table_of_variables[counter])
        else:
            variations_for_sknf.append(table_of_variables[counter])
        counter+=1
    binary_form = list_to_string(logic_object)
    sknf_string = sknf(variations_for_sknf)
    sdnf_string = sdnf(variations_for_sdnf)
    output_table = copy.deepcopy(table_of_variables)
    row = 0
    for sign in logic_object:
        output_table[row].append(sign)
        row+=1
    sdnf_list = sdnf_string_to_list_of_vars(sdnf_string)
    sknf_list = sknf_string_to_list_of_vars(sknf_string)
    return sdnf_list, sknf_list, output_table
