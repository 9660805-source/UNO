# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Project:       VEX EXP UNO Robot (Physical Drive & Pixel Graphics)         #
# 	Module:        main.py                                                     #
# 	Author:        VEXcode EXP                                                 #
# 	Created:       2026                                                        #
# 	Description:   Integrated card rendering graphics, driving privacy screens, #
# 	               and multi-card draw animations.                             #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# --- Custom Hardware-Safe Random Shuffle ---
def shuffle_list(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = urandom.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

# --- Custom Graphical Card Display Function ---

def draw_card_full_screen(card_str, color_code):
    brain.screen.clear_screen()
    if color_code == 'R': brain.screen.set_fill_color(Color.RED)
    elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
    elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
    elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
    else: brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    for i in range(5):
        brain.screen.draw_rectangle(0+i, 0+i, 159-(i*2), 107-(i*2))
   
    card = card_str[1:] if len(card_str) > 1 else card_str
    if card == "0":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
    elif card == "8":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(72+i, 20, 72+i, 85)
    elif card == "1":
        for i in range(15):
            brain.screen.draw_line(20, 47+i, 139, 47+i)
    elif card == "3":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
    elif card == "2":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "5":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "6":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "9":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "4" and "D" not in card_str:
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
    elif card == "7":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
    elif card == "Rv":
        for i in range(15):
            brain.screen.draw_line(62+i, 30, 62+i, 87)
            brain.screen.draw_line(69, 20, 52+i, 40)
            brain.screen.draw_line(69, 20, 82-i, 40)
            brain.screen.draw_line(82+i, 20, 82+i, 77)
            brain.screen.draw_line(89, 87, 74+i, 67)
            brain.screen.draw_line(89, 87, 104-i, 67)
    elif card == "S":
        for i in range(15):
            brain.screen.draw_rectangle(40+i, 20+i, 82-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(52+i, 20, 92+i, 80)
    elif card == "D2":
        brain.screen.set_fill_color(Color.WHITE)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+(i/2), 30)
        if color_code == 'R': brain.screen.set_fill_color(Color.RED)
        elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
        elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
        elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(47, 32, 40, 25)
        brain.screen.draw_rectangle(73, 52, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10+i, 66, 10+i, 79)
            brain.screen.draw_line(10, 66+i, 20, 66+i)
            brain.screen.draw_line(18+i, 66, 18+i, 79)
            brain.screen.draw_line(20, 75+i, 30, 75+i)
            brain.screen.draw_line(26+i, 66, 26+i, 79)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10-i, 107-66, 159-10-i, 107-79)
            brain.screen.draw_line(159-10, 107-66-i, 159-20, 107-66-i)
            brain.screen.draw_line(159-18-i, 107-66, 159-18-i, 107-79)
            brain.screen.draw_line(159-20, 107-75-i, 159-30, 107-75-i)
            brain.screen.draw_line(159-26-i, 107-66, 159-26-i, 107-79)
    elif card_str == "W":
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(50, 20, 30, 32)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(50, 52, 30, 32)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(80, 20, 30, 32)
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(80, 52, 30, 32)
        brain.screen.set_fill_color(Color.TRANSPARENT)
        brain.screen.set_pen_width(3)
        for i in range(15):
            brain.screen.draw_circle(80, 52, 30-(i/5))
        brain.screen.set_pen_color(Color.BLACK)
        for i in range(65):
            brain.screen.draw_circle(80, 52, 31+(i/5))
        brain.screen.set_pen_width(1)
    elif card_str == "D4":
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(78, 42, 40, 25)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(60, 28, 40, 25)
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(42, 42, 40, 25)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(60, 56, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10, 75+i, 20, 75+i)
            brain.screen.draw_line(16+i, 75, 16+i, 66)
            brain.screen.draw_line(10, 66+i, 30, 66+i)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10, 107-75-i, 159-20, 107-75-i)
            brain.screen.draw_line(159-16-i, 107-75, 159-16-i, 107-66)
            brain.screen.draw_line(159-10, 107-66-i, 159-30, 107-66-i)
    else:
        # Card Back Graphic
        brain.screen.set_fill_color(Color.RED)
        brain.screen.set_pen_color(Color.RED)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+(i/2), 30)
        brain.screen.set_pen_color(Color.YELLOW)
        for i in range(5):
            brain.screen.draw_line(75, 50+i-5, 85, 50+i-5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i+5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i-5)

            brain.screen.draw_line(75, 50+i-15, 85, 50+i-15)
            brain.screen.draw_line(75+(i/2), 50-15, 75+(i/2), 50-25)
            brain.screen.draw_line(83+(i/2), 50-15, 83+(i/2), 50-25)
            brain.screen.draw_line(75, 50+i-25, 85, 50+i-25)

            brain.screen.draw_line(75, 50+i+15, 85, 50+i+15)
            brain.screen.draw_line(83+(i/2), 50+15, 83+(i/2), 50+25)
            brain.screen.draw_line(75, 50+i+25, 85, 50+i+25)
    brain.screen.set_fill_color(Color.TRANSPARENT)

