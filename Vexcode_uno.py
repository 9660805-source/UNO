# ---------------------------------------------------------------------------- #
# 	Project:       VEX EXP UNO Autonomous Host (Player Card Render Fix)        #
# 	Module:        main.py                                                     #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# Hardware Motors (Port 1 Left, Port 5 Right)
motor_l = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_r = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

# --- Motion Constants ---
DEG_PER_FORWARD_UNIT = 150 
DEG_PER_90_TURN = 220

def drive_forward(units=2):
    deg = units * DEG_PER_FORWARD_UNIT
    motor_l.spin_for(FORWARD, deg, DEGREES, wait=False)
    motor_r.spin_for(FORWARD, deg, DEGREES, wait=True)
    wait(100, MSEC)

def drive_reverse(units=2):
    deg = units * DEG_PER_FORWARD_UNIT
    motor_l.spin_for(REVERSE, deg, DEGREES, wait=False)
    motor_r.spin_for(REVERSE, deg, DEGREES, wait=True)
    wait(100, MSEC)

def turn_right_90(steps=1):
    for _ in range(steps):
        motor_l.spin_for(FORWARD, DEG_PER_90_TURN, DEGREES, wait=False)
        motor_r.spin_for(REVERSE, DEG_PER_90_TURN, DEGREES, wait=True)
        wait(100, MSEC)

def turn_left_90(steps=1):
    for _ in range(steps):
        motor_l.spin_for(REVERSE, DEG_PER_90_TURN, DEGREES, wait=False)
        motor_r.spin_for(FORWARD, DEG_PER_90_TURN, DEGREES, wait=True)
        wait(100, MSEC)

# --- Absolute Heading Navigation ---
CURRENT_HEADING = 0 

def navigate_to_station(target_station):
    global CURRENT_HEADING
    turn_diff = (target_station - CURRENT_HEADING) % 4
    if turn_diff == 1:
        turn_right_90(1)
    elif turn_diff == 2:
        turn_right_90(2)
    elif turn_diff == 3:
        turn_left_90(1)
    CURRENT_HEADING = target_station
    drive_forward(2)

def return_to_center_station():
    drive_reverse(2)

