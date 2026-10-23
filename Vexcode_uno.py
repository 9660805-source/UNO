# ---------------------------------------------------------------------------- #
# 	Project:       VEX EXP UNO Solo Mode (Official Draw/Skip Rules)           #
# 	Module:        main.py                                                     #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# Seed random number generator with boot millisecond time for fresh shuffles
urandom.seed(int(brain.timer.time(MSEC)))

def wait_for_button_release():
    while brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing():
        wait(20, MSEC)

# --- Deck & Card Logic ---
COLORS = ['Red', 'Yellow', 'Green', 'Blue']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2', '+4']

def shorten(text):
    res = text.replace("Yellow", "Yel").replace("Green", "Grn")
    return res.replace("Blue", "Blu").replace("Reverse", "Rev")

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

# --- User Interface ---

def select_option(options, title):
    selected_idx = 0
    wait_for_button_release()
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print(title[:16])
        brain.screen.set_cursor(3, 1)
        brain.screen.print("< " + options[selected_idx] + " >")
        brain.screen.set_cursor(5, 1)
        brain.screen.print("L/R:Nav  [V]:OK")
        
        wait(100, MSEC)
        if brain.buttonLeft.pressing():
            selected_idx = (selected_idx - 1) % len(options)
            wait_for_button_release()
        elif brain.buttonRight.pressing():
            selected_idx = (selected_idx + 1) % len(options)
            wait_for_button_release()
        elif brain.buttonCheck.pressing():
            wait_for_button_release()
            return options[selected_idx]

def show_message(line1, line2=""):
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print(line1[:16])
    if line2:
        brain.screen.set_cursor(4, 1)
        brain.screen.print(line2[:16])

def choose_card_to_play(hand, playable_indices, top_card):
    selected_idx = playable_indices[0] if len(playable_indices) > 0 else 0
    wait_for_button_release()
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP: " + shorten(top_card))
        
        card_name = hand[selected_idx]
        is_legal = selected_idx in playable_indices
        status = "[OK]" if is_legal else "[X]"
        
        brain.screen.set_cursor(3, 1)
        brain.screen.print("< %s > %s" % (shorten(card_name), status))
        
        brain.screen.set_cursor(5, 1)
        if is_legal: brain.screen.print("L/R:Nav  [V]:PLAY")
        else: brain.screen.print("L/R:Nav (ILLEGAL)")
        
        wait(100, MSEC)
        if brain.buttonLeft.pressing():
            selected_idx = (selected_idx - 1) % len(hand)
            wait_for_button_release()
        elif brain.buttonRight.pressing():
            selected_idx = (selected_idx + 1) % len(hand)
            wait_for_button_release()
        elif brain.buttonCheck.pressing():
            if is_legal:
                wait_for_button_release()
                return selected_idx

# --- Main Game Loop ---

