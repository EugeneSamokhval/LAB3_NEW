import copy


cycle = 0


def karno_map_constructor(variable: int):
    iteration = 1
    starting_table = [[0], [1]]
    while iteration != variable:
        riter = len(starting_table)-1
        iter = len(starting_table)
        while riter >= 0:
            starting_table.append(copy.deepcopy(starting_table[riter]))
            starting_table[riter].insert(0, 0)
            starting_table[iter].insert(0, 1)
            iter+=1
            riter-=1
        iteration+=1
    return starting_table


def number_of_variables_counter(number_of_variables):
    collumns_exp = 0
    rows_exp = 0
    columns = 0
    rows = 0
    if number_of_variables % 2 != 0:
        columns = 1
        while rows+columns != number_of_variables:
            rows = 2**rows_exp
            rows_exp += 1
        return rows, columns
    while columns+rows!=number_of_variables and columns+rows < number_of_variables:
        rows=2**rows_exp
        rows_exp+=1
        while columns!=rows and columns+rows!=number_of_variables:
            columns=2**collumns_exp
            collumns_exp+=1
            if columns+rows==number_of_variables:
                break
    return rows, columns


def table_constructor(table_of_truth: list):
    number_of_variables = len(table_of_truth[0])-1
    columns, rows = number_of_variables_counter(number_of_variables)
    table_to_compare_rows = karno_map_constructor(rows)
    table_to_compare_columns = karno_map_constructor(columns)
    main_table = [[0 for column in range(len(table_to_compare_columns))] for row in range(len(table_to_compare_rows))]
    for row in range(len(table_to_compare_rows)):
        for column in range(len(table_to_compare_columns)):
            list_of_truth_temp_row = table_to_compare_rows[row]+ table_to_compare_columns[column] + [1]
            if list_of_truth_temp_row in table_of_truth:
                main_table[row][column] = 1
    return main_table, table_to_compare_rows, table_to_compare_columns


def variables_filler(variables, place_to_fill):
    place_to_fill_operable = place_to_fill[:]
    for row in range(len(place_to_fill_operable)):
        for column in range(len(place_to_fill_operable[row])):
            if place_to_fill_operable[row][column] == 0:
                place_to_fill_operable[row][column] = '!' + variables[column]
            else:
                place_to_fill_operable[row][column] = variables[column]
    return place_to_fill_operable


