# Application: Sea Battle
############################################################

import random


class Coordinate:
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_hit = False
        self.is_missed = False


class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.is_sunk = False

    def hit(self):
        self.is_sunk = all(coord.is_hit for coord in self.coordinates)


class Board:

    BOARD_SIZE = 6

    def __init__(self):
        self.ships = []
        self.grid = [[Coordinate(row, col) for col in range(1, self.BOARD_SIZE + 1)] for row in
                     range(1, self.BOARD_SIZE + 1)]
        self.computer_shots = set()
        self.place_ships()
        self.player_ships_sunk = 0
        self.computer_ships_sunk = 0

    def place_ships(self):

        ship_lengths = [3, 2, 2, 1, 1, 1, 1]  # number of ships and their lengths

        for length in ship_lengths:
            self.place_ship(length)

    def generate_ship_coordinates(self, length):
        max_attempts = 100  # the number of attempts
        for _ in range(max_attempts):
            start_row, start_col = random.randint(1, self.BOARD_SIZE), random.randint(1, self.BOARD_SIZE)
            direction = random.choice([Coordinate.HORIZONTAL, Coordinate.VERTICAL])

            if direction == Coordinate.HORIZONTAL:
                ship_coordinates = [Coordinate(start_row, start_col + i) for i in range(length)]
            else:
                ship_coordinates = [Coordinate(start_row + i, start_col) for i in range(length)]

            if self.is_valid_ship_placement(ship_coordinates):
                return ship_coordinates

        raise ValueError("Unable to find valid coordinates for the ship. Reduce ship density or increase board size.")

    # Check if we can place a ship at chosen coordinates, if not then choose coordinates again
    def is_valid_ship_placement(self, ship_coordinates):
        occupied_coordinates = set()

        for ship in self.ships:
            if not ship.is_sunk:
                occupied_coordinates.update((coord.row, coord.col) for coord in ship.coordinates)

        for coord in ship_coordinates:
            if (
                    not (1 <= coord.row <= self.BOARD_SIZE)
                    or not (1 <= coord.col <= self.BOARD_SIZE)
                    or (coord.row, coord.col) in occupied_coordinates
            ):
                return False

        # Additional check for minimum distance between ships

        for ship_coord in occupied_coordinates:
            for coord in ship_coordinates:
                if (
                        abs(ship_coord[0] - coord.row) <= 1
                        and abs(ship_coord[1] - coord.col) <= 1
                ):
                    return False

        return True

    def place_ship(self, length):
        while True:
            ship_coordinates = self.generate_ship_coordinates(length)
            if self.is_valid_ship_placement(ship_coordinates):
                ship = Ship(ship_coordinates)
                self.ships.append(ship)
                for coord in ship_coordinates:
                    self.grid[coord.row - 1][coord.col - 1] = coord
                break

    def display_result(self, coord, show_ships):
        if coord.is_hit:
            return " X |"  # Display "X" for hits
        elif coord.is_missed:
            return " T |"  # Display "T" for misses
        elif show_ships:
            ship_at_coord = next((ship for ship in self.ships if coord in ship.coordinates), None)
            if ship_at_coord:
                # Display ship using "X" or "■" based on whether it's hit or not:
                return " X |" if ship_at_coord.is_sunk else " ■ |"
        return " O |"  # Display "O" for empty spaces

    def display(self, show_ships=False):
        print("  |", " | ".join(str(i) for i in range(1, self.BOARD_SIZE + 1)), "|")
        for row in range(1, self.BOARD_SIZE + 1):
            row_str = f"{row} |"
            for col in range(1, self.BOARD_SIZE + 1):
                coord = self.grid[row - 1][col - 1]
                row_str += self.display_result(coord, show_ships)

            print(row_str)

    def take_shot(self, row, col, is_computer=False):
        coord = self.grid[row - 1][col - 1]

        if coord.is_hit or coord.is_missed:  # Check for both is_hit and is_missed
            raise ValueError("These coordinates are already taken, make a move again!")

        if is_computer:
            self.computer_shots.add((row, col))

        hit_ship = next((ship for ship in self.ships if coord in ship.coordinates), None)

        if hit_ship:
            coord.is_hit = True
            hit_ship.hit()

            if hit_ship.is_sunk:
                if is_computer:
                    self.player_ships_sunk += len(hit_ship.coordinates)
                else:
                    self.computer_ships_sunk += len(hit_ship.coordinates)
        else:
            coord.is_missed = True  # Set is_missed for missed shots

        return bool(hit_ship)

    def all_ships_sunk(self, is_computer=False):
        total_hits = sum(1 for ship in self.ships for coord in ship.coordinates if coord.is_hit)

        if is_computer:
            return total_hits == sum(len(ship.coordinates) for ship in self.ships) and self.player_ships_sunk == 0
        else:
            return total_hits == sum(len(ship.coordinates) for ship in self.ships) and self.computer_ships_sunk == 0


def get_user_input():
    try:
        row = int(input(f"Enter the row (1-{Board.BOARD_SIZE}) for your shot: "))
        col = int(input(f"Enter the column (1-{Board.BOARD_SIZE}) for your shot: "))
        if 1 <= row <= Board.BOARD_SIZE and 1 <= col <= Board.BOARD_SIZE:
            return row, col
        else:
            print(f"Invalid input. Row and column values must be between 1 and {Board.BOARD_SIZE}.")
            return get_user_input()
    except ValueError:
        print("Invalid input. Please enter correct integer values.")
        return get_user_input()


def main():
    player_board = Board()
    computer_board = Board()

    while True:
        print("\nPlayer's Board:")
        player_board.display(show_ships=True)

        print("\nComputer's Board:")
        computer_board.display(show_ships=False)

        while True:
            row, col = get_user_input()

            try:
                hit = computer_board.take_shot(row, col)
            except ValueError as e:
                print(e)
                continue

            if hit:

                print("\nPlayer's Board:")
                player_board.display(show_ships=True)

                print("\nComputer's Board:")
                computer_board.display(show_ships=False)
            
                print("Player hits at", row, col)
            else:
                print("Player misses at", row, col)
                break  # Break out of the loop if the player misses

        if computer_board.all_ships_sunk(is_computer=True):
            print("\nPlayer's Board:")
            player_board.display(show_ships=True)

            print("\nComputer's Board:")
            computer_board.display(show_ships=True)

            print("Congratulations! You've won!")
            break

        while True:
            computer_row, computer_col = random.randint(1, Board.BOARD_SIZE), random.randint(1, Board.BOARD_SIZE)

            while (computer_row, computer_col) in player_board.computer_shots:
                computer_row, computer_col = random.randint(1, Board.BOARD_SIZE), random.randint(1, Board.BOARD_SIZE)

            try:
                hit = player_board.take_shot(computer_row, computer_col, is_computer=True)
            except ValueError:
                continue

            if hit:

                print("\nPlayer's Board:")
                player_board.display(show_ships=True)

                print("\nComputer's Board:")
                computer_board.display(show_ships=False)
            
                print("Computer hits at", computer_row, computer_col)
            else:
                print("Computer misses at", computer_row, computer_col)
                break # Break out of the loop if the computer misses

        if player_board.all_ships_sunk(is_computer=False):

            print("\nPlayer's Board:")
            player_board.display(show_ships=True)

            print("\nComputer's Board:")
            computer_board.display(show_ships=True)

            print("Sorry, you've lost. Try again!")
            break


if __name__ == "__main__":
    main()