# --- Graphical Display Converter & Renderer ---
def format_card_for_graphics(card_str):
    color_code = 'K'
    if "Red" in card_str: color_code = 'R'
    elif "Green" in card_str: color_code = 'G'
    elif "Blue" in card_str: color_code = 'B'
    elif "Yellow" in card_str: color_code = 'Y'

    if "Wild +4" in card_str or "+4" in card_str:
        return "D4", color_code
    elif "Wild" in card_str:
        return "W", color_code
    elif "Skip" in card_str:
        return "XS", color_code
    elif "Reverse" in card_str:
        return "XRv", color_code
    elif "+2" in card_str:
        return "XD2", color_code

    parts = card_str.split(" ")
    val = parts[1] if len(parts) > 1 else card_str
    return "X" + val, color_code

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
    elif card == "Rv" or card == "Reverse":
        for i in range(15):
            brain.screen.draw_line(62+i, 30, 62+i, 87)
            brain.screen.draw_line(69, 20, 52+i, 40)
            brain.screen.draw_line(69, 20, 82-i, 40)
            brain.screen.draw_line(82+i, 20, 82+i, 77)
            brain.screen.draw_line(89, 87, 74+i, 67)
            brain.screen.draw_line(89, 87, 104-i, 67)
    elif card == "S" or card == "Skip":
        for i in range(15):
            brain.screen.draw_rectangle(40+i, 20+i, 82-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(52+i, 20, 92+i, 80)
    elif card == "D2" or card == "+2":
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
    elif card_str == "W" or "Wild" in card_str and "+4" not in card_str:
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
    elif card_str == "D4" or "+4" in card_str:
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

def render_card(card_str):
    c_str, color = format_card_for_graphics(card_str)
    draw_card_full_screen(c_str, color)

# --- UI Helpers ---
def wait_for_button_release():
    while brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing():
        wait(20, MSEC)

def shorten(text):
    res = text.replace("Yellow", "Yel").replace("Green", "Grn")
    return res.replace("Blue", "Blu").replace("Reverse", "Rev")

def show_message(line1, line2=""):
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print(line1[:16])
    if line2:
        brain.screen.set_cursor(4, 1)
        brain.screen.print(line2[:16])

def display_full_hand(hand, title="HAND"):
    page = 0
    total_pages = (len(hand) + 5) // 6 if len(hand) > 0 else 1
    
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("%s (%d) P%d/%d" % (title[:8], len(hand), page + 1, total_pages))
    
    start_idx = page * 6
    for r in range(3):
        brain.screen.set_cursor(r + 2, 1)
        c1 = start_idx + (r * 2)
        c2 = c1 + 1
        s1 = "%d:%s" % (c1 + 1, shorten(hand[c1])) if c1 < len(hand) else ""
        s2 = "%d:%s" % (c2 + 1, shorten(hand[c2])) if c2 < len(hand) else ""
        brain.screen.print("%-8s %-7s" % (s1[:8], s2[:7]))
        
    wait(1.5, SECONDS)

# --- Card Engine & Logic ---
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

def shuffle_list(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = urandom.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

def draw_card(deck, discard_pile):
    if len(deck) == 0:
        if len(discard_pile) > 1:
            top = discard_pile.pop()
            deck.extend(discard_pile)
            discard_pile.clear()
            discard_pile.append(top)
            shuffle_list(deck)
        else:
            return None
    return deck.pop(0)

def is_card_legal(card, top_card):
    if "Wild" in card: return True
    c_parts = card.split(" ")
    t_parts = top_card.split(" ")
    if c_parts[0] == t_parts[0]: return True
    if len(c_parts) > 1 and len(t_parts) > 1 and c_parts[1] == t_parts[1]: return True
    return False

def get_best_color(hand):
    counts = {c: 0 for c in COLORS}
    for card in hand:
        for c in COLORS:
            if c in card:
                counts[c] += 1
    best = COLORS[0]
    for c in COLORS:
        if counts[c] > counts[best]:
            best = c
    return best

# --- Match Execution Loop ---

def run_match():
    global CURRENT_HEADING
    
    urandom.seed(int(brain.timer.time(MSEC)))
    CURRENT_HEADING = 0

    deck = create_deck()
    shuffle_list(deck)
    shuffle_list(deck)
    
    discard_pile = []
    top_card = draw_card(deck, discard_pile)
    while "Wild" in top_card:
        deck.append(top_card)
        shuffle_list(deck)
        top_card = draw_card(deck, discard_pile)
    discard_pile.append(top_card)
    
    players = ["BOT 1", "BOT 2", "BOT 3", "BOT 4"]
    hands = {p: [draw_card(deck, discard_pile) for _ in range(7)] for p in players}
    
    current_p_idx = 0
    direction = 1
    
    show_message("AUTONOMOUS HOST", "PRESS [V] START")
    wait_for_button_release()
    while not brain.buttonCheck.pressing(): wait(20, MSEC)
    wait_for_button_release()
    
    while True:
        current_player = players[current_p_idx]
        top_card = discard_pile[-1]
        
        # 1. Drive to station
        show_message("TARGET: " + current_player, "DRIVING...")
        navigate_to_station(current_p_idx)
        
        # 2. Display active player hand
        bot_hand = hands[current_player]
        display_full_hand(bot_hand, current_player)
        
        # 3. Evaluate and execute turn
        playable = [i for i, c in enumerate(bot_hand) if is_card_legal(c, top_card)]
        card_played = False
        
        if len(playable) > 0:
            chosen_i = playable[0]
            played = bot_hand.pop(chosen_i)
            
            if "Wild" in played:
                best_color = get_best_color(bot_hand)
                played = best_color + " +4" if played == "Wild +4" else best_color + " Wild"
                
            discard_pile.append(played)
            render_card(played)
            card_played = True
            wait(1.5, SECONDS)
        else:
            show_message(current_player, "DRAWS A CARD")
            wait(1.2, SECONDS)
            drawn = draw_card(deck, discard_pile)
            if drawn:
                bot_hand.append(drawn)
                if is_card_legal(drawn, top_card):
                    played = bot_hand.pop()
                    if "Wild" in played:
                        best_color = get_best_color(bot_hand)
                        played = best_color + " +4" if played == "Wild +4" else best_color + " Wild"
                    discard_pile.append(played)
                    render_card(played)
                    card_played = True
                    wait(1.5, SECONDS)

        # 4. UNO Call Check
        if len(bot_hand) == 1:
            brain.play_sound(SoundType.SIREN)
            show_message("*** UNO! ***", current_player + " HAS 1 CARD")
            wait(1.5, SECONDS)

        # 5. Winner Check
        if len(bot_hand) == 0:
            show_message("MATCH OVER!", current_player + " WINS!")
            wait(3, SECONDS)
            return_to_center_station()
            break

        # 6. Return to Center
        show_message("RETURNING...", "TO CENTER HUB")
        return_to_center_station()

        # 7. Action Card Penalty Processing & Turn Shift
        if card_played:
            latest_card = discard_pile[-1]
            
            if "Skip" in latest_card:
                render_card(latest_card)
                wait(1, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue
            elif "Reverse" in latest_card:
                render_card(latest_card)
                wait(1, SECONDS)
                direction *= -1
            elif "+2" in latest_card:
                victim_idx = (current_p_idx + direction) % len(players)
                victim = players[victim_idx]
                for _ in range(2):
                    d = draw_card(deck, discard_pile)
                    if d: hands[victim].append(d)
                render_card(latest_card)
                wait(1.5, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue
            elif "+4" in latest_card:
                victim_idx = (current_p_idx + direction) % len(players)
                victim = players[victim_idx]
                for _ in range(4):
                    d = draw_card(deck, discard_pile)
                    if d: hands[victim].append(d)
                render_card(latest_card)
                wait(1.5, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue

        current_p_idx = (current_p_idx + direction) % len(players)

def main():
    while True:
        run_match()

main()