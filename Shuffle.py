#!/usr/bin/env python3

"""Python program to shuffle a deck of card."""

# importing modules
# import itertools
import random
# from pprint import pprint, pformat
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import numpy as np
import functools

# TODO
# - Allow for choosing the cards that are in the deck
# - Allow for choosing the number of players
# - Allow for choosing the method of dealing cards
# - Make presets for different games
#   - Klaverjassen
#   - Bridge
#   - Toepen
#   -
# - Allow for changing email text:
#   - Change subject
#   - Send multiple games at once
#   - Give the set of games a custom name
#   - Give every individual game a custom name
#   - Make a Web UI interface
#   -
# - Allow for a sets of shared 'OpenCards' to be included in every email
# - Make Text in email HTML table
# - Add name of player in email text
# - Allow for changing the ranking of cards: klaverjas ranking
# - In klaverjas, allow for adding ranking overview + points of cards to email
# - Allow for adding rules of game to email
# - Allow for adding the settings that were used to generate the game to email, including other players
# - Allow for choosing language of email
# - Allow for adding clickable checkboxes for the cards in the email, to keep track of what has been played
# - Find out if random's shuffle is random enough
# - Store Suit and value of cards stored in 4-vector, to determine card value with matrix?
# -

# Done
# - Remove passwords and emailaddresses from file
# - Make object oriented

# Classes
# - Card
#     - Suit
#     - Value
#     - Points
#     - Rank
#     -
#     -
# - Player
# - CardSet -> Use Abstract Base Class Sequence: https://docs.python.org/3/library/collections.abc.html
#   https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/
#   - Deck -> repr shows lengths
#   - Hand -> repr shows cards
#   - OpenCards  -> repr shows cards
#   -
# -
# -
# -
# -


def SendEmail(subject = "Test Onderwerp", body="Body Text", to = []):
    """Send an email."""

    with open("email_username", 'r') as file:
        gmail_user = file.read()
    with open("email_password", 'r') as file:
        gmail_password = file.read()

    print(f"Sedning from email address {gmail_user}")

    sent_from = gmail_user

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = ", ".join(to)

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(body, 'plain')
    part1 = MIMEText(body.encode('utf-8'), _charset='utf-8')
    # msg = MIMEText('€10'.encode('utf-8'), _charset='utf-8')
    # part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    # msg.attach(part2)

    # msg = MIMEText(msg.encode('utf-8'), _charset='utf-8')

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        # server.sendmail(sent_from, to, msg)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()

        print(f'Email "{subject}" to {to} sent!')
    except BaseException:
        print('Something went wrong...')
        raise

    return()


def HandToStringFancy(Hand):
    """Format the cards in the given hand, arranging them in columns per suit."""
    # print(time_string)
    # HandText = f"Je kaarten van {time_string} zijn:\n\n"
    HandText = f"Je kaarten van zijn:\n\n"

    Suits = []
    CardRanks = []
    CardsPerSuit = {SuitNum: [] for SuitNum in Suits}

    for suit_num, card_num in Hand:
        CardsPerSuit[suit_num].append(f"{Suits[suit_num]} {CardRanks[card_num]}")

    TextRows = []
    TextRows.append(f"{Suits[suit_num]}" for suit_num in Suits)
    # TextRows.append(f"{Suits[suit_num]}" for suit_num in Suits.keys())
    # TextRows.append(("", "", "", ""))

    while any(CardsPerSuit.values()):
        TextRows.append([CardsPerSuit[SuitNum].pop() if CardsPerSuit[SuitNum] else "" for SuitNum in Suits])
        # print(CardsPerSuit.values())

    # Lines = [f"{Suits[suit_num]} {Cards[card_num]}" if   for suit_num, card_num in CardsPerSuit]

    # pprint(TextRows)
    for Row in TextRows:
        # print(Row)

        HandText += " {: <5} {: <5} {: <5} {: <5}\n".format(*Row)
    # CardsPerSuit = list(map(list, zip(*CardsPerSuit)))

    # Matrix = [[0 for x in range(w)] for y in range(h)]
    # pprint(CardsPerSuit)

    CardsPerSuit = [
        [f"{Suits[suit_num]} {CardRanks[card_num]}" if suit_num == Suit else "" for suit_num, card_num in Hand]
        for Suit in Suits
    ]

    # pprint(CardsPerSuit)


