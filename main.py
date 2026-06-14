import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============================================================================
# GLOBAL VARIABLES
# ============================================================================

suits = ['♠', '♥', '♦', '♣']
values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

player_hand = []
dealer_hand = []
active_game = False

# Session statistics
hands_played = 0
hands_won = 0
hands_lost = 0
hands_tied = 0


# ============================================================================
# GAME FUNCTIONS
# ============================================================================

def generate_card():
    """
    Generates a random card.

    Randomly selects a value (A, 2-10, J, Q, K) and a suit
    (♠, ♥, ♦, ♣), then combines them into a single card.

    Returns:
        str: A card in "value+suit" format, for example, "A♠" or "K♥".
    """
    value = random.choice(values)
    suit = random.choice(suits)
    return value + suit


def calculate_points(hand):
    """
    Calculates the total value of a hand of cards.

    Number cards are worth their number, face cards (J, Q, K) are worth 10,
    and Aces are worth 11 but become 1 if the total goes over 21.

    Parameter:
        hand (list): A list of cards as strings, for example ['A♠', 'K♥', '7♦'].

    Returns:
        int: The total points of the hand.
    """
    points = 0
    aces = 0

    # Count initial points
    for card in hand:
        value = card[:-1]  # Extract the value, everything except the suit

        if value == 'A':
            aces += 1
            points += 11
        elif value in ['J', 'Q', 'K']:
            points += 10
        else:
            points += int(value)

    # Adjust Aces from 11 to 1 if necessary to avoid going over 21
    while points > 21 and aces > 0:
        points -= 10
        aces -= 1

    return points


def new_game():
    """
    Starts a new Blackjack game.

    Deals 2 cards to the player and 2 cards to the dealer, then shows:
    - The player's full hand
    - Only the dealer's first card, while the second card stays hidden

    If the player gets 21 with 2 cards, the game ends automatically.
    """
    global player_hand, dealer_hand, active_game

    player_hand = [generate_card(), generate_card()]
    dealer_hand = [generate_card(), generate_card()]
    active_game = True

    print(f"\n{Fore.YELLOW}{'=' * 50}")
    print(f"{Fore.YELLOW}NEW GAME")
    print(f"{Fore.YELLOW}{'=' * 50}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}Your hand:{Style.RESET_ALL} {player_hand}")
    print(f"{Fore.CYAN}Points:{Style.RESET_ALL} {Fore.GREEN}{calculate_points(player_hand)}{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}Dealer's visible card:{Style.RESET_ALL} {dealer_hand[0]}")

    # Detect automatic Blackjack
    if calculate_points(player_hand) == 21:
        print(f"\n{Fore.GREEN}BLACKJACK! The game ends automatically.{Style.RESET_ALL}")
        stand()


def hit():
    """
    The player requests an additional card.

    Adds a new card to the player's hand and shows:
    - The updated hand
    - The total points

    If the player goes over 21, they automatically lose.
    If the player reaches exactly 21, they are notified.

    Requirement:
        The game must be active.
    """
    global player_hand, active_game, hands_played, hands_lost

    if not active_game:
        print(f"{Fore.RED}The game is not active. Start a new game first.{Style.RESET_ALL}")
        return

    player_hand.append(generate_card())
    points = calculate_points(player_hand)

    print(f"\n{Fore.CYAN}Your hand:{Style.RESET_ALL} {player_hand}")
    print(f"{Fore.CYAN}Points:{Style.RESET_ALL} {Fore.GREEN}{points}{Style.RESET_ALL}")

    if points > 21:
        print(f"{Fore.RED}BUST! You went over 21. You lost.{Style.RESET_ALL}")
        active_game = False
        hands_played += 1
        hands_lost += 1
        show_statistics()
    elif points == 21:
        print(f"{Fore.GREEN}21! You reached the maximum score.{Style.RESET_ALL}")


