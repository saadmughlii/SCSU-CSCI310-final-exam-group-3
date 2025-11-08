import threading, random, time

# --- Game setup ---
SIZE = 5
board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
numbers = [(r, c) for r in range(SIZE) for c in range(SIZE)]
game_over = False

lock = threading.Lock()
barrier = threading.Barrier(4)  # 4 threads = 4 players

# Track each player’s position
positions = {"B": None, "T": None, "M": None, "D": None}

# --- Helper functions ---
def print_board():
    for row in board:
        print(' | '.join(row))
        print('-' * (SIZE * 4 - 3))
    print()

def check_winner(player):
    # Simple placeholder — customize this rule if needed
    return False

def pick_number(player):
    global game_over

    while not game_over:
        with lock:
            if not numbers:
                print("Game Over! It's a draw.")
                game_over = True
                break

            # Pick random empty cell
            choice = random.choice(numbers)
            print(choice)
            numbers.remove(choice)

            # Clear old position
            if positions[player] is not None:
                old_r, old_c = positions[player]
                board[old_r][old_c] = ' '

            # Move to new cell
            r, c = choice
            board[r][c] = player
            positions[player] = (r, c)

        # Wait for all 4 players to move before printing
        barrier.wait()

        # Print the board once per full cycle
        if barrier.broken or barrier.n_waiting == 0:
            with lock:
                print(f"\n=== All players moved! ===")
                print_board()

        # Check for win (optional rule)
        if check_winner(player):
            print(f"Game Over! Player {player} wins!")
            game_over = True
            break

        time.sleep(1)

# --- Start threads ---
players = ["B", "T", "M", "D"]
threads = [threading.Thread(target=pick_number, args=(p,)) for p in players]

for t in threads:
    t.start()

for t in threads:
    t.join()