@functools.total_ordering
class Suit():
    """Suit with rank and name."""

    _name = [
        "clubs",
        "diamonds",
        "hearts",
        "spades",
    ]
    _symbols = {
        "clubs": "♣",
        "diamonds": "♢",
        "hearts": "♡",
        "spades": "♠",
    }
    # _symbols = {
    #     "clubs": "♣",
    #     "diamonds": "♦",
    #     "hearts": "♥",
    #     "spades": "♠",
    # }

    def __repr__(self):
        return(self._name[self._rank])

    def __str__(self):
        return(self._symbols[self.__repr__()])

    def __init__(self, name):
        """Create Suit. Give a rank(str)."""
        self._rank = self._name.index(name)

    # https://stackoverflow.com/a/29429106/5633770
    def __eq__(self, other):
        return(self._rank == other._rank)

    def __lt__(self, other):
        return(self._rank < other._rank)


@functools.total_ordering
class Value():
    """Card value with rank and name."""

    _ranking = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "Q",
        "K",
        "10",
        "A",
        "9",
        "J",
    ]
    # values = [Value(value_rank, value_name) for value_rank, value_name in enumerate(value_ranking)]

    def __repr__(self):
        return(self._ranking[self._rank])

    def __init__(self, name):
        """Create Suit. Give the name(str)."""
        self._rank = self._ranking.index(name)

    # https://stackoverflow.com/a/29429106/5633770
    def __eq__(self, other):
        return(self._rank == other._rank)

    def __lt__(self, other):
        return(self._rank < other._rank)


@functools.total_ordering
class Card():
    """Card with value and suit."""

    def __repr__(self):
        return(f"{self.value} {self.suit}")

    # def __str__(self):
    #     return(f"{self.value}\u2009{self.suit}")

    def __init__(self, value, suit):
        """Create card. Give value(int) and suit(str)."""
        self.value = Value(value)
        self.suit = Suit(suit)

    # https://stackoverflow.com/a/29429106/5633770
    def __eq__(self, other):
        return(self.suit == other.suit and self.value == other.value)

    def __lt__(self, other):
        if self.suit != other.suit:
            return(self.suit < other.suit)
        else:
            return(self.value < other.value)


class CardSet():
    """Set of Cards."""

    def check_card(self, position):
        pass

    def pick_card(self, method="random"):
        pass

    def __len__(self):
        return(len(self._cards))

    def __getitem__(self, position):
        return(self._cards[position])

    def __setitem__(self, position, card):
        self._cards[position] = card
        return()

    def __delitem__(self, position):
        # https://stackoverflow.com/a/48139870/5633770
        del self._cards[position]
        return()

    def __iter__(self):
        return(iter(self._cards))

    def __reversed__(self):
        return(reversed(self._cards))

    def __contains__(self, card):
        return(card in self._cards)

    def insert_card(self, position, card):
        # https://stackoverflow.com/a/48139870/5633770
        self._cards[position:position] = [card]
        return()

    def append_card(self, card):
        self.insert_card(len(self), card)
        return()

    def prepend_card(self, card):
        self.insert_card(0, card)
        return()

    def take_card(self, position):
        return(self._cards.pop(position))

    def draw_card(self):
        return(self.take_card(-1))

    def find_card_positions(self, limit_value=None, limit_suit=None, limit_count=0, start_position=0, step_size=1):
        positions = [
            position for position, card
            in enumerate(self._cards) if
            (limit_value is None or str(card.value) == limit_value)
            and (limit_suit is None or repr(card.suit) == limit_suit)
        ]
        return(positions)

    def insert_cardset(self, position, card_set):
        # https://stackoverflow.com/a/48139870/5633770
        self._cards[position:position] = [card for card in card_set]
        return()

    def append_cardset(self, card_set):
        self.insert_cardset(len(self), card_set)
        return()

    def prepend_cardset(self, card_set):
        self.insert_cardset(0, card_set)
        return()

    def take_cards(self, position, count):
        taken_cards = CardSet()
        for _ in range(count):
            taken_cards.append_card(self.draw_card())
        return(taken_cards)

    def draw_cards(self, count):
        return(self.take_cards(-1, count))

    def shuffle(self):
        random.shuffle(self._cards)
        return()

    def sort(self, reverse=False):
        # self._cards.sort(key=lambda card: card.value, reverse = False)
        # self._cards.sort(key=lambda card: card.suit, reverse = False)
        self._cards.sort(reverse=reverse)

    def __repr__(self):
        return(str([card for card in self._cards]))

    def __init__(self):
        """Create set of cards, initially empty."""
        self._cards = []


