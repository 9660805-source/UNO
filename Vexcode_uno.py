# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Project:       VEX EXP UNO Robot (Physical Navigation & Game Logic)        #
# 	Module:        main.py                                                     #
# 	Author:        VEXcode EXP                                                 #
# 	Created:       2026                                                        #
# 	Description:   Tracks game state with Brain buttons and executes physical   #
# 	               driving broadcasts to draw/discard cards at table center.   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# --- Physical Drive & Turn Helpers ---
FORWARD_DIST_UNITS = 2  # Standard distance units to center (adjust for table size)
TURN_ANGLE_DEGREES = 90  # Standard turn angle

def robot_drive_forward(units=FORWARD_DIST_UNITS):
    """Executes broadcast/command to drive robot forward."""
    print("--> BROADCAST: Driving Forward (%d units)" % units)
    # Put physical drivetrain code or broadcast here, e.g.:
    # drivetrain.drive_for(FORWARD, units * 100, MM)
    wait(1, SECONDS)

def robot_turn_left(angle=TURN_ANGLE_DEGREES):
    """Executes broadcast/command to turn left."""
    print("--> BROADCAST: Turning Left (%d degrees)" % angle)
    # drivetrain.turn_for(LEFT, angle, DEGREES)
    wait(1, SECONDS)

def robot_turn_right(angle=TURN_ANGLE_DEGREES):
    """Executes broadcast/command to turn right."""
    print("--> BROADCAST: Turning Right (%d degrees)" % angle)
    # drivetrain.turn_for(RIGHT, angle, DEGREES)
    wait(1, SECONDS)

# --- Physical Routine Functions ---