def stand():
    """
    The player ends their turn and the dealer plays automatically.

    Flow:
    1. Shows the dealer's full hand
    2. The dealer draws cards until reaching 17 or more points
    3. Compares points and determines the winner
    4. Records the result in the statistics

    Requirement:
        The game must be active. You cannot stand twice in the same round.
    """
    global dealer_hand, active_game, hands_played, hands_won, hands_lost, hands_tied

    if not active_game:
        print(f"{Fore.RED}The game is not active.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}{'=' * 50}")
    print(f"{Fore.YELLOW}DEALER'S TURN")
    print(f"{Fore.YELLOW}{'=' * 50}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}Dealer's hand:{Style.RESET_ALL} {dealer_hand}")

    # The dealer must reach 17 or more
    while calculate_points(dealer_hand) < 17:
        dealer_hand.append(generate_card())
        print(f"{Fore.MAGENTA}The dealer draws a card:{Style.RESET_ALL} {dealer_hand}")

    dealer_points = calculate_points(dealer_hand)
    print(f"{Fore.MAGENTA}Dealer's points:{Style.RESET_ALL} {Fore.GREEN}{dealer_points}{Style.RESET_ALL}")

    player_points = calculate_points(player_hand)

    print(f"\n{Fore.YELLOW}{'=' * 50}")
    print(f"{Fore.YELLOW}RESULT")
    print(f"{Fore.YELLOW}{'=' * 50}{Style.RESET_ALL}")

    print(f"{Fore.CYAN}Your score:{Style.RESET_ALL} {Fore.GREEN}{player_points}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Dealer's score:{Style.RESET_ALL} {Fore.GREEN}{dealer_points}{Style.RESET_ALL}")

    # Determine the winner and record the result
    hands_played += 1

    if dealer_points > 21:
        print(f"\n{Fore.GREEN}The dealer went over 21! YOU WIN!{Style.RESET_ALL}")
        hands_won += 1
    elif player_points > dealer_points:
        print(f"\n{Fore.GREEN}YOU WIN!{Style.RESET_ALL}")
        hands_won += 1
    elif player_points == dealer_points:
        print(f"\n{Fore.CYAN}TIE!{Style.RESET_ALL}")
        hands_tied += 1
    else:
        print(f"\n{Fore.RED}YOU LOST.{Style.RESET_ALL}")
        hands_lost += 1

    show_statistics()
    active_game = False


def show_statistics():
    """
    Shows the cumulative statistics for the current session.

    Information shown:
    - Total hands played
    - Hands won, lost, and tied
    - Win percentage, if at least one hand has been played

    Statistics are shown automatically after each hand
    and can also be requested from the main menu.
    """
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.CYAN}SESSION STATISTICS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

    print(f"{Fore.WHITE}Hands played:{Style.RESET_ALL} {Fore.GREEN}{hands_played}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Hands won:{Style.RESET_ALL} {Fore.GREEN}{hands_won}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Hands lost:{Style.RESET_ALL} {Fore.RED}{hands_lost}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Hands tied:{Style.RESET_ALL} {Fore.CYAN}{hands_tied}{Style.RESET_ALL}")

    if hands_played > 0:
        win_rate = (hands_won / hands_played) * 100
        print(f"{Fore.WHITE}Win percentage:{Style.RESET_ALL} {Fore.GREEN}{win_rate:.1f}%{Style.RESET_ALL}")


def menu():
    """
    Shows the main menu and controls the game flow.

    Available options:
    1. Play - Starts a new hand
    2. Hit - The player requests an additional card
    3. Stand - The player ends their turn and the dealer plays
    4. View statistics - Shows the current session statistics
    5. Exit - Closes the program

    The menu runs in an infinite loop until the user chooses Exit.
    """
    while True:
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{Fore.CYAN}BLACKJACK{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Play")
        print("2. Hit")
        print("3. Stand")
        print("4. View statistics")
        print(f"5. Exit{Style.RESET_ALL}")

        option = input(f"\n{Fore.YELLOW}Choose an option: {Style.RESET_ALL}")

        if option == "1":
            new_game()
        elif option == "2":
            hit()
        elif option == "3":
            stand()
        elif option == "4":
            show_statistics()
        elif option == "5":
            print(f"{Fore.GREEN}See you later, alligator!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid option.{Style.RESET_ALL}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    menu()