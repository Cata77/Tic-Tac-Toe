import random
from exception import CoordinatesError, OccupiedCellError, EmptyInputError

commands = ['start', 'user']
difficulty = ['easy', 'medium', 'hard']


def print_matrix(matrix):
    print("---------")
    for row in matrix:
        print('|', *row, '|')
    print("---------")


def check_occupied_cell(matrix, x, y):
    return True if matrix[x][y] != ' ' else False


def check_state_of_game(matrix):
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
    if all(matrix[i][len(matrix) - 1 - i] == matrix[0][len(matrix) - 1]
           and matrix[0][len(matrix) - 1] != ' ' for i in range(len(matrix))):
        return 'win', matrix[0][len(matrix) - 1]

    return None, None


def check_empty_cells_remaining(matrix):
    return any(cell == ' ' for row in matrix for cell in row)


def check_if_logic_move_is_possible(matrix: list[list[str]],
                                    free_cells: list[tuple[int, int]], player_symbol: str,
                                    opponent_symbol: str) -> bool:
    copy_free_cells = list(free_cells)

    while len(copy_free_cells):
        x, y = random.choice(copy_free_cells)
        matrix[x][y] = player_symbol
        if check_state_of_game(matrix)[0] == 'win':
            print_matrix(matrix)
            free_cells.remove((x, y))
            return True
        matrix[x][y] = opponent_symbol
        if check_state_of_game(matrix)[0] == 'win':
            matrix[x][y] = player_symbol
            print_matrix(matrix)
            free_cells.remove((x, y))
            print((x, y))
            return True
        matrix[x][y] = ' '
        copy_free_cells.remove((x, y))
    return False


def ai_easy_move(free_cells, matrix, player_turn):
    x, y = random.choice(free_cells)
    free_cells.remove((x, y))
    matrix[x][y] = 'X' if player_turn % 2 == 1 else 'O'
    print_matrix(matrix)


def minimax(matrix: list[list[str]], is_maximizing: bool, player_symbol: str,
            opponent_symbol: str):
    if check_state_of_game(matrix)[1] == player_symbol:
        return 1
    elif check_state_of_game(matrix)[1] == opponent_symbol:
        return -1
    elif not check_empty_cells_remaining(matrix):
        return 0

    if is_maximizing:
        best_score = -800
        for x in range(3):
            for y in range(3):
                if matrix[x][y] == ' ':
                    matrix[x][y] = player_symbol
                    score = minimax(matrix, False, player_symbol, opponent_symbol)
                    matrix[x][y] = ' '
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = 800
        for x in range(3):
            for y in range(3):
                if matrix[x][y] == ' ':
                    matrix[x][y] = opponent_symbol
                    score = minimax(matrix, True, player_symbol, opponent_symbol)
                    matrix[x][y] = ' '
                    if score < best_score:
                        best_score = score
        return best_score


def user_move(matrix: list[list[str]], free_cells: list[tuple[int, int]], player_turn: int) -> int:
    while True:
        try:
            coordinates = input('Enter the coordinates: ')
            if coordinates.strip() == '':
                raise EmptyInputError

            x, y = map(int, coordinates.split())
            x -= 1
            y -= 1
            if not (0 <= x <= 2) or not (0 <= y <= 2):
                raise CoordinatesError
            elif check_occupied_cell(matrix, x, y):
                raise OccupiedCellError
            else:
                matrix[x][y] = 'X' if player_turn % 2 == 1 else 'O'
                free_cells.remove((x, y))
                print_matrix(matrix)
                return player_turn + 1
        except ValueError:
            print('You should enter numbers!')
        except CoordinatesError as err:
            print(err)
        except OccupiedCellError as err:
            print(err)
        except EmptyInputError as err:
            print(err)


def ai_move(matrix: list[list[str]], free_cells: list[tuple[int, int]], difficulty: str, player_turn: int) -> int:
    if difficulty == 'easy':
        print('Making move level "easy"')
        ai_easy_move(free_cells, matrix, player_turn)
        return player_turn + 1
    elif difficulty == 'medium':
        print('Making move level "medium"')
        if player_turn % 2 == 1:
            player_symbol = 'X'
            opponent_symbol = 'O'
        else:
            player_symbol = 'O'
            opponent_symbol = 'X'

        if check_if_logic_move_is_possible(matrix, free_cells, player_symbol, opponent_symbol):
            return player_turn + 1
        else:
            ai_easy_move(free_cells, matrix, player_turn)
            return player_turn + 1
    elif difficulty == 'hard':
        print('Making move level "hard"')
        if player_turn % 2 == 1:
            player_symbol = 'X'
            opponent_symbol = 'O'
        else:
            player_symbol = 'O'
            opponent_symbol = 'X'
        best_score = -800
        best_move = (-1, -1)

        for x in range(3):
            for y in range(3):
                if matrix[x][y] == ' ':
                    matrix[x][y] = player_symbol
                    score = minimax(matrix, False, player_symbol, opponent_symbol)
                    matrix[x][y] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = x, y

        x, y = best_move
        matrix[x][y] = player_symbol
        free_cells.remove(best_move)
        print_matrix(matrix)
        return player_turn + 1


def choose_game_mode(player1: str, player2: str):
    matrix = [[' ' for _ in range(3)] for _ in range(3)]
    print_matrix(matrix)

    player_turn = 1
    free_cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    while True:
        if player1 == 'user':
            player_turn = user_move(matrix, free_cells, player_turn)
        elif player1 in difficulty:
            player_turn = ai_move(matrix, free_cells, player1, player_turn)
        if check_state_of_game(matrix)[0] is not None or not check_empty_cells_remaining(matrix):
            break
        if player2 == 'user':
            player_turn = user_move(matrix, free_cells, player_turn)
        elif player2 in difficulty:
            player_turn = ai_move(matrix, free_cells, player2, player_turn)
        if check_state_of_game(matrix)[0] is not None or not check_empty_cells_remaining(matrix):
            break

    is_completed, symbol = check_state_of_game(matrix)
    if is_completed is not None:
        print(f'{symbol} wins')
    elif not check_empty_cells_remaining(matrix):
        print('Draw')
    main()


def main():
    while True:
        command = input('Input command: ').split()
        if command[0] == 'exit':
            exit()
        elif len(command) != 3 or any(elem not in commands and elem not in difficulty for elem in command):
            print('Bad parameters!')
        else:
            choose_game_mode(command[1], command[2])


if __name__ == '__main__':
    main()
