import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self):

        self.all_cards_in_deck = []
        for suit in suits:
            for rank in ranks:
                new_card = Card(rank, suit)
                self.all_cards_in_deck.append(new_card)

    def shuffle_deck(self):
        random.shuffle(self.all_cards_in_deck)

    def remove_card_from_deck(self):
        card = self.all_cards_in_deck.pop()
        return card


class Player:
    def __init__(self, remaining_chips, player_name):
        self.remaining_chips = remaining_chips
        self.name = player_name
        self.cards = []
        self.cards_value = 0
        self.aces = 0

    def add_chips(self, chips_to_add):
        self.remaining_chips += chips_to_add

    def remove_chips(self, chips_to_remove):
        self.remaining_chips -= chips_to_remove

    def add_to_players_cards(self, new_cards):
        # Add a single card object
        self.cards.append(new_cards)
        if new_cards.rank == 'Ace':
            self.aces += 1

    def calculate_player_cards_value(self):
        self.cards_value = calculate_cards_value(self.cards)
        if self.aces > 0:
            self.adjust_for_ace()
        return self.cards_value

    def adjust_for_ace(self):
        while self.cards_value > 21 and self.aces > 0:
            self.cards_value -= 10
            self.aces -= 1


class Dealer:
    def __init__(self):
        self.cards = []
        self.cards_value = 0

    def add_to_dealers_cards(self, new_cards):
        # Add a single card object
        self.cards.append(new_cards)

    def calculate_dealer_cards_value(self):
        self.cards_value = calculate_cards_value(self.cards)
        return self.cards_value


def calculate_cards_value(cards):
    card_val = 0
    for card in cards:
        card_val += card.value
    return card_val


def show_cards(player, dealer, show_all_cards):
    # if we don't want to show all the cards
    if not show_all_cards:
        print("\nDealer's Hand:")
        print("<Dealer Card Hidden>")
        print(" ", dealer.cards[1])
        print("\nPlayer's Hand:", *player.cards, sep='\n ')
    else:
        print("\nDealer's Hand:", *dealer.cards, sep='\n ')
        print("Dealer's Hand =", dealer.calculate_dealer_cards_value())
        print("\nPlayer's Hand:", *player.cards, sep='\n ')
        print("Player's Hand =", player.calculate_player_cards_value())


def deal_cards(player, dealer, deck, add_to_player):
    times = 0
    # if it is not the case of a hit, add two cards to the dealer and the players hand
    while times < 2:
        cards = deck.remove_card_from_deck()
        if add_to_player:
            player.add_to_players_cards(cards)
            times += 1
        else:
            dealer.add_to_dealers_cards(cards)
            times += 1


def deal_cards_after_hit(player, deck):
    card = deck.remove_card_from_deck()
    player.add_to_players_cards(card)
    player.adjust_for_ace()


def dealer_hit_and_win(dealer, player, deck, ):
    while dealer.calculate_dealer_cards_value() < player.calculate_player_cards_value():
        card = deck.remove_card_from_deck()
        dealer.add_to_dealers_cards(card)
        show_cards(player, dealer, False)
    if dealer.calculate_dealer_cards_value() > 21:
        return False
    return True


def player_lost(player, bet):
    player.remove_chips(bet)
    print(f"You lost! You have lost {bet} chips and have {player.remaining_chips} chips remaining")
    return


def player_won(player, bet):
    chips_to_add = bet * 2
    player.add_chips(chips_to_add)
    print(f"You won! You have won {chips_to_add} chips and have {player.remaining_chips} chips remaining")
    return


def play_again():
    answer = input("Would you like to play again? Y/N\n")
    if answer == "Y":
        return True
    return False


def player_hit():
    while True:
        decision = input("Would you like to hit? Y/N\n")
        if decision[0] == 'Y':
            return True
        elif decision[0] == 'N':
            print("Player Stands. Dealers Turn")
            return False
        else:
            print("Wrong input! Please enter Y or N only")


def play_game():
    # start the game
    print("Welcome to BlackJack! May the odds ever be in your favor")
    # get players name
    name = input("Please enter your name \n")
    game_on = True
    invalid_input = True
    add_to_player = True
    show_all_cards = False
    player_loses = False
    # create player object
    player = Player(100, name)
    # create dealer object
    dealer = Dealer()
    # create and shuffle a new deck
    new_deck = Deck()
    new_deck.shuffle_deck()
    while game_on:
        # make sure a valid bet is placed
        while invalid_input:
            try:
                bet = int(input("Please enter your bet: "))
                if bet > player.remaining_chips:
                    print("Not enough money to place bet. Please bet again")
                    continue
                invalid_input = False
            except ValueError:
                print("Error! Only allowed to bet monetary amounts i.e: using integers")
                continue
        # give 2 cards to player and 2 cards to dealer
        deal_cards(player, dealer, new_deck, add_to_player)
        deal_cards(player, dealer, new_deck, add_to_player=False)
        # show the cards of the dealer and the player
        show_cards(player, dealer, show_all_cards)
        # keep asking the player if he wants to hit again
        while player_hit():
            # deal the cards
            deal_cards_after_hit(player, new_deck)
            # show the cards
            show_cards(player, dealer, show_all_cards)
            # if the player busts then the player loses
            if player.calculate_player_cards_value() > 21:
                player_lost(player, bet)
                show_cards(player, dealer, show_all_cards=True)
                player_loses = True
                break
        # if the player stands, then the dealer starts to hit. if the dealer wins then the player lost
        if not player_loses:
            if dealer_hit_and_win(dealer, player, new_deck):
                player_lost(player, bet)
                show_cards(player, dealer, show_all_cards=True)
            # if we reach here the player had won
            else:
                player_won(player, bet)
                show_cards(player, dealer, show_all_cards=True)
        if play_again():
            continue
        game_on = False
        print(f"Thank you for playing {player.name}! Come again soon")


if __name__ == '__main__':
    play_game()

