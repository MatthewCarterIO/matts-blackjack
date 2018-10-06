"""
    File name: mattsblackjack.py
    Author: Matthew Carter
    Date created: 17/04/2018
    Date last modified: 06/10/2018
    Python Version: 3.6.6
"""

import random
import time


# Global variables.
balance = 0.0
round_number = 1


# Print rules.
def show_rules():
    choices = {'Y', 'N'}
    while True:
        choice = input("\nWould you like to read the rules before starting? [Y/N]: ")
        choice = choice.upper()
        if choice in choices:
            if choice == 'Y':
                try:
                    # Read in text from file.
                    with open('mattsblackjackrules.txt', 'r', encoding="utf-8") as f:
                        rules_text = f.readlines()
                except FileNotFoundError:
                    print("The rules are missing. It is now a world without rules!")
                else:
                    # Remove whitespace character at the end of each line and print each.
                    print()
                    for line in rules_text:
                        print(line.strip('\n'))
                    break
            else:
                break
        else:
            print("Invalid choice.")


# Print round number.
def show_round():
    global round_number
    print("\nRound {}:".format(round_number))


# Player's starting cash total.
def starting_balance(start_balance):
    global balance
    balance = start_balance


# Current balance.
def current_balance():
    global balance
    return balance


# Update the balance following win or loss.
def update_balance(operation, bet):
    global balance
    if operation == "bet":
        balance -= bet
    elif operation == "normal_win":
        balance += bet
    elif operation == "blackjack_win":
        balance = balance + (1.5 * bet)
    elif operation == "normal_loss":
        balance -= bet


# Print balance.
def show_balance():
    global balance
    print("\nBalance = £{0:.2f}".format(round(balance, 2)))


# Initial bet.
def initial_bet():
    global balance
    while True:
        try:
            # Accept only integers.
            bet = input("\nPlace your bet: £")
            bet = int(bet)
        except ValueError:
            print("Not a valid bet!")
        else:
            if bet < 10:
                # Insufficient bet.
                print("Minimum bet is £10.")
            elif bet > current_balance():
                # Insufficient balance to make bet.
                print("You only have £{0:.2f} available to bet.".format(round(balance, 2)))
            else:
                # Valid bet, exit loop.
                break
    return bet


# Offer chance to double down bet.
def double_down_bet(original_bet):
    doubled_down = False
    doubled_bet = original_bet * 2
    # Offer player the opportunity to double down if their balance allows it.
    if current_balance() >= doubled_bet:
        choices = {'Y', 'N'}
        while True:
            choice = input("\nDo you want to double down? (Y/N): ")
            choice = choice.upper()
            if choice in choices:
                if choice == 'Y':
                    # Chosen to double down.
                    doubled_down = True
                    print("Doubling down. Bet is now £{0:.2f}.".format(round(doubled_bet, 2)))
                    return doubled_bet, doubled_down
                else:
                    # Not doubling down.
                    print("Not doubling down. Bet remains at £{0:.2f}.".format(round(original_bet, 2)))
                    return original_bet, doubled_down
            else:
                print("Invalid choice.")
    else:
        print("\nInsufficient balance to double down. Bet remains at £{0:.2f}.".format(round(original_bet, 2)))
        return original_bet, doubled_down


# Create a new deck.
def new_deck():
    #  Create a list of cards where each card is stored as a tuple.
    deck = []
    suits = ("Clubs", "Diamonds", "Hearts", "Spades")
    numbers = tuple(range(1, 14))
    for suit in suits:
        for number in numbers:
            card = (number, suit)
            deck.append(card)
    return deck


# Create a new multi-deck. Blackjack usually played with between 6-8 decks in casinos.
def new_multi_deck(no_of_decks):
    multi_deck = []
    for _ in range(no_of_decks):
        multi_deck.extend(new_deck())
    return multi_deck


# Shuffle the deck.
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


# Deal a single card.
def deal_card(deck):
    return deck.pop()


# Deal the first two cards of the round to the player and dealer.
def initial_deal(deck, player_hand, dealer_hand):
    for _ in range(2):
        player_hand.append(deal_card(deck))
        dealer_hand.append(deal_card(deck))
    return player_hand, dealer_hand


# Check if initial hand contains any aces.
def initial_hand_has_aces(hand):
    # Hand containing cards is a list containing two tuples.
    # Check for ace in opening hand.
    if hand[0][0] == 1 or hand[1][0] == 1:
        return True


# Check if the two cards in the initial hand are the same.
def initial_hand_has_same(hand):
    if hand[0][0] == hand[1][0]:
        return True


