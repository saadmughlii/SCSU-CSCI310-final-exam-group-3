import threading, random, time
from character import Character

# --- Game setup ---
BOARD_SIZE = 5
CARROT_SYMBOL = "C"
MOUNTAIN_SYMBOL = "F"
NUM_CARROTS = 2

# Mountain location
mountain_location = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]

# Carrot locations (cannot be on mountain)
def get_free_location(exclude_locations):
    while True:
        pos = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        if pos not in exclude_locations:
            return pos

carrot_locations = []
exclude = [mountain_location]
for _ in range(NUM_CARROTS):
    pos = get_free_location(exclude)
    carrot_locations.append(pos)
    exclude.append(pos)

# Board initialization
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
board[mountain_location[0]][mountain_location[1]] = MOUNTAIN_SYMBOL
for c in carrot_locations:
    board[c[0]][c[1]] = CARROT_SYMBOL


def barrier_action():
    with lock:
        # Restore mountain
        board[mountain_location[0]][mountain_location[1]] = MOUNTAIN_SYMBOL
        # Restore carrots
        for c in carrot_locations:
            board[c[0]][c[1]] = CARROT_SYMBOL
        # Update all player positions
        for pid in player_ids:
            r, c = current_locations[pid]
            board[r][c] = players[pid].name
        print("\n=== All players moved! ===")
        print_board()



game_over = False
lock = threading.Lock()
barrier = threading.Barrier(4, action=barrier_action)

# --- Initialize players ensuring no overlap with mountain or carrots ---
current_locations = {"mountain": mountain_location}
player_ids = ["B", "T", "M", "D"]
players = {}

for pid in player_ids:
    pos = get_free_location(exclude + list(current_locations.values()))

    current_locations[pid] = pos
    players[pid] = Character(pos[0], pos[1], pid, BOARD_SIZE)
    board[pos[0]][pos[1]] = pid

# --- Helper functions ---
def print_board():
    for row in board:
        print(' | '.join(row))
        print('-' * (BOARD_SIZE * 4 - 3))
    print()

def check_winner(character):
    # Winning condition: player with at least 1 carrot jumps on mountain
    return character.has_carrot and [character.row, character.column] == mountain_location

def get_valid_moves(character):
    # generate all potential moves
    moves = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row = max(0, min(character.row + dr, BOARD_SIZE - 1))
            new_col = max(0, min(character.column + dc, BOARD_SIZE - 1))
            # Check mountain collision: only allow if character has carrot
            if [new_row, new_col] == mountain_location and not character.has_carrot:
                continue
            # Check other players collision
            if [new_row, new_col] in [current_locations[p] for p in player_ids if p != character.name[0]]:
                continue
            moves.append([new_row, new_col])
    return moves





# --- Game loop for each player ---
def take_turn(player_id):
    global game_over, carrot_locations
    character = players[player_id]

    while not game_over:
        with lock:
            prev_row, prev_col = current_locations[player_id]

            # Decide move
            if random.random() < 0.8:
                moves = get_valid_moves(character)
                if moves:
                    new_pos = random.choice(moves)
                    character.row, character.column = new_pos
            else:
                # Teleport safely
                while True:
                    new_row = random.randint(0, BOARD_SIZE - 1)
                    new_col = random.randint(0, BOARD_SIZE - 1)
                    if [new_row, new_col] == mountain_location and not character.has_carrot:
                        continue
                    if [new_row, new_col] in [current_locations[p] for p in player_ids if p != player_id]:
                        continue
                    character.row, character.column = new_row, new_col
                    break

            # Check for carrot pickup
            for carrot in carrot_locations:
                if [character.row, character.column] == carrot:
                    character.pick_carrot()
                    print(f"{character.name} picked up a carrot!")
                    carrot_locations.remove(carrot)
                    break

            # Update current location
            current_locations[player_id] = [character.row, character.column]

            # Clear old position
            if prev_row != character.row or prev_col != character.column:
                board[prev_row][prev_col] = ' '

        # Wait for all players — the barrier action will print the board
        barrier.wait()

        # Check winner
        if check_winner(character):
            with lock:
                print(f"Game Over! Player {character.name} wins by reaching the mountain with a carrot!")
            game_over = True
            break

        time.sleep(1)


        # Check winner
        if check_winner(character):
            with lock:
                print(f"Game Over! Player {character.name} wins by reaching the mountain with a carrot!")
            game_over = True
            break

        time.sleep(1)

# --- Start threads ---
threads = [threading.Thread(target=take_turn, args=(pid,)) for pid in player_ids]
for t in threads:
    t.start()
for t in threads:
    t.join()
