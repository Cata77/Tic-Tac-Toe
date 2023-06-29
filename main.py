import random

matrix = list()
occupied_cells = list()


def print_matrix(matrix):
    print("---------")
    for row in matrix:
        print('|', *row, '|')
    print("---------")


def check_occupied_cell(x, y):
    return True if matrix[x][y] != ' ' else False


def check_win_condition():
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


def check_state_of_game():
    is_completed, symbol = check_win_condition()
    if is_completed is not None:
        print(f'{symbol} wins')
        exit()
    elif not check_empty_cells_remaining():
        print('Draw')
        exit()


def ai_move():
    print('Making move level "easy"')
    while True:
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        if (i, j) not in occupied_cells:
            matrix[i][j] = 'O'
            occupied_cells.append((i, j))
            break


def main():
    cells = '_________'.replace('_', ' ')
    for i in range(0, len(cells), 3):
        matrix.append(list(cells[i:i + 3]))

    print_matrix(matrix)
    while True:
        try:
            x, y = map(int, input('Enter the coordinates: ').split())

        except ValueError:
            print('You should enter numbers!')
        else:
            if not (1 <= x <= 3) or not (1 <= y <= 3):
                print('Coordinates should be from 1 to 3!')
                continue
            elif check_occupied_cell(x - 1, y - 1):
                print('This cell is occupied! Choose another one!')
                continue
            else:
                x -= 1
                y -= 1
                matrix[x][y] = 'X'
                print_matrix(matrix)
                check_state_of_game()
                occupied_cells.append((x, y))
                ai_move()
                print_matrix(matrix)
                check_state_of_game()


if __name__ == '__main__':
    main()
