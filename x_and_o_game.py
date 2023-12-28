#Игра «Крестики-нолики»
##########################################################################

def create_a_board(board):
    print("  0   1   2")
    for i, row in enumerate(board):
        print(f"{i} {'   '.join(cell if cell != ' ' else '-' for cell in row)}")

def check_if_move_is_correct(board, row, col):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '-'

def check_winner(board):
    # Проверка по горизонтали и вертикали:
    for i in range(3):
        if all(cell == 'x' for cell in board[i]) or all(board[j][i] == 'x' for j in range(3)):
            return 'x'
        elif all(cell == 'o' for cell in board[i]) or all(board[j][i] == 'o' for j in range(3)):
            return 'o'

    # Проверка по диагоналям:
    if all(board[i][i] == 'x' for i in range(3)) or all(board[i][2 - i] == 'x' for i in range(3)):
        return 'x'
    elif all(board[i][i] == 'o' for i in range(3)) or all(board[i][2 - i] == 'o' for i in range(3)):
        return 'o'

    return None

def check_if_board_is_full(board):
    return all(cell != '-' for row in board for cell in row)

def print_result(winner):
    if winner:
        print(f"Игрок, игравший {winner}-иками, мои поздравления, ты победитель!")
        if winner != 'x':
            print(f"Игрок, игравший x-иками, не отчаивайся, в следующий раз тебе повезёт!")
        else:
            print(f"Игрок, игравший o-иками, не отчаивайся, в следующий раз тебе повезёт!")
    else:
        print("Ничья! Победила дружба!")

def play_x_and_o_game():

    print('Игра «Крестики-нолики»:')
    print('Правила игры:')
    print('1. Игровое поле представлено матрицей 3x3.')
    print('2. Игроки ходят поочередно, вводя номер строки и столбца для своего хода.')
    print('3. Ходы обозначаются символами "x" и "o".')
    print('4. Побеждает игрок, который соберет три своих символа в ряд по горизонтали, вертикали или диагонали.')
    print('5. Если все клетки заполнены, и нет победителя, игра завершается ничьей.')

    confirm = input('Если вы готовы начать игру, введите "Y": ')
    if confirm.lower() == 'y':
        print('Запасайтесь попкорном, игра «Крестики-нолики» начинается!')

        board = [['-' for _ in range(3)] for _ in range(3)]
        current_player = 'x'

        while True:
            create_a_board(board)

            row = int(input(f"Игрок, играющий {current_player}-иками, введите номер строки: "))
            col = int(input(f"Игрок, играющий {current_player}-иками, введите номер столбца: "))

            if check_if_move_is_correct(board, row, col):
                board[row][col] = current_player
                winner = check_winner(board)

                if winner or check_if_board_is_full(board):
                    create_a_board(board)
                    print_result(winner)
                    break

                current_player = 'o' if current_player == 'x' else 'x'
            else:
                print("Неверный ход. Попробуйте снова!")

    else:
        print('Игра отменена.')

# Запускаем игру:
play_x_and_o_game()