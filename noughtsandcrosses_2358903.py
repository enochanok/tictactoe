import json
import random
from os.path import exists
random.seed()


def draw_board(board):

    """
      functionName: draw_board
       Prints board in a 3x3 grid with dashes(-) and pipes(|)
      """
    print('-------------')
    for row in board:  # iterates rows in board
        temp = '| '
        for mark in row:  # iterates every mark in row
            temp += mark + ' | '
        print(temp)
        print('-------------')


def welcome(board):
    """
    functionName: welcome
    prints a blank board
    """
    print("Welcome to the 'Unbeatable Noughts and Crosses' game.")
    print("The board layout is shown below:")
    draw_board(board)
    print('When prompted, enter the number of corresponding to the square you want.')


def initialise_board(board):
    """
    functionName: initialise_board
    :return: board
    """
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    return board


def get_player_move(board):
    """
    functionName: get_player_move
    prompt user to input the number
    :return: row and column through conversion
    """
    while True:
        playerChoice = input('''
                       1  2  3
                       4  5  6
   Choose your square: 7  8  9 : ''')
        if not playerChoice.isdigit():  # handles non numbers
            print('Invalid Input. Enter a Number.')
            continue
        if not 1 <= int(playerChoice) <= 9:  # handles all numbers except < 1 and > 9
            print('Invalid Input. Please enter number between (1-9)')
            continue
        row = (int(playerChoice) - 1) // 3  # conversion to row
        col = (int(playerChoice) - 1) % 3  # conversion to column
        playerPosition = board[row][col]
        if not playerPosition == ' ':  # checks if user's choice is empty or not
            print('Please choose an empty space.')
            return None, None
        return row, col


def choose_computer_move(board):
    """
    functionName: choose_computer_move
    generate random computer's move in a list of empty spaces
    :return: row and column
    """
    emptyPosition = []
    boardLength = len(board)
    for i in range(boardLength):
        for j in range(boardLength):
            if board[i][j] == ' ':
                emptyPosition.append([i, j])
    choice = random.choice(emptyPosition)  # choose empty space randomly
    row = choice[0]
    col = choice[1]
    return row, col


def check_for_win(board, mark):
    """
    functionName: check_for_win

    :param board:
    :param mark:
    :return: won or lose
    """
    boardLength = len(board)
    for i in range(boardLength):  # iterate over rows
        rowWin, colWin = True, True  # Check rows and columns
        for j in range(boardLength):  # iterate over marks
            if board[i][j] != mark:
                rowWin = False
            if board[j][i] != mark:
                colWin = False
        if rowWin or colWin:
            return True
    firstDiagonalWins, secondDiagonalWins = True, True  # Check diagonals
    for i in range(boardLength):  # iterate over rows
        if board[i][i] != mark:
            firstDiagonalWins = False
        if board[i][boardLength - i - 1] != mark:
            secondDiagonalWins = False
    if firstDiagonalWins or secondDiagonalWins:
        return True
    return False


def check_for_draw(board):
    """
    functionName: check_for_draw
    :return: isDrawn
    """

    for row in board:  # iterates over rows
        if ' ' in row:  # checks if mark is empty or not
            return False
    return True


def play_game(board):
    """
    functionName: play_game


    :return: Either player won(1) or computer won(-1), else draw (0)
    """
    playerInput = False
    isMatchRunning = True
    board = initialise_board(board)
    welcome(board)
    while isMatchRunning:
        while not playerInput:
            playerRow, playerColumn = get_player_move(board)
            if (playerRow, playerColumn) == (None, None):
                continue
            board[playerRow][playerColumn] = 'X'
            draw_board(board)
            break
        if check_for_win(board, 'X'):  # check if win
            print('Congratulation, You won.')
            draw_board(board)
            return 1
        if check_for_draw(board):
            draw_board(board)
            print("It's a draw.")  # check if draw
            return 0
        computerRow, computerColumn = choose_computer_move(board)
        board[computerRow][computerColumn] = 'O'
        print('''Computer's move is''')
        draw_board(board)
        if check_for_win(board, 'O'):  # check if win
            print("Sorry you lost.")
            draw_board(board)
            return -1
        if check_for_draw(board):  # check if win
            draw_board(board)
            print("It's a draw.")
            return 0
                    
                
def menu():
    """
    functionName: menu
    It prompts user to enter any 4 options. i.e. 1, 2, 3, q.
    Each options call functions accordingly
    """
    while True:
        choice = input('''
        Enter one of the following options:
            1 - Play the game
            2 - Save your score in the leaderboard
            3 - Load and display the leaderboard
            q - End the program
        1, 2, 3, or q: ''')
        if choice.lower() in ['1', '2', '3', 'q']:
            return choice.lower()
        print('''\nPlease select valid options''')


def load_scores():
    """
    functionName: load_scores
    :return:
    """
    leaderboard = {}
    if not exists('leaderboard.txt'):
        print("Leaderboard does not exists.")
        with open('leaderboard.txt', 'w', encoding='utf-8') as newFile:
            print('Creating a new leaderboard')
            json.dump({}, newFile)
    with open('leaderboard.txt', 'r', encoding='utf-8') as readFile:
        line = readFile.read()
    try:
        leaderboard = json.loads(line)  # loads all names and score in leaderboard
    except json.JSONDecodeError:  # if leaderboard does not have object
        with open('leaderboard.txt', 'w', encoding='utf-8') as writeFile:
            json.dump({}, writeFile)
    return leaderboard


def save_score(score):
    """
    functionName: save_score
    Prompt player to enter their name
    Class load_scores() function to load all the scores
    """
    playerName = input("Enter your name: ").strip().lower()
    leaderboard = load_scores()
    allPlayers = leaderboard.keys()
    if playerName in allPlayers:
        oldScore = leaderboard[playerName]
        newScore = oldScore + score
        leaderboard[playerName] = newScore
    else:
        leaderboard[playerName] = score
    with open('leaderboard.txt', 'w', encoding='utf-8') as writeFile:
        json.dump(leaderboard, writeFile)
        print("Saved Successfully.")


def display_leaderboard(leaders):
    """
    function name: display_leaderboard
    :return: the list of the players and score in console.
    """

    print("\nLEADERBOARD")
    print('{:<10} {:<10}'.format('Name', 'Score'))
    print('--------------------')
    if leaders == {}:  # empty leaderboard
        print('No leaders in board yet')
    else:
        for name, score in leaders.items():
            print('{:<10} {:<10}'.format(name, score))
    print('--------------------')