# Offer chance to split hand if cards are of the same value.
def split_hand(hand, bet, deck):
    global balance
    splitting = False
    hand_one = []
    hand_two = []
    split_hands = []
    choices = {'Y', 'N'}
    if balance >= bet * 2:
        while True:
            choice = input("\nSame value cards in opening hand. Would you like to split? (Y/N): ")
            choice = choice.upper()
            if choice in choices:
                if choice == 'Y':
                    # Player splits.
                    print("Splitting hand...\n")
                    time.sleep(1.5)
                    splitting = True
                    # Add cards from original hand to two separate hands, deal another card to each split hand, then
                    # clear original hand.
                    hand_one.append(hand[0])
                    hand_one.append(deal_card(deck))
                    show_split_hand("first", hand_one)
                    hand_two.append(hand[1])
                    hand_two.append(deal_card(deck))
                    show_split_hand("second", hand_two)
                    split_hands = [hand_one, hand_two]
                    clear_hand(hand)
                    return hand, split_hands, splitting
                else:
                    # Doesn't split.
                    print("Not splitting.")
                    return hand, split_hands, splitting
            else:
                print("Invalid choice.")
    else:
        print("\nInsufficient balance to split your hand.")
        return hand, split_hands, splitting


# Deal card(s) to player if they choose to hit.
def deal_out_player(hand, deck):
    player_done = False
    choices = {'H', 'S'}
    while not player_done:
        choice = input("\nHit or Stand? (H/S): ")
        choice = choice.upper()
        if choice in choices:
            if choice == 'H':
                # Player hits.
                print("\nPlayer receives a card...")
                time.sleep(1.5)
                extra_card = deal_card(deck)
                hand.append(extra_card)
                show_hand("Player", hand)
                show_hand_total("Player", hand)
                # If player now has 21 or goes bust after receiving card, stop asking for H/S input.
                if hand_total_twenty_one(hand) or hand_total_bust(hand):
                    player_done = True
                    if hand_total_bust(hand):
                        print("Player bust.")
            else:
                # Player stands.
                player_done = True
                print()
        else:
            print("Invalid choice.")


# Deal card to player following double down bet.
def deal_out_player_doubled(hand, deck):
    print("\nPlayer receives one additional card...")
    time.sleep(1.5)
    extra_card = deal_card(deck)
    hand.append(extra_card)
    show_hand("Player", hand)
    show_hand_total("Player", hand)
    if hand_total_bust(hand):
        print("Player bust.")


# Deal card(s) to dealer if necessary.
def deal_out_dealer(hand, deck):
    dealer_done = False
    while not dealer_done:
        show_hand("Dealer", hand)
        show_hand_total("Dealer", hand)
        if hand_total(hand) < 17:
            # Dealer not at minimum of 17 so must draw card.
            print("\nDealer draws a card...")
            time.sleep(1.5)
            extra_card = deal_card(deck)
            hand.append(extra_card)
        elif hand_total(hand) > 21:
            # Dealer bust.
            print("Dealer bust.")
            dealer_done = True
        else:
            # Includes totals 17-21.
            dealer_done = True


# Print single card.
def show_card(card):
    if card[0] == 1:
        print("\tAce of {}".format(card[1]))
    elif card[0] == 11:
        print("\tJack of {}".format(card[1]))
    elif card[0] == 12:
        print("\tQueen of {}".format(card[1]))
    elif card[0] == 13:
        print("\tKing of {}".format(card[1]))
    else:
        print("\t{} of {}".format(card[0], card[1]))


# Print hand.
def show_hand(string, hand):
    print("{}'s hand:".format(string))
    for card in hand:
        show_card(card)


# Print dealer's initial hand.
def show_initial_dealer_hand(hand):
    print("Dealer's opening hand:")
    show_card(hand[0])
    # On opening dealer has one card face down.
    print("\tSecond card face down.")


# Print player's split hand.
def show_split_hand(hand_string, hand):
    print("Player's {} split hand:".format(hand_string))
    for card in hand:
        show_card(card)


# Print total of hand.
def show_hand_total(string, hand):
    if hand_total_blackjack(hand):
        print("{} blackjack.".format(string))
    else:
        print("{} currently has {}".format(string, hand_total(hand)))


# Calculate total of hand.
def hand_total(hand):
    total = 0
    # Keep track of aces available to be converted if required.
    aces_for_conversion = aces_in_hand_counter(hand)
    for card in hand:
        if card[0] is 1:
            # Aces.
            if total < 21:
                # Ace is 11.
                total += 11
        elif (card[0] == 11) or (card[0] == 12) or (card[0] == 13):
            # Face cards.
            total += 10
        else:
            # Numbered cards.
            total += card[0]
        # Any ace currently in hand has been counted as 11. If the hand total following addition above is now above 21
        # (would be bust) but an ace is in the hand, convert it to being worth 1.
        if total > 21 and aces_for_conversion > 0:
            total -= 10
            aces_for_conversion -= 1
    return total