class CardDeck(CardSet):
    """Deck of Cards. Used to bring new cards into play."""

    _deck_types = {
        "52": [],
        "54": [],
        "32": [],
    }

    _suits = [
        "clubs",
        "diamonds",
        "hearts",
        "spades",
    ]

    _values = [
        # "2",
        # "3",
        # "4",
        # "5",
        # "6",
        "7",
        "8",
        "9",
        "10",
        "J",
        "Q",
        "K",
        "A",
    ]

    def __init__(self, deck_type="52", additional_cards=None, excldued_cards=None, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._cards = [Card(value, suit) for suit in self._suits for value in self._values]


class Player():

    all_players = []

    def __init__(self, name, email_address):
        """Add a new player."""
        self._name = name
        self.email_address = email_address
        self.hand = CardSet()
        self.all_players.append(self)

    def __repr__(self):
        return(self._name)


def main():
    """Draw cards from deck for all players, then email them to them."""

    # my_deck = CardSet()
    # my_deck.append_card(Card("A", "clubs"))
    # my_deck.append_card(Card("K", "clubs"))
    # my_deck.append_card(Card("A", "spades"))
    # my_deck.append_card(Card("A", "hearts"))
    # my_deck.insert_card(2, Card("7", "diamonds"))
    # print(my_deck)
    # # for card in reversed(my_deck):
    # #     print(card)

    # my_deck2 = CardSet()
    # my_deck2.append_card(Card("9", "spades"))
    # my_deck2.append_card(Card("10", "hearts"))
    # my_deck2.insert_card(2, Card("J", "diamonds"))
    # print(my_deck2)

    # # my_deck.append_cardset(my_deck2)
    # my_deck.prepend_cardset(my_deck2)
    # # my_deck.insert_cardset(3, my_deck2)
    # print(my_deck)

    my_deck = CardDeck()
    my_deck.shuffle()
    print(my_deck)
    print(my_deck.find_card_positions(limit_value="10"))
    print(my_deck.find_card_positions(limit_value="10", limit_suit="clubs"))
    print(my_deck.find_card_positions(limit_suit="clubs"))

    # print()
    # player_count = 4
    # hand_size = 8
    # print(my_deck)
    # hands = [my_deck.draw_cards(hand_size) for _ in range(player_count)]
    # # hand1 = my_deck.draw_cards(hand_size)
    # # print(my_deck)
    # for hand in hands:
    #     # print()
    #     # print(hand)
    #     hand.sort(reverse=True)
    #     # hand.sort(reverse=False)
    #     print(hand)

    Player1 = Player("Joe", "joe@example.com")
    Player2 = Player("Ted", "ted@example.com")
    Player2 = Player("Anne", "anne@example.com")
    Player2 = Player("Mary", "mary@example.com")

    hand_size = 8
    for player in Player.all_players:
        # print(player)
        # print(player.email_address)
        player.hand = my_deck.draw_cards(hand_size)
        player.hand.sort(reverse=True)

    for player in Player.all_players:
        print(player)
        print(player.hand)


    # hand_texts = []
    # time_string = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    # for hand in hands:
    #     hand_text = f"Je kaarten van {time_string} zijn:\n\n"
    #     for card in hand:
    #         hand_text += f"{card}\n"
    #     hand_texts.append(hand_text)

    # for hand_texts in hand_texts:
    #     pass
    #     print(hand_texts)

    # print(Player1.hand)

    # # print(list(zip(Recipients, hand_texts)))
    # for Recipient, hand_text in zip(Recipients, hand_texts):
    #     SendEmail(
    #         body = hand_text,
    #         to = [Recipient],
    #         subject = "Kaarten voor klaverjas, geschud om " + time_string
    #     )
    #     # break


if __name__ == "__main__":
    main()