def play_solo_game():
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
    
    hands = {
        "YOU": [draw_card(deck, discard_pile) for _ in range(7)],
        "BOT1": [draw_card(deck, discard_pile) for _ in range(7)],
        "BOT2": [draw_card(deck, discard_pile) for _ in range(7)]
    }
    
    players = ["YOU", "BOT1", "BOT2"]
    current_p_idx = 0
    direction = 1  # 1 = forward, -1 = reverse
    
    show_message("SOLO UNO HOST", "PRESS [V] START")
    wait_for_button_release()
    while not brain.buttonCheck.pressing(): wait(20, MSEC)
    wait_for_button_release()
    
    while True:
        current_player = players[current_p_idx]
        top_card = discard_pile[-1]
        
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP: " + shorten(top_card))
        brain.screen.set_cursor(2, 1)
        brain.screen.print("TURN: " + current_player)
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Y:%d  B1:%d  B2:%d" % (len(hands["YOU"]), len(hands["BOT1"]), len(hands["BOT2"])))
        brain.screen.set_cursor(5, 1)
        brain.screen.print("PRESS [V] NEXT")
        
        wait_for_button_release()
        while not brain.buttonCheck.pressing(): wait(20, MSEC)
        wait_for_button_release()
        
        card_played = False
        
        # Human Player Turn
        if current_player == "YOU":
            playable = [i for i, c in enumerate(hands["YOU"]) if is_card_legal(c, top_card)]
            
            if len(playable) > 0:
                chosen_i = choose_card_to_play(hands["YOU"], playable, top_card)
                played = hands["YOU"].pop(chosen_i)
                
                if "Wild" in played:
                    chosen_color = select_option(COLORS, "CHOOSE COLOR")
                    played = chosen_color + " +4" if played == "Wild +4" else chosen_color + " Wild"
                
                discard_pile.append(played)
                show_message("YOU PLAYED:", played)
                card_played = True
                wait(1.2, SECONDS)
            else:
                show_message("NO MATCH!", "DRAWING CARD...")
                wait(1, SECONDS)
                drawn = draw_card(deck, discard_pile)
                if drawn:
                    hands["YOU"].append(drawn)
                    if is_card_legal(drawn, top_card):
                        playable = [len(hands["YOU"]) - 1]
                        chosen_i = choose_card_to_play(hands["YOU"], playable, top_card)
                        played = hands["YOU"].pop(chosen_i)
                        
                        if "Wild" in played:
                            chosen_color = select_option(COLORS, "CHOOSE COLOR")
                            played = chosen_color + " +4" if played == "Wild +4" else chosen_color + " Wild"
                                
                        discard_pile.append(played)
                        show_message("YOU PLAYED:", played)
                        card_played = True
                        wait(1.2, SECONDS)

        # Bot Player Turn
        else:
            bot_hand = hands[current_player]
            bot_playable = [i for i, c in enumerate(bot_hand) if is_card_legal(c, top_card)]
            
            if len(bot_playable) > 0:
                chosen_i = bot_playable[0]
                played = bot_hand.pop(chosen_i)
                
                if "Wild" in played:
                    best_color = COLORS[urandom.randint(0, 3)]
                    played = best_color + " +4" if played == "Wild +4" else best_color + " Wild"
                        
                discard_pile.append(played)
                show_message(current_player + " PLAYED:", played)
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
                            best_color = COLORS[urandom.randint(0, 3)]
                            played = best_color + " +4" if played == "Wild +4" else best_color + " Wild"
                        discard_pile.append(played)
                        show_message(current_player + " PLAYED:", played)
                        card_played = True
                        wait(1.5, SECONDS)

        # Win Condition Check
        if len(hands[current_player]) == 0:
            show_message("GAME OVER!", current_player + " WINS!")
            break
            
        # UNO Check
        if len(hands[current_player]) == 1:
            brain.play_sound(SoundType.SIREN)
            show_message("*** UNO! ***", current_player + " HAS 1 CARD")
            wait(1.5, SECONDS)

        # Official Action Card Rule Processing
        if card_played:
            latest_card = discard_pile[-1]
            
            if "Skip" in latest_card:
                # Skip next player entirely
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                show_message("SKIP APPLIED!")
                wait(1, SECONDS)
                continue
            elif "Reverse" in latest_card:
                direction *= -1
                show_message("REVERSED!")
                wait(1, SECONDS)
            elif "+2" in latest_card:
                # Next player draws 2 AND loses their turn (skipped)
                next_p_idx = (current_p_idx + direction) % len(players)
                next_p = players[next_p_idx]
                for _ in range(2):
                    d = draw_card(deck, discard_pile)
                    if d: hands[next_p].append(d)
                show_message(next_p + " DRAWS 2!", "TURN SKIPPED!")
                wait(1.5, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue
            elif "+4" in latest_card:
                # Next player draws 4 AND loses their turn (skipped)
                next_p_idx = (current_p_idx + direction) % len(players)
                next_p = players[next_p_idx]
                for _ in range(4):
                    d = draw_card(deck, discard_pile)
                    if d: hands[next_p].append(d)
                show_message(next_p + " DRAWS 4!", "TURN SKIPPED!")
                wait(1.5, SECONDS)
                current_p_idx = (current_p_idx + (2 * direction)) % len(players)
                continue

        # Standard turn advance
        current_p_idx = (current_p_idx + direction) % len(players)

play_solo_game()