# Check if hand is blackjack.
def hand_total_blackjack(hand):
    # Return True if 21 with two cards, False if not.
    return hand_total_twenty_one(hand) and (len(hand) == 2)


# Check if hand is 21.
def hand_total_twenty_one(hand):
    # Return True if hand total equals 21, False if not.
    return hand_total(hand) == 21


# Check if hand is bust.
def hand_total_bust(hand):
    # Return True if hand total greater than 21, False if not.
    return hand_total(hand) > 21


# Count aces in hand.
def aces_in_hand_counter(hand):
    ace_counter = 0
    for card in hand:
        if card[0] == 1:
            ace_counter += 1
    return ace_counter


# Clear hand.
def clear_hand(hand):
    hand.clear()


# Main game.
def play_game():
    # Game title.
    print("Blackjack")

    # Give player option of reading the game rules.
    show_rules()

    print("\nLet's play Blackjack!")

    # Create a new multi-deck using 8 decks, the empty player and dealer hands, and balance.
    game_multi_deck = new_multi_deck(8)
    player_hand = []
    dealer_hand = []
    starting_balance(500)

    # Shuffle deck.
    shuffle_deck(game_multi_deck)

    # Show opening balance.
    show_balance()

    # Display round.
    show_round()

    # Start new round flag.
    new_round = True
    # Start of new round.
    while new_round:
        # Place initial bet.
        player_bet = initial_bet()
        # Deal initial cards.
        initial_deal(game_multi_deck, player_hand, dealer_hand)
        # Display player's hand and current total. Display dealer's initial hand.
        show_hand("Player", player_hand)
        show_hand_total("Player", player_hand)
        show_initial_dealer_hand(dealer_hand)

        # Give player opportunity to split if initial hand allows it.
        player_split_hands = []
        split_round = False
        if initial_hand_has_same(player_hand):
            player_hand, player_split_hands, split_round = split_hand(player_hand, player_bet, game_multi_deck)

        if split_round:
            # Proceed with round using the two split hands.
            # Store bets of each split hand.
            player_split_bets = []
            # Keep the running total of bets through both split hands, including initial bets for each hand and any
            # doubling down. Initialised with the required bet for each of the split hands.
            split_bets_running_total = player_bet * 2
            # Keep count of split hands that go bust.
            split_hand_bust_counter = 0
            for player_split_hand in player_split_hands:
                print("\nBetting on", end=" ")
                show_hand("player", player_split_hand)
                show_hand_total("Player", player_split_hand)

                # Give player opportunity to double down if they don't have blackjack already and they have sufficient
                # funds to do so. (Nb. adding another player_bet accounts for the amount required to double down).
                doubled_down_hand = False
                if split_bets_running_total + player_bet <= current_balance() \
                        and not hand_total_blackjack(player_split_hand):
                    player_bet, doubled_down_hand = double_down_bet(player_bet)
                elif hand_total_blackjack(player_split_hand):
                    print("\nCannot double down on this split hand. You have blackjack.")
                else:
                    print("\nInsufficient balance to double down on this split hand.")

                # Add the player's bet (either initial or doubled) to the split bets list.
                player_split_bets.append(player_bet)

                # Update the split bet running total.
                if doubled_down_hand:
                    # Initial bets for each split hand were added to the running total when the variable was
                    # initialised, so only need to add the difference from any doubling up. As a result not necessary
                    # to update the running total if no doubling up occurred.
                    split_bets_running_total += (player_bet / 2)
                    # Reset player_bet variable to the initial non-doubled amount, ready for the next split hand.
                    player_bet = player_bet / 2

                if doubled_down_hand:
                    # Player has doubled down.
                    deal_out_player_doubled(player_split_hand, game_multi_deck)
                    if hand_total_bust(player_split_hand):
                        # Player is bust after taking a card.
                        split_hand_bust_counter += 1
                elif hand_total_blackjack(player_split_hand):
                    # Player has blackjack.
                    continue
                elif hand_total_twenty_one(player_split_hand):
                    # Player has 21.
                    continue
                elif not hand_total_bust(player_split_hand):
                    # Player has less than 21, give option to take card.
                    deal_out_player(player_split_hand, game_multi_deck)
                    if hand_total_bust(player_split_hand):
                        # Player is bust after taking card(s).
                        split_hand_bust_counter += 1
                elif hand_total_bust(player_split_hand):
                    # Player has more than 21. Dealer doesn't need to continue.
                    split_hand_bust_counter += 1

            # Deal out dealer only if at least one of the player's split hands is not bust.
            if split_hand_bust_counter < 2:
                deal_out_dealer(dealer_hand, game_multi_deck)

            # Show result and balance for each split hand in the round.
            for player_split_hand, split_hand_bet in zip(player_split_hands, player_split_bets):
                print("\nSplit hand result:")
                show_hand("Player", player_split_hand)
                round_result(player_split_hand, dealer_hand, split_hand_bet)
                show_balance()
        else:
            # Proceed with round as normal with single hand.
            # Give player opportunity to double down if they don't have blackjack already.
            doubled_down_hand = False
            if not hand_total_blackjack(player_hand):
                player_bet, doubled_down_hand = double_down_bet(player_bet)

            if doubled_down_hand:
                # Player has doubled down.
                deal_out_player_doubled(player_hand, game_multi_deck)
                if not hand_total_bust(player_hand):
                    # Player is not bust after taking card so deal to dealer.
                    deal_out_dealer(dealer_hand, game_multi_deck)
            elif hand_total_blackjack(player_hand):
                # Player has blackjack.
                show_hand("Dealer", dealer_hand)
                show_hand_total("Dealer", dealer_hand)
            elif hand_total_twenty_one(player_hand):
                # Player has 21.
                deal_out_dealer(dealer_hand, game_multi_deck)
            elif not hand_total_bust(player_hand):
                # Player has less than 21, give option to take card.
                deal_out_player(player_hand, game_multi_deck)
                if not hand_total_bust(player_hand):
                    # Player is not bust after taking card so deal to dealer.
                    deal_out_dealer(dealer_hand, game_multi_deck)
            elif hand_total_bust(player_hand):
                # Player has more than 21. Dealer doesn't need to continue.
                show_hand("Dealer", dealer_hand)

            # Show the result and balance at end of the round.
            print("\nRound result:")
            round_result(player_hand, dealer_hand, player_bet)
            show_balance()

        # Check whether the player wishes to play another round if their current balance is sufficient.
        if current_balance() >= 10:
            new_round = play_new_round(game_multi_deck, player_hand, dealer_hand)
        else:
            print("\nInsufficient funds to continue playing! Game over.")
            new_round = False


