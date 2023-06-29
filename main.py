matrix = list()


def print_matrix(matrix):
    print("---------")
    for row in matrix:
        print('|', *row, '|')
    print("---------")


def check_occupied_cell(x, y):
    return True if matrix[x][y] != ' ' else False


def define_current_symbol(x, y):
    nr_of_x = sum(cell == 'X' for rows in matrix for cell in rows)
    nr_of_o = sum(cell == 'O' for rows in matrix for cell in rows)
    if nr_of_x <= nr_of_o:
        matrix[x][y] = 'X'
    else:
        matrix[x][y] = 'O'


def check_state_of_the_game():
    # check on the rows
    for rows in matrix:
        first_element = rows[0]
        if all(element == first_element and first_element != ' ' for element in rows):
            return 'win', first_element

    # check on columns
    for cols in range(len(matrix[0])):
        first_element = matrix[0][cols]
        ok = True
        for rows in range(len(matrix)):
            if matrix[rows][cols] != first_element or first_element == ' ':
                ok = False
                break
        if ok:
            return 'win', first_element

    # check main diagonal
    ok = True
    first_element = matrix[0][0]
    for rows in range(len(matrix)):
        if matrix[rows][rows] != first_element or first_element == ' ':
            ok = False
            break
    if ok:
        return 'win', first_element

    # check secondary diagonal
    ok = True
    first_element = matrix[0][len(matrix)-1]
    for rows in range(len(matrix)):
        if matrix[rows][len(matrix) - 1 - rows] != first_element or first_element == ' ':
            ok = False
            break
    if ok:
        return 'win', first_element
    return None, None


def check_empty_cells_remaining():
    return True if any(cells == ' ' for rows in matrix for cells in rows) else False


def main():
    for i in range(0, 9, 3):
        matrix.append(list(' '))

    print_matrix(matrix)
    while True:
        try:
            x, y = map(int, input('Enter the coordinates: ').split())
        except ValueError:
            print('You should enter numbers!')
        else:
            if not (1 <= x <= 3) or not (1 <= y <= 3):
                print('Coordinates should be from 1 to 3!')
            elif check_occupied_cell(x - 1, y - 1):
                print('This cell is occupied! Choose another one!')
            else:
                x -= 1
                y -= 1
                define_current_symbol(x, y)
                print_matrix(matrix)
                is_completed, symbol = check_state_of_the_game()
                if is_completed is not None:
                    print(f'{symbol} wins')
                    break
                elif check_empty_cells_remaining():
                    print('Game not finished')
                else:
                    print('Draw')
                    break


if __name__ == '__main__':
    main()
