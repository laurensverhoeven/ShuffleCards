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
import numpy as np
import functools
import os
from dominate import document
import dominate.tags as html

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
# - Gather all lists of suits and values in one place, instead of redifining in multple classes
# -
# -
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


class Email():

    _credentials_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(_credentials_path, "email_username"), 'r') as file:
        __sender_username = file.read()

    with open(os.path.join(_credentials_path, "email_password"), 'r') as file:
        __sender_password = file.read()

    def __init__(self, recipient, subject = "Test Subject", body="Body Text", body_html=None):
        """Create en email to send to a player."""
        self._recipient = recipient
        self.subject = subject
        self.body = body
        self.body_html = body_html

    def send(self):
        """Send an email."""

        # TODO: delete this
        # For testing
        self._recipient.email_address = self.__sender_username

        # print(
        #     f"Sending from email address {self.__sender_username} to "
        #     + f"{self._recipient} at {self._recipient.email_address} "
        #     + f"with subject '{self.subject}' and text: \n{self.body}"
        # )

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.__sender_username
        msg['To'] = ", ".join([self.__sender_username])

        # Record the MIME types of both parts - text/plain and text/html.
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        if self.body is not None:
            part1 = MIMEText(self.body.encode('utf-8'), _charset='utf-8')
            msg.attach(part1)
        if self.body_html is not None:
            part2 = MIMEText(str(self.body_html).encode('utf-8'), 'html', _charset='utf-8')
            msg.attach(part2)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.__sender_username, self.__sender_password)
            # server.sendmail(self.__sender_username, to, msg)
            server.sendmail(self.__sender_username, self.__sender_username, msg.as_string())
            server.close()

            print(f'Email "{self.subject}" to {self.__sender_username} sent!')
        except BaseException:
            print('Something went wrong...')
            raise


class Game():

    current_game = []

    def __init__(self, hand_size = 13):
        """Start a new game."""
        self.start_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.rule_set = None
        self.game_type = None
        self.value_ranking = None
        self.suit_ranking = None
        self.hand_size = hand_size
        self.__class__.current_game = self


class Round():

    start_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    dealer = None
    value_ranking = None
    suit_ranking = None
    # trump_suit = None


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

    _ranking_contexts = [
        "dealing",
        "playing",
    ]

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
        # TODO add option to take all, with 0, or leave N with negative counts N
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

    @property
    def hand_text(self):
        """Text for a player to view the cards in their hand."""

        time_string = Game.current_game.start_time
        card_text = "\n".join(str(card) for card in self.hand)

        hand_text = f"Je kaarten van {time_string} zijn:\n\n{card_text}"
        return(hand_text)

    @property
    def hand_text_fancy(self):
        """Text in columns per suit for a player to view the cards in their hand."""

        time_string = Game.current_game.start_time

        _suits = [
            "clubs",
            "diamonds",
            "hearts",
            "spades",
        ]
        cards_per_suit = {suit: CardSet() for suit in _suits}
        for card in self.hand:
            cards_per_suit[repr(card.suit)].append_card(card)

        text_rows = []
        text_rows.append(tuple(suit for suit in _suits))

        while any(cards_per_suit.values()):
            text_rows.append(
                tuple(cards_per_suit[suit].take_card(0) if cards_per_suit[suit] else "" for suit in _suits)
            )

        card_text = "\n".join(
            "".join(("{: <10}".format(str(card)) for card in row))
            for row in text_rows
        )
        hand_text = f"Je kaarten van {time_string} zijn:\n\n{card_text}"
        return(hand_text)

    @property
    def hand_text_html(self):
        """Text for a player to view the cards in their hand."""

        time_string = Game.current_game.start_time

        _suits = [
            "clubs",
            "diamonds",
            "hearts",
            "spades",
        ]
        cards_per_suit = {suit: CardSet() for suit in _suits}
        for card in self.hand:
            cards_per_suit[repr(card.suit)].append_card(card)
        # print(cards_per_suit)

        header_row = tuple(suit for suit in _suits)

        text_rows = []
        while any(cards_per_suit.values()):
            text_rows.append(
                tuple(cards_per_suit[suit].take_card(0) if cards_per_suit[suit] else "" for suit in _suits)
            )

        title = f"Cards for {self._name}"
        text = f"Je kaarten van {time_string} zijn:"

        with document(title=title) as hand_text:
            html.h1(title)
            html.p(text)
            with html.table().add(html.tbody()):
                line = html.tr()
                for cell in header_row:
                    line += html.td(str(cell))
                for text_row in text_rows:
                    line = html.tr()
                    for cell in text_row:
                        line += html.td(str(cell))

        return(hand_text)