# Determine result of the round.
def round_result(player_hand, dealer_hand, bet):
    # When the player has blackjack, the player always wins unless the dealer has blackjack too:
    # Player blackjack, dealer blackjack. Push.
    # Player blackjack, dealer under 21. Player wins.
    # Player blackjack, dealer over 21. Player wins. (Not possible for dealer to be bust on two cards though).
    if hand_total_blackjack(player_hand):
        if hand_total_blackjack(dealer_hand):
            print("\nPush - Both player and dealer have blackjack.")
        else:
            print("\nPlayer wins - Player has blackjack but dealer doesn't.")
            update_balance("blackjack_win", bet)
    # Player under 21, dealer blackjack. Dealer wins.
    # Player under 21, dealer under 21. Push if hand totals are the same, otherwise highest hand wins.
    # Player under 21, dealer over 21. Player wins.
    elif not hand_total_bust(player_hand):
        if hand_total_blackjack(dealer_hand):
            print("\nDealer wins - Player under 21 but dealer has blackjack.")
            update_balance("normal_loss", bet)
        elif not hand_total_bust(dealer_hand):
            if hand_total(player_hand) == hand_total(dealer_hand):
                print("\nPush - Both player and dealer are under 21 and have matching totals.")
            elif hand_total(player_hand) > hand_total(dealer_hand):
                print("\nPlayer wins - Both player and dealer under 21 but player has higher total.")
                update_balance("normal_win", bet)
            else:
                print("\nDealer wins - Both player and dealer under 21 but dealer has higher total.")
                update_balance("normal_loss", bet)
        else:
            print("\nPlayer wins - Dealer bust.")
            update_balance("normal_win", bet)
    # In listed cases player is bust so dealer always wins:
    # Player over 21, dealer blackjack. Dealer wins.
    # Player over 21, dealer under 21. Dealer wins.
    # Player over 21, dealer over 21. Doesn't occur because player would be bust before dealer takes any cards.
    elif hand_total_bust(player_hand):
        print("\nDealer wins - Player bust.")
        update_balance("normal_loss", bet)


# Give player option to play another round.
def play_new_round(deck, player_hand, dealer_hand):
    global round_number
    # Ensure there are sufficient cards left to play with.
    if len(deck) >= 10:
        choices = {'Y', 'N'}
        while True:
            choice = input("\nPlay another hand? (Y/N): ")
            choice = choice.upper()
            if choice in choices:
                if choice == 'Y':
                    # Play new round.
                    round_number += 1
                    show_round()
                    clear_hand(player_hand)
                    clear_hand(dealer_hand)
                    return True
                else:
                    # End game.
                    print("\nThe player has left the table.")
                    return False
            else:
                print("Invalid choice.")
    else:
        print("Insufficient cards in the deck for another round!")


if __name__ == "__main__":
    play_game()
