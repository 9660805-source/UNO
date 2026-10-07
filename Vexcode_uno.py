# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Project:       VEX EXP Interactive Multi-Player UNO                        #
# 	Module:        main.py                                                     #
# 	Author:        VEXcode EXP                                                 #
# 	Created:       2026                                                        #
# 	Description:   Interactive 2-Player turn loop with human input prompts     #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# --- Custom Random Generator ---
def shuffle_list(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = urandom.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

# --- Deck Setup ---
COLORS = ['Red', 'Yellow', 'Green', 'Blue']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
WILD_CARDS = ['Wild', 'Wild +4']

def create_deck():
    deck = []
    for color in COLORS:
        deck.append("%s 0" % color)
        for val in VALUES[1:]:
            deck.append("%s %s" % (color, val))
            deck.append("%s %s" % (color, val))
    for wild in WILD_CARDS:
        for _ in range(4):
            deck.append(wild)
    return deck

def draw_card(deck):
    if len(deck) > 0:
        return deck.pop(0)
    return None

def start_game(deck, hand_size=7):
    hand = []
    for _ in range(hand_size):
        card = draw_card(deck)
        if card:
            hand.append(card)
    return hand

def setup_top_card(deck):
    top_card = draw_card(deck)
    while "Wild" in top_card and len(deck) > 0:
        deck.append(top_card)
        shuffle_list(deck)
        top_card = draw_card(deck)
    return top_card

# --- Legal Move Checker ---

def is_card_legal(card, top_card):
    if "Wild" in card:
        return True
    
    card_parts = card.split(" ")
    top_parts = top_card.split(" ")
    
    if card_parts[0] == top_parts[0]:
        return True
    if len(card_parts) > 1 and len(top_parts) > 1 and card_parts[1] == top_parts[1]:
        return True
        
    return False

def get_legal_moves(hand, top_card):
    legal_indices = []
    for idx in range(len(hand)):
        if is_card_legal(hand[idx], top_card):
            legal_indices.append(idx)
    return legal_indices

# --- Display & Pacing (Strict 5 Rows x 16 Columns) ---

def shorten_card_name(card_str):
    res = card_str.replace("Yellow", "Yel")
    res = res.replace("Green", "Grn")
    res = res.replace("Blue", "Blu")
    res = res.replace("Reverse", "Rev")
    return res

def show_turn_banner(player_num):
    """Hides previous player's hand so players can pass the robot/terminal."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(3, 1)
    brain.screen.print(" PASS TO P%d    " % player_num)
    brain.screen.set_cursor(4, 1)
    brain.screen.print("================")
    wait(2, SECONDS)

def render_interactive_screen(player_num, top_card, hand, legal_indices):
    brain.screen.clear_screen()
    
    # Row 1: Player & Top Card
    brain.screen.set_cursor(1, 1)
    p_str = "P%d TOP:%s" % (player_num, shorten_card_name(top_card))
    brain.screen.print(p_str[:16])
    
    # Rows 2 & 3: Turn Instructions
    brain.screen.set_cursor(2, 1)
    if len(legal_indices) == 0:
        brain.screen.print("NO LEGAL CARDS")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("MUST DRAW CARD")
    else:
        brain.screen.print("LEGAL: %d CARDS" % len(legal_indices))
        brain.screen.set_cursor(3, 1)
        brain.screen.print("ENTER SELECTION")
        
    # Rows 4 & 5: Player Hand Size
    brain.screen.set_cursor(4, 1)
    brain.screen.print("Hand: %d cards" % len(hand))
    brain.screen.set_cursor(5, 1)
    brain.screen.print("Input in Term")

# --- Manual Input Turn Execution ---

def execute_player_turn(player_num, hand, deck, top_card):
    show_turn_banner(player_num)
    legal_indices = get_legal_moves(hand, top_card)
    
    render_interactive_screen(player_num, top_card, hand, legal_indices)
    
    print("\n" * 5) # Clear console space
    print("========================================")
    print("--- PLAYER %d'S TURN ---" % player_num)
    print("TOP CARD: %s" % top_card)
    print("YOUR HAND:")
    for idx, card in enumerate(hand, 1):
        status = "[LEGAL]" if (idx - 1) in legal_indices else "[CANNOT PLAY]"
        print("  %d. %s %s" % (idx, card, status))
    print("----------------------------------------")
    
    if len(legal_indices) == 0:
        print("--> No playable cards. Press Enter to draw a card.")
        input("Press Enter: ")
        
        drawn_card = draw_card(deck)
        if drawn_card:
            hand.append(drawn_card)
            print("--> Player %d drew: %s" % (player_num, drawn_card))
            
            # Allow player to immediately play the drawn card if legal
            if is_card_legal(drawn_card, top_card):
                print("--> Drawn card is legal! Playing %s" % drawn_card)
                hand.pop()
                return drawn_card
        
        wait(1.5, SECONDS)
        return top_card
    else:
        # Prompt human player for choice
        valid_choice = False
        selected_card_idx = -1
        
        while not valid_choice:
            try:
                raw_input = input("Player %d, choose card number to play: " % player_num)
                choice_num = int(raw_input) - 1
                
                if choice_num in legal_indices:
                    selected_card_idx = choice_num
                    valid_choice = True
                else:
                    print("Invalid move! Pick a number marked as [LEGAL].")
            except ValueError:
                print("Please enter a valid number from your hand list.")
                
        played_card = hand.pop(selected_card_idx)
        print("--> Player %d played: %s" % (player_num, played_card))
        wait(1.5, SECONDS)
        return played_card

# --- Multi-Player Game Loop ---

def play_multiplayer_game():
    uno_deck = create_deck()
    shuffle_list(uno_deck)
    
    p1_hand = start_game(uno_deck, 7)
    p2_hand = start_game(uno_deck, 7)
    
    top_card = setup_top_card(uno_deck)
    current_player = 1
    
    while len(p1_hand) > 0 and len(p2_hand) > 0 and len(uno_deck) > 0:
        if current_player == 1:
            top_card = execute_player_turn(1, p1_hand, uno_deck, top_card)
            if len(p1_hand) == 0:
                break
            current_player = 2
        else:
            top_card = execute_player_turn(2, p2_hand, uno_deck, top_card)
            if len(p2_hand) == 0:
                break
            current_player = 1

    # Winner Display
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    
    if len(p1_hand) == 0:
        brain.screen.print("PLAYER 1 WINS!")
        print("\n=== GAME OVER: PLAYER 1 WINS! ===")
    elif len(p2_hand) == 0:
        brain.screen.print("PLAYER 2 WINS!")
        print("\n=== GAME OVER: PLAYER 2 WINS! ===")
    else:
        brain.screen.print("DECK EMPTY - DRAW")
        print("\n=== GAME OVER: DECK IS EMPTY ===")

# Run program
play_multiplayer_game()