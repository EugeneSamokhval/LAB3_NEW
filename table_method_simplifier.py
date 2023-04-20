import counting_method_simplifier


def implicant_in_constitut(constit: list, impl: list):
    variable: str
    for variable in impl:
        if variable not in constit:
            return False
    return True


def table_correct_check(table: list):
    checked_columns = [False for column in table]
    for column in range(len(table)):
        for sign in range(len(table[column])):
            if table[column][sign] == 1:
                checked_columns[column] = True
    return checked_columns.count(True) == len(checked_columns)


def table_check(table: list, implicants: list):
    operable_implicants = implicants[:]
    operatable_table = table[:]
    iteration_flag = True
    while iteration_flag:
        iteration_flag = False
        for implicant in range(len(operable_implicants)):
            temp_table = operatable_table[:]
            for column in range(len(temp_table)):
                temp_table[column][implicant] = 0
            if table_correct_check(temp_table):
                for column in range(len(temp_table)):
                    temp_table[column].remove(table[column][implicant])
                    operatable_table = temp_table[:]
                    operable_implicants.remove(implicant)
                    iteration_flag = True
                    break
    return operable_implicants


class Table:
    def __init__(self, sknf_operable, sdnf_operable):
        sknf_united = sknf_operable[:]
        sdnf_united = sdnf_operable[:]
        iterator = 1
        while iterator != 0:
            sknf_united, iterator = counting_method_simplifier.sdnf_simplification(sknf_united)
        iterator = 1
        while iterator != 0:
            sdnf_united, iterator = counting_method_simplifier.sdnf_simplification(sdnf_united)
        self.operable_sknf = sknf_united
        self.sknf = sknf_operable
        self.sdnf = sdnf_operable
        self.operable_sdnf = sdnf_united

    def sdnf_processing(self):
        table_to_check = [[0 for implicant in self.operable_sdnf] for constitut in self.sdnf]
        for constitut in range(len(table_to_check)):
            for implicant in range(len(table_to_check[constitut])):
                if implicant_in_constitut(self.sdnf[constitut], self.operable_sdnf[implicant]):
                    table_to_check[constitut][implicant] = 1
        result = table_check(table_to_check, self.operable_sdnf)
        return result

    def sknf_processing(self):
        table_to_check = [[0 for implicant in self.operable_sknf] for constitut in self.sknf]
        for constitut in range(len(table_to_check)):
            for implicant in range(len(table_to_check[constitut])):
                if implicant_in_constitut(self.sknf[constitut], self.operable_sknf[implicant]):
                    table_to_check[constitut][implicant] = 1
        result = table_check(table_to_check, self.operable_sknf)
        return result

    def calculate(self):
        sknf_optimised = self.sknf_processing()
        sdnf_optimised = self.sdnf_processing()
        return sdnf_optimised, sknf_optimised