def main():
    """Draw cards from deck for all players, then email them to them."""

    my_deck = CardDeck()
    my_deck.shuffle()

    Player("Joe", "joe@example.com")
    Player("Ted", "ted@example.com")
    Player("Anne", "anne@example.com")
    Player("Mary", "mary@example.com")

    Game(hand_size = 8)
    for player in Player.all_players:
        # print(player)
        # print(player.email_address)
        player.hand = my_deck.draw_cards(Game.current_game.hand_size)
        player.hand.sort(reverse=True)

    # for player in Player.all_players:
    #     print(player)
    #     print(player.hand_text)
    #     print(player.hand_text_fancy)
    #     print(player.hand_text_html)

    email1 = Email(
        player,
        subject=f"Kaarten voor klaverjas, geschud om {Game.current_game.start_time}",
        body=player.hand_text,
        body_html=player.hand_text_html,
    )
    email1.send()


def matrix_stuff():
    print()
    a = np.array([
        [5, 1, 3],
        [1, 1, 1],
        [1, 2, 1]
    ])
    b = np.array([1, 2, 3])
    print(a.dot(b))

    # standard_ranking = np.zeros((13, 13), dtype=int)
    # np.fill_diagonal(standard_ranking, 1)
    # print(standard_ranking)

    value_count = 8
    # standard_ranking2 = np.diag(np.full(value_count, 1))
    # print(standard_ranking2)

    klaverjas_ranking = np.zeros((value_count, value_count), dtype=int)
    diagonal_ranks = np.arange(-6, -value_count - 1, -1)
    klaverjas_ranking[diagonal_ranks, diagonal_ranks] = 1
    klaverjas_ranking[-1, -1] = 1
    klaverjas_ranking[-2, -5] = 1
    klaverjas_ranking[-3, -2] = 1
    klaverjas_ranking[-4, -3] = 1
    klaverjas_ranking[-5, -4] = 1

    # diagonal_ranks = np.insert(diagonal_ranks, 0, -1, axis=0)
    # print(diagonal_ranks)

    # shifted_diagonal_ranks = np.arange(-2, -4 - 1, -1)
    # print(shifted_diagonal_ranks)
    # klaverjas_ranking[shifted_diagonal_ranks - 1, shifted_diagonal_ranks] = 1

    klaverjas_ranking[-2, -5] = 1

    print(klaverjas_ranking)
    ranks = np.array(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", ], dtype=object)
    ranks = ranks[-value_count:]
    print(ranks)
    print(klaverjas_ranking.dot(ranks))

    klaverjas_trump_ranking = np.zeros((value_count, value_count), dtype=int)

    diagonal_ranks = np.arange(-7, -value_count - 1, -1)
    klaverjas_trump_ranking[diagonal_ranks, diagonal_ranks] = 1

    klaverjas_trump_ranking[-1, -4] = 1
    klaverjas_trump_ranking[-2, -6] = 1
    klaverjas_trump_ranking[-3, -1] = 1
    klaverjas_trump_ranking[-4, -5] = 1
    klaverjas_trump_ranking[-5, -2] = 1
    klaverjas_trump_ranking[-6, -3] = 1

    print(klaverjas_trump_ranking.dot(ranks))


def test():
    # TODO
    my_deck = CardSet()
    my_deck.append_card(Card("A", "clubs"))
    my_deck.append_card(Card("K", "clubs"))
    my_deck.append_card(Card("A", "spades"))
    my_deck.append_card(Card("A", "hearts"))
    my_deck.insert_card(2, Card("7", "diamonds"))
    print(my_deck)
    # for card in reversed(my_deck):
    #     print(card)

    my_deck2 = CardSet()
    my_deck2.append_card(Card("9", "spades"))
    my_deck2.append_card(Card("10", "hearts"))
    my_deck2.insert_card(2, Card("J", "diamonds"))
    print(my_deck2)

    # my_deck.append_cardset(my_deck2)
    my_deck.prepend_cardset(my_deck2)
    # my_deck.insert_cardset(3, my_deck2)
    print(my_deck)

    my_deck = CardDeck()
    my_deck.shuffle()
    print(my_deck)
    print(my_deck.find_card_positions(limit_value="10"))
    print(my_deck.find_card_positions(limit_value="10", limit_suit="clubs"))
    print(my_deck.find_card_positions(limit_suit="clubs"))


if __name__ == "__main__":
    main()
