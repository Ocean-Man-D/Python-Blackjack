import random
from os import system, name


class Card:
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit
        pass

    def __repr__(self) -> str:
        ranks = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        suits = {"D": "♦️", "C": "♣️", "H": "♥️", "S": "♠️"}
        return f"{suits[self.suit]} {ranks.get(self.rank, self.rank)}"


class Deck:
    def __init__(self) -> None:
        self.cards = []
        for suit in ["D", "C", "H", "S"]:  # Diamonds, Clubs, Hearts, Spades
            for rank in range(1, 14):
                self.cards.append(Card(rank, suit))
        pass

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Hand:
    def __init__(self) -> None:
        self._cards = []
        self._value = 0
        self._ace = False
        self._soft = False
        pass

    def __repr__(self) -> str:
        return f"Total hand value: {self._value} {'(Soft hand) ' if self._soft else ''}"

    def add_card(self, card):
        self._cards.append(card)
        if 11 <= card.rank <= 13:
            self._value += 10
        elif card.rank == 1:
            self._ace = True
            self._value += 11
        else:
            self._value += card.rank
        if self._value > 21:
            if self._ace and not self._soft:
                self._value -= 10
                self._soft = True

    @property
    def cards(self):
        return self._cards

    @property
    def value(self):
        return self._value

    @property
    def ace(self):
        return self._ace

    @property
    def soft(self):
        return self._soft


class Player:
    def __init__(self) -> None:
        self.hand = Hand()
        self.stand = False
        pass

    def hit(self, deck):
        card = deck.deal()
        self.hand.add_card(card)


class Blackjack:
    def __init__(self) -> None:
        self.deck = None
        self.dealer = None
        self.player = None
        pass

    def start(self):
        self.deck = Deck()
        self.dealer = Player()
        self.player = Player()
        self.deck.shuffle()
        for p in (self.dealer, self.player):
            p.hit(self.deck)
            p.hit(self.deck)
        self.player_turn()

    def player_turn(self):
        if self.player.hand.value > 21:
            self.end_game()
        elif self.player.hand.value == 21:
            self.end_game()
        elif self.player.stand:
            self.dealer_turn()
        else:
            clear()
            print(f"Dealer's first card: {self.dealer.hand.cards[0]}")
            print("")
            print("Cards in hand:")
            for card in self.player.hand.cards:
                print(card)
            print(self.player.hand)
            print("")
            user_input = input("Choose action: (H)it/(S)tand ").lower()
            if user_input == "h":
                self.player.hit(self.deck)
            elif user_input == "s":
                self.player.stand = True
            else:
                print("Invalid input.")
            self.player_turn()

    def dealer_turn(self):
        if self.dealer.hand.value > 21:
            self.end_game()
        elif self.dealer.hand.value == 21:
            self.end_game()
        elif self.dealer.hand.value < 17:
            self.dealer.hit(self.deck)
            self.dealer_turn()
        else:
            self.end_game()

    def end_game(self):
        reason = ""
        if self.player.hand.value > 21:
            reason = "Bust! You Lose!"
        elif self.dealer.hand.value > 21:
            reason = "Dealer Bust! You Win!"
        elif self.player.hand.value == 21:
            reason = "Blackjack! You Win!"
        elif self.dealer.hand.value == 21:
            reason = "Dealer Blackjack! You Lose!"
        elif self.player.hand.value == self.dealer.hand.value:
            reason = "Draw!"
        elif self.player.hand.value > self.dealer.hand.value:
            reason = "Higher Hand! You Win!"
        else:
            reason = "Lower Hand! You Lose!"
        clear()
        print("Dealer's cards:")
        for card in self.dealer.hand.cards:
            print(card)
        print(self.dealer.hand)
        print("")
        print("Your cards:")
        for card in self.player.hand.cards:
            print(card)
        print(self.player.hand)
        print("")
        print(reason)
        user_input = input("Play again? (Y)es/(N)o ").lower()
        if user_input == "n":
            print("Program has ended.")
        elif user_input == "y":
            self.start()
        else:
            self.end_game()


def clear():
    if name == "nt":  # Windows
        system("cls")
    else:  # Mac, Linux
        system("clear")


game = Blackjack()
game.start()
