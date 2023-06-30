class CoordinatesError(Exception):
    def __str__(self):
        return 'Coordinates should be from 1 to 3!'


class OccupiedCellError(Exception):
    def __str__(self):
        return 'This cell is occupied! Choose another one!'


class EmptyInputError(Exception):
    def __str__(self):
        return 'You should enter numbers!'