# --- Argument Mapping Helper ---

def get_card_render_args(card_str):
    """Converts a card string like 'Red 5' into (card_str, color_code)."""
    if "Wild +4" in card_str or card_str == "D4":
        return ("D4", "K")
    elif "Wild" in card_str or card_str == "W":
        return ("W", "K")
    
    parts = card_str.split(" ")
    if len(parts) < 2:
        return ("BACK", "K")
        
    color_map = {'Red': 'R', 'Green': 'G', 'Blue': 'B', 'Yellow': 'Y'}
    c_code = color_map.get(parts[0], 'K')
    
    val = parts[1]
    val_map = {'Skip': 'S', 'Reverse': 'Rv', '+2': 'D2'}
    val_code = val_map.get(val, val)
    
    return (c_code + val_code, c_code)

# --- Driving & Privacy Routines ---

FORWARD_DIST_UNITS = 2
TURN_ANGLE_DEGREES = 90

def robot_drive_forward(units=FORWARD_DIST_UNITS):
    wait(1, SECONDS)
    FWD.broadcast_and_wait()
    FWD.broadcast_and_wait()

def robot_turn_left(angle=TURN_ANGLE_DEGREES):
    wait(1, SECONDS)
    LT.broadcast_and_wait()
    
def robot_turn_right(angle=TURN_ANGLE_DEGREES):
    wait(1, SECONDS)
    RT.broadcast_and_wait()

def show_privacy_screen(text_msg):
    """Hides player hand during drive movement."""
    brain.screen.clear_screen()
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.set_cursor(2, 1)
    brain.screen.print("================")
    brain.screen.set_cursor(3, 1)
    brain.screen.print(text_msg[:16])
    brain.screen.set_cursor(4, 1)
    brain.screen.print("================")

def move_to_center_and_discard(played_card):
    # Hide hand while driving out
    show_privacy_screen("DRIVING CENTER...")
    robot_drive_forward(FORWARD_DIST_UNITS)
    
    # Display played card full screen at center
    c_str, c_code = get_card_render_args(played_card)
    draw_card_full_screen(c_str, c_code)
    wait(2, SECONDS)
    
    # Hide screen while returning to player
    show_privacy_screen("RETURNING...")
    robot_turn_right(90)
    robot_turn_right(90)
    robot_drive_forward(FORWARD_DIST_UNITS)
    robot_turn_right(90)
    robot_turn_right(90)

def move_to_center_and_draw(count=1):
    # Hide hand while driving out
    show_privacy_screen("DRIVING CENTER...")
    robot_drive_forward(FORWARD_DIST_UNITS)
    
    # Flash card back graphic once for each drawn card
    for i in range(count):
        draw_card_full_screen("BACK", "K")
        wait(800, MSEC)
        brain.screen.clear_screen()
        wait(300, MSEC)
        
    # Hide screen while returning
    show_privacy_screen("RETURNING...")
    robot_turn_left(90)
    robot_turn_left(90)
    robot_drive_forward(FORWARD_DIST_UNITS)
    robot_turn_left(90)
    robot_turn_left(90)

# --- Game Deck Setup ---

COLORS = ['Red', 'Yellow', 'Green', 'Blue']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2', '+4']

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

# --- UI & Hand Display ---

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

# --- Main Physical Game Loop ---

def play_physical_game():
    robot_deck = create_deck()
    shuffle_list(robot_deck)
    
    bot_hand = [draw_card(robot_deck) for _ in range(7)]
    display_full_hand(bot_hand, "START HAND")
    
    turn = 1
    while len(bot_hand) > 0:
        top_card = input_top_card_via_buttons()
        
        # Draw penalties (+2 or +4)
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
            
            # Drive out to center and display full-screen card graphic
            move_to_center_and_discard(played_card)
        else:
            # Drive out to center and draw card
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

    # Winner Display
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("ROBOT WINS!")
    brain.screen.set_cursor(4, 1)
    brain.screen.print("HAND EMPTY")

# Run program
play_physical_game()