import random
import threading
import time

# Global variables
board_layout = [' '] * 25           # 5x5 game board
lock = threading.Lock()
game_over = False
numbers = list(range(0, 25))  # number of spots available in game board
mountain_location = 0
carrot_locations = [0,0,0,0] #there will be 5 carrots on the board


# Winning combinations (indices)
win_conditions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
    [0, 4, 8], [2, 4, 6]              # diagonals
]

def check_winner(player):
    """Check if the given player ('X' or 'O') has won."""
    for combo in win_conditions: # iterate through each list in win_conditions
        if all(board_layout[i] == player for i in combo): # Check if all values at the given indices
                                                            # in board_layout match the player's name
            return True
    return False


def pick_number(player):
    """Thread function: player makes random moves until game ends."""
    global numbers, game_over
    while not game_over:
        with lock:  # only one thread at a time can access the list
            if game_over:
                break

            # Find available moves
            available = [i for i, cell in enumerate(board_layout) if cell == ' ']
            if not available:
                print("Game Over! It's a draw.")
                game_over = True
                break

            # Player picks a random move
            choice = random.choice(numbers)
            numbers.remove(choice)
            board_layout[choice] = player
            print(f"{player} picked {choice}, remaining: {numbers}")
            print_board()

            # Check for win
            if check_winner(player):
                print(f"Game Over! Player {player} wins!")
                game_over = True
                break

        time.sleep(1)  # Small delay so threads alternate

def print_board():
    global board_layout
    # Print the board
    print("\nGame board:")
    for i in range(0, 24, 5):  #Take a number from 0 to 24 every 5 steps, excluding 9
        print(" | ".join(board_layout[i:i + 5]))
        if i < 20:
            print("-" * 17)  # Print a separator line
    print() # print new line

def main():
    #bugs bunny :)
    b = threading.Thread(target=pick_number, args=("B",))  # creating a thread object that will run pick_number function
    
    #taz devil >:)
    d = threading.Thread(target=pick_number, args=("D",))
    
    #tweety :>
    
    t = threading.Thread(target=pick_number, args=("T",))
    
    #marvin the martian (8)
    m = threading.Thread(target=pick_number, args=("M",))

    b.start()  # this activates the thread
    d.start()
    t.start()
    m.start()

    b.join()  # this will wait for b to finish before proceeding
    d.join()
    t.join()
    m.join()

    return 0


if __name__ == "__main__":
    main()
