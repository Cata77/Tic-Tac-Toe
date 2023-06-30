import random

commands = ['start', 'easy', 'user']


def print_matrix(matrix):
    print("---------")
    for row in matrix:
        print('|', *row, '|')
    print("---------")


def check_occupied_cell(matrix, x, y):
    return True if matrix[x][y] != ' ' else False


def check_win_condition(matrix):
    # Check rows
    for row in matrix:
        if row.count(row[0]) == len(row) and row[0] != ' ':
            return 'win', row[0]

    # Check columns
    for col in range(len(matrix[0])):
        if all(matrix[row][col] == matrix[0][col] and matrix[0][col] != ' ' for row in range(len(matrix))):
            return 'win', matrix[0][col]

    # Check main diagonal
    if all(matrix[i][i] == matrix[0][0] and matrix[0][0] != ' ' for i in range(len(matrix))):
        return 'win', matrix[0][0]

    # Check secondary diagonal
    if all(matrix[i][len(matrix)-1-i] == matrix[0][len(matrix)-1] and
           matrix[0][len(matrix)-1] != ' ' for i in range(len(matrix))):
        return 'win', matrix[0][len(matrix)-1]

    return None, None


def check_empty_cells_remaining(matrix):
    return any(cell == ' ' for row in matrix for cell in row)


def check_state_of_game(matrix):
    is_completed, symbol = check_win_condition(matrix)
    if is_completed is not None:
        print(f'{symbol} wins')
        exit()
    elif not check_empty_cells_remaining(matrix):
        print('Draw')
        exit()


def ai_move(matrix):
    print('Making move level "easy"')
    while True:
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        if matrix[i][j] == ' ':
            matrix[i][j] = 'O'
            break


def user_vs_ai(user='first'):
    matrix = [[' ' for _ in range(3)] for _ in range(3)]
    print_matrix(matrix)
    if user == 'first':
        while True:
            try:
                x, y = map(int, input('Enter the coordinates: ').split())
            except ValueError:
                print('You should enter numbers!')
            else:
                if not (1 <= x <= 3) or not (1 <= y <= 3):
                    print('Coordinates should be from 1 to 3!')
                    continue
                elif check_occupied_cell(matrix, x - 1, y - 1):
                    print('This cell is occupied! Choose another one!')
                    continue
                else:
                    x -= 1
                    y -= 1
                    matrix[x][y] = 'X'
                    print_matrix(matrix)
                    check_state_of_game(matrix)
                    ai_move(matrix)
                    print_matrix(matrix)
                    check_state_of_game(matrix)
    else:
        while True:
            ai_move(matrix)
            print_matrix(matrix)
            check_state_of_game(matrix)
            try:
                x, y = map(int, input('Enter the coordinates: ').split())
            except ValueError:
                print('You should enter numbers!')
            else:
                if not (1 <= x <= 3) or not (1 <= y <= 3):
                    print('Coordinates should be from 1 to 3!')
                    continue
                elif check_occupied_cell(matrix, x - 1, y - 1):
                    print('This cell is occupied! Choose another one!')
                    continue
                else:
                    x -= 1
                    y -= 1
                    matrix[x][y] = 'X'
                    print_matrix(matrix)
                    check_state_of_game(matrix)


def ai_vs_ai():
    matrix = [[' ' for _ in range(3)] for _ in range(3)]
    while True:
        ai_move(matrix)
        print_matrix(matrix)
        check_state_of_game(matrix)


def main():
    while True:
        command = input('Input command: ').split()
        if command[0] == 'exit':
            break
        elif len(command) != 3 or any(elem not in commands for elem in command):
            print('Bad parameters!')
        elif command[1] == 'user' and command[2] == 'easy':
            user_vs_ai()
        elif command[1] == 'user' and command[2] == 'easy':
            user_vs_ai('second')
        elif command[1] == 'user' and command[2] == 'easy':
            ai_vs_ai()


if __name__ == '__main__':
    main()
