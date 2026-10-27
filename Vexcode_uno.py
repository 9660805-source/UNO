# ---------------------------------------------------------------------------- #
# 	Project:       VEX EXP UNO Autonomous Host (Absolute Heading Engine)      #
# 	Module:        main.py                                                     #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# Hardware Motors (Port 1 Left, Port 5 Right)
motor_l = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_r = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

# --- Low-Level Motion Constants ---
DEG_PER_FORWARD_UNIT = 425
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
# 0: Station 0 (Forward), 1: Station 1 (Right), 2: Station 2 (Behind), 3: Station 3 (Left)
CURRENT_HEADING = 0 

def navigate_to_station(target_station):
    global CURRENT_HEADING
    
    # Calculate shortest rotation from current heading to target station
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
    # Reverse back along the exact vector entered, keeping orientation locked
    drive_reverse(2)

# --- Display & UI Helpers ---
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

# --- Fully Autonomous Match Runner ---

def run_match():
    global CURRENT_HEADING
    
    # Reset seed based on boot timer
    urandom.seed(int(brain.timer.time(MSEC)))

    # Reset Hardware Heading Tracking
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
    direction = 1  # 1: Clockwise, -1: Counter-Clockwise
    
    show_message("AUTONOMOUS HOST", "PRESS [V] START")
    wait_for_button_release()
    while not brain.buttonCheck.pressing(): wait(20, MSEC)
    wait_for_button_release()
    
    while True:
        current_player = players[current_p_idx]
        top_card = discard_pile[-1]
        
        # 1. Navigate to target player station
        show_message("TARGET: " + current_player, "DRIVING...")
        navigate_to_station(current_p_idx)
        
        # 2. Evaluate turn logic at station
        bot_hand = hands[current_player]
        playable = [i for i, c in enumerate(bot_hand) if is_card_legal(c, top_card)]
        card_played = False
        
        if len(playable) > 0:
            chosen_i = playable[0]
            played = bot_hand.pop(chosen_i)
            
            if "Wild" in played:
                best_color = get_best_color(bot_hand)
                played = best_color + " +4" if played == "Wild +4" else best_color + " Wild"
                
            discard_pile.append(played)
            show_message(current_player + " PLAYED:", shorten(played))
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
                    show_message(current_player + " PLAYED:", shorten(played))
                    card_played = True
                    wait(1.5, SECONDS)

        # 3. UNO Call Check
        if len(bot_hand) == 1:
            brain.play_sound(SoundType.SIREN)
            show_message("*** UNO! ***", current_player + " HAS 1 CARD")
            wait(1.5, SECONDS)

        # 4. Winner Check
        if len(bot_hand) == 0:
            show_message("MATCH OVER!", current_player + " WINS!")
            wait(3, SECONDS)
            return_to_center_station()
            break

        # 5. Return to central hub position
        show_message("RETURNING...", "TO CENTER HUB")
        return_to_center_station()

        # 6. Apply Official Action Rules & Target Next Player Index
        if card_played:
            latest_card = discard_pile[-1]
            
            if "Skip" in latest_card:
                show_message("ACTION: SKIP", "SKIPPING NEXT")
                wait(1, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue
            elif "Reverse" in latest_card:
                show_message("ACTION: REVERSE", "SWAPPING DIR")
                wait(1, SECONDS)
                direction *= -1
            elif "+2" in latest_card:
                victim_idx = (current_p_idx + direction) % len(players)
                victim = players[victim_idx]
                for _ in range(2):
                    d = draw_card(deck, discard_pile)
                    if d: hands[victim].append(d)
                show_message(victim + " +2", "TURN SKIPPED")
                wait(1.5, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue
            elif "+4" in latest_card:
                victim_idx = (current_p_idx + direction) % len(players)
                victim = players[victim_idx]
                for _ in range(4):
                    d = draw_card(deck, discard_pile)
                    if d: hands[victim].append(d)
                show_message(victim + " +4", "TURN SKIPPED")
                wait(1.5, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue

        current_p_idx = (current_p_idx + direction) % len(players)

def main():
    while True:
        run_match()

main()