def move_to_center_and_discard(played_card):
    """Drives to table center, drops physical card onto pile, and returns."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("DRIVING CENTER...")
    
    # 1. Drive out to center discard pile
    robot_drive_forward(FORWARD_DIST_UNITS)
    
    # 2. Action at center
    brain.screen.set_cursor(3, 1)
    brain.screen.print("DISCARDING...")
    print("--> ROBOT AT CENTER: Dropping card '%s'" % played_card)
    wait(1.5, SECONDS)
    
    # 3. Turn around (180 deg) and drive back to player position
    robot_turn_right(90)
    robot_turn_right(90)
    robot_drive_forward(FORWARD_DIST_UNITS)
    
    # 4. Turn back around to face table center
    robot_turn_right(90)
    robot_turn_right(90)

def move_to_center_and_draw(count=1):
    """Drives to table center, picks up drawn card(s), and returns to player."""
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("DRIVING CENTER...")
    
    # 1. Drive out to center draw pile
    robot_drive_forward(FORWARD_DIST_UNITS)
    
    # 2. Action at center
    brain.screen.set_cursor(3, 1)
    brain.screen.print("DRAWING +%d..." % count)
    print("--> ROBOT AT CENTER: Drawing %d card(s) from deck" % count)
    wait(1.5, SECONDS)
    
    # 3. Return to player base
    robot_turn_left(90)
    robot_turn_left(90)
    robot_drive_forward(FORWARD_DIST_UNITS)
    
    # 4. Re-orient to face forward
    robot_turn_left(90)
    robot_turn_left(90)

# --- Deck & Card Game Logic ---
COLORS = ['Red', 'Yellow', 'Green', 'Blue']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2', '+4']

def shuffle_list(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = urandom.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

def create_deck():
    deck = []
    for color in COLORS:
        deck.append("%s 0" % color)
        for val in VALUES[1:13]:
            deck.append("%s %s" % (color, val))
            deck.append("%s %s" % (color, val))
    for _ in range(4):
        deck.append("Wild")
        deck.append("Wild +4")
    return deck

def draw_card(deck):
    if len(deck) > 0:
        return deck.pop(0)
    return None

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

def shorten_card_name(card_str):
    res = card_str.replace("Yellow", "Yel")
    res = res.replace("Green", "Grn")
    res = res.replace("Blue", "Blu")
    res = res.replace("Reverse", "Rev")
    return res

# --- Screen UI & Button Navigation ---

def render_hand_page(hand, header_text, page, total_pages):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    head = "%s (%d)" % (header_text[:8], len(hand))
    brain.screen.print("%-10s P%d/%d" % (head, page + 1, total_pages))
    
    start_idx = page * 6
    for r in range(3):
        row_num = r + 2
        brain.screen.set_cursor(row_num, 1)
        c1_idx = start_idx + (r * 2)
        c2_idx = c1_idx + 1
        
        c1_str = "%d:%s" % (c1_idx + 1, shorten_card_name(hand[c1_idx])) if c1_idx < len(hand) else ""
        c2_str = "%d:%s" % (c2_idx + 1, shorten_card_name(hand[c2_idx])) if c2_idx < len(hand) else ""
        
        line = "%-8s %-7s" % (c1_str[:8], c2_str[:7])
        brain.screen.print(line[:16])
        
    brain.screen.set_cursor(5, 1)
    brain.screen.print("L/R:Pg  [V]:Turn")

def display_full_hand(hand, header_text="BOT HAND"):
    page = 0
    total_pages = (len(hand) + 5) // 6 if len(hand) > 0 else 1
    render_hand_page(hand, header_text, page, total_pages)
    
    while True:
        wait(50, MSEC)
        if brain.buttonLeft.pressing():
            page = (page - 1) % total_pages
            render_hand_page(hand, header_text, page, total_pages)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            page = (page + 1) % total_pages
            render_hand_page(hand, header_text, page, total_pages)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return

def render_picker_screen(hand, playable_indices, selected_idx, top_card):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(("TOP:" + shorten_card_name(top_card))[:16])
    
    brain.screen.set_cursor(3, 1)
    card_name = hand[selected_idx]
    is_legal = selected_idx in playable_indices
    status_symbol = "[OK]" if is_legal else "[X]"
    
    line = "< %s > %s" % (shorten_card_name(card_name), status_symbol)
    brain.screen.print(line[:16])
    
    brain.screen.set_cursor(5, 1)
    if is_legal:
        brain.screen.print("L/R:Nav [V]:PLAY")
    else:
        brain.screen.print("L/R:Nav (ILLEGAL)")

def choose_card_to_play(hand, playable_indices, top_card):
    selected_idx = playable_indices[0]
    render_picker_screen(hand, playable_indices, selected_idx, top_card)
    
    while True:
        wait(50, MSEC)
        if brain.buttonLeft.pressing():
            selected_idx = (selected_idx - 1) % len(hand)
            render_picker_screen(hand, playable_indices, selected_idx, top_card)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            selected_idx = (selected_idx + 1) % len(hand)
            render_picker_screen(hand, playable_indices, selected_idx, top_card)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            if selected_idx in playable_indices:
                while brain.buttonCheck.pressing():
                    wait(20, MSEC)
                return selected_idx
            else:
                brain.screen.set_cursor(5, 1)
                brain.screen.print("CANNOT PLAY THIS")
                wait(500, MSEC)
                render_picker_screen(hand, playable_indices, selected_idx, top_card)

def render_option_screen(prompt_title, option_str):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print(prompt_title[:16])
    brain.screen.set_cursor(3, 1)
    brain.screen.print("< " + option_str + " >")
    brain.screen.set_cursor(5, 1)
    brain.screen.print("L/R:Nav [V]:OK")

def select_option_with_buttons(options, prompt_title):
    selected_idx = 0
    render_option_screen(prompt_title, options[selected_idx])
    
    while True:
        wait(50, MSEC)
        if brain.buttonLeft.pressing():
            selected_idx = (selected_idx - 1) % len(options)
            render_option_screen(prompt_title, options[selected_idx])
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            selected_idx = (selected_idx + 1) % len(options)
            render_option_screen(prompt_title, options[selected_idx])
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return options[selected_idx]

def input_top_card_via_buttons():
    color = select_option_with_buttons(COLORS + ['Wild/Penalty'], "SELECT COLOR")
    if color == 'Wild/Penalty':
        special = select_option_with_buttons(['Wild', '+2', '+4'], "SELECT TYPE")
        return special
    else:
        val = select_option_with_buttons(VALUES, "SELECT VALUE")
        return color + " " + val

# --- Game Loop ---

def play_physical_game():
    robot_deck = create_deck()
    shuffle_list(robot_deck)
    
    bot_hand = [draw_card(robot_deck) for _ in range(7)]
    display_full_hand(bot_hand, "START HAND")
    
    turn = 1
    while len(bot_hand) > 0:
        top_card = input_top_card_via_buttons()
        
        # Draw Penalty Handling
        if top_card == "+2":
            move_to_center_and_draw(2)
            for _ in range(2):
                d = draw_card(robot_deck)
                if d: bot_hand.append(d)
            display_full_hand(bot_hand, "CURR HAND")
            turn += 1
            continue
        elif top_card == "+4":
            move_to_center_and_draw(4)
            for _ in range(4):
                d = draw_card(robot_deck)
                if d: bot_hand.append(d)
            display_full_hand(bot_hand, "CURR HAND")
            turn += 1
            continue
            
        playable_indices = [i for i, c in enumerate(bot_hand) if is_card_legal(c, top_card)]
        
        if len(playable_indices) > 0:
            chosen_idx = choose_card_to_play(bot_hand, playable_indices, top_card)
            played_card = bot_hand.pop(chosen_idx)
            top_card = played_card
            
            # Physical drive out to discard card
            move_to_center_and_discard(played_card)
        else:
            # Physical drive out to draw card
            move_to_center_and_draw(1)
            drawn = draw_card(robot_deck)
            if drawn:
                bot_hand.append(drawn)
                if is_card_legal(drawn, top_card):
                    playable_indices = [len(bot_hand) - 1]
                    chosen_idx = choose_card_to_play(bot_hand, playable_indices, top_card)
                    played_card = bot_hand.pop(chosen_idx)
                    top_card = played_card
                    move_to_center_and_discard(played_card)
            
        if len(bot_hand) == 0:
            break
            
        display_full_hand(bot_hand, "CURR HAND")
        turn += 1

    # Winner Screen
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("ROBOT WINS!")
    brain.screen.set_cursor(4, 1)
    brain.screen.print("HAND EMPTY")

# Run program
play_physical_game()