def shape_divider(shape: list, collector: list):
    if len(shape) == 0:
        return None
    elif len(shape[0]) == 0:
        return None
    elif len(shape[0][0]) == 0:
        return None
    if len(shape) == 1 and len(shape[0]) == len(shape):
        return None
    else:
        current_shape_height = copy.deepcopy(shape)
        current_shape_height = current_shape_height[0:len(current_shape_height)//2]
        current_shape_width = copy.deepcopy(shape)
        current_shape_width = [row[0:len(row)//2] for row in current_shape_width]
        collector.append(current_shape_width)
        collector.append(current_shape_height)
        return shape_divider(current_shape_width, collector), shape_divider(current_shape_height, collector)


def shapes_constructor(main_table: list):
    operable_table = main_table[:]
    checker_matrix_max = [[[row, column] for column in range(len(operable_table[row]))]
                          for row in range(len(operable_table))]
    list_of_checkers = [copy.deepcopy(checker_matrix_max)]
    shape_divider(checker_matrix_max, list_of_checkers)
    output_list = []
    for checker in list_of_checkers:
        temp_checker = []
        for row in checker:
            for pair in row:
                if len(pair) == 0 or len(row) == 0:
                    break
                temp_checker.append(pair)
        if len(temp_checker) != 0:
            output_list.append(temp_checker)
    cleaner = []
    for checker in output_list:
        if cleaner.count(checker) == 0:
            cleaner.append(checker)
    return cleaner


def check_logic(shape, table):
    check_box = [False for cell in shape]
    iteration = 0
    for cell in shape:
        if table[cell[0]][cell[1]] == 1:
            check_box[iteration] = True
        iteration+=1
    return len(check_box) == check_box.count(True)


def tautology_check(shape: list, check_table: list):
    check_box = [False for coordinates in shape]
    for coordinates in range(len(shape)):
        if check_table[shape[coordinates][0]][shape[coordinates][1]] == 1:
            check_box[coordinates] = True
    return not check_box.count(True) > len(shape)/2


def next_iteration(shape, table):
    global cycle
    if shape[len(shape)-1][0] == 0 and shape[len(shape)-1][1] == 0 and cycle != 0:
        cycle = 0
        return None
    elif shape[len(shape)-1][1] != 0:
        for coordinate in range(len(shape)):
            shape[coordinate][1] += 1
            if shape[coordinate][1] == len(table[0]):
                shape[coordinate][1] = 0
        return shape
    elif shape[len(shape)-1][1] == 0:
        if shape[len(shape)-1][0] == 0 and shape[len(shape)-1][1] == 0 and cycle == 0:
            cycle+=1
        min_coordinate = copy.deepcopy(shape[0][1])
        for coordinate in range(len(shape)):
            shape[coordinate][0]+=1
            if shape[coordinate][0] == len(table):
                shape[coordinate][0] = 0
            if len(shape) != 1 and shape[coordinate][1] != 0:
                shape[coordinate][1] -= min_coordinate
            elif len(shape) != 1 and shape[coordinate][1] == 0:
                shape[coordinate][1] = shape[coordinate - 1][1] + 1
        return shape


def next_iteration_tall(shape, table):
    global cycle
    if shape[len(shape)-1][1] != 0 or cycle == 0:
        if shape[len(shape)-1][1] == 0:
            cycle+=1
        for coordinates in range(len(shape)):
            shape[coordinates][1] += 1
            if shape[coordinates][1]>= len(table[0]):
                shape[coordinates][1] = 0
        return shape
    else:
        cycle = 0
        return None


def next_iteration_wide(shape, table):
    global cycle
    if shape[len(shape)-1][0] != 0 or cycle == 0:
        if shape[len(shape)-1][0] == 0:
            cycle += 1
        for coordinates in range(len(shape)):
            shape[coordinates][0] += 1
            if shape[coordinates][0] >= len(table):
                shape[coordinates][0] = 0
        return shape
    else:
        cycle = 0
        return None


def next_iteration_point(shape, table):
    if shape[0][0] != len(table)-1 and shape[0][1] == len(table[0])-1:
        shape[0][0] += 1
        shape[0][1] = 0
        return shape
    elif shape[0][1] != len(table[0])-1:
        shape[0][1] += 1
        return shape
    elif shape[0][0] == len(table)-1 and shape[0][1] == len(table[0])-1:
        return None


def type_of_iteration(shape, table):
    if shape[len(shape) - 1][0] + 1 == len(table):
        return 1
    elif shape[len(shape) - 1][1] + 1 == len(table[0]):
        return 2
    elif len(shape) == 1:
        return 3
    else:
        return 4


def final_collection(list_of_vars, variables):
    changed_vars = [False for var in list_of_vars[0]]
    variables_previous = copy.deepcopy(list_of_vars[0])
    for sublist in list_of_vars:
        for variable in range(len(sublist)):
            if variables_previous[variable] != sublist[variable]:
                changed_vars[variable] = True
    changed_vars += changed_vars
    all_variations = copy.deepcopy(variables)
    all_variations: list
    for variable in variables:
        all_variations.append('!' + variable)
    controling_dictionary = {all_variations[iteration]: changed_vars[iteration]
                             for iteration in range(len(all_variations))}
    return controling_dictionary


class Map:
    def __init__(self, table_of_truth, variables):
        self.table_of_truth = table_of_truth
        self.main_table, self.grey_code_row, self.grey_code_column = table_constructor(table_of_truth)
        self.variables = variables

    def karno_map_processor(self):
        final_fill = []
        shapes = shapes_constructor(self.main_table)
        checked_table = [[0 for column in row] for row in self.main_table]
        for shape in shapes:
            if checked_table == self.main_table:
                break
            iterational_shape =copy.deepcopy(shape)
            type_iter = type_of_iteration(iterational_shape, self.main_table)
            while iterational_shape:
                if check_logic(iterational_shape, self.main_table) and tautology_check(iterational_shape,
                                                                                       checked_table):
                    for coordinates in iterational_shape:
                        checked_table[coordinates[0]][coordinates[1]] = 1
                    final_fill.append(copy.deepcopy(iterational_shape))
                if type_iter == 1:
                    iterational_shape = next_iteration_tall(iterational_shape, self.main_table)
                elif type_iter == 2:
                    iterational_shape = next_iteration_wide(iterational_shape, self.main_table)
                elif type_iter == 3:
                    iterational_shape = next_iteration_point(iterational_shape, self.main_table)
                else:
                    iterational_shape = next_iteration(iterational_shape, self.main_table)
        return final_fill

    def miniterm_union(self):
        result = []
        figures = self.karno_map_processor()
        for figure in figures:
            miniterm = []
            for coordinates in figure:
                miniterm.append(self.grey_code_row[coordinates[0]]+self.grey_code_column[coordinates[1]])
            checker = final_collection(miniterm, self.variables)
            miniterm = variables_filler(self.variables, miniterm)
            final_form = []
            for sublist in range(len(miniterm)):
                final_form.append([])
                for variable in miniterm[sublist]:
                    if not checker.get(variable):
                        final_form[sublist].append(variable)
            result.append(final_form)
        result_cleaned = []
        for obj in result:
            for subobj in obj:
                if result_cleaned.count(subobj) == 0:
                    result_cleaned.append(subobj)
        return result_cleaned
