import random
from itertools import product
import time
import os
import sys
clear = lambda: os.system('cls')
possible_card_values = ["A",2,3,4,5,6,7,8,9,10]
list_of_suits = ["H","S","C","D"]
list_of_values = ["A","2","3","4","5","6","7","8","9","10","J","K","Q"]

# List of all cards in a deck of cards
CARDS = list(map(lambda x: f"{x[0]}{x[1]}",list(product(list_of_values,list_of_suits))))



class Deck:
    def __init__(self,cards):
        """ Inits the deck with cards inside of it, and makes a list that will be filled with all cards dealt """
        self.cards = cards
        self.cards_dealt = list()

    def shuffle(self):
        """ shuffles deck randomly """
        random.shuffle(self.cards)

    def deal_cards(self,amount_to_deal_manually = False,time_per_deal = 5,silence=False):
       """ deals cards one at a time, it will choose a random amount to deal if not specified, it also has delays on how long it should display each card. It will clear the screen once all cards are dealt """
        amount_to_deal = random.randint(0,len(self.cards))
        if amount_to_deal_manually != False:
            amount_to_deal = amount_to_deal_manually

        for i in range(amount_to_deal):
            card_dealt = self.cards.pop()
            self.cards_dealt.append(card_dealt)
            if not silence:
                print(f"Dealing the card {card_dealt}")
            time.sleep(time_per_deal)
        print("OVER")
        clear()

    def convert_card_to_value(self,card):
        """ converts a card into it's value in blackjack """
        value = card[0]
        if value == "A":
            return "A"
        elif value in ["1","J","Q","K"]:
            return 10
        else:
            return int(value)

    def count_remaining(self):
        """ counts the remaining values in the deck """
        card_values_list = list(map(self.convert_card_to_value,self.cards))
        amount_of_each_card = dict()
        for value in card_values_list:
            if value not in amount_of_each_card:
                amount_of_each_card[value] = 1
            else:
                amount_of_each_card[value] += 1
        return amount_of_each_card

    def card_to_highlow_value(self,value):
        """ finds card values using the high low system """
        if value == "A":
            return -1
        elif value>9:
            return -1
        elif 6<value<=9:
            return 0
        else:
            return 1

    def hilow_value_from_dealt(self):
        """ finds the count from all cards dealt """
        card_dealt_values_list = list(map(self.convert_card_to_value,self.cards_dealt))
        count = sum(list(map(self.card_to_highlow_value,card_dealt_values_list)))
        return count

    def show_cards(self):
        """ returns the cards left in the deck """
        return self.cards


class Game:
    def __init__(self,mode,amount_of_decks):
        self.mode = mode
        self.amount_of_decks = amount_of_decks

    def check_win_high_low(self,deck_of_cards: Deck):
        """ checks if player has won with the normal mode """
        user_input = int(input("please type the count: "))
        true_count = deck_of_cards.hilow_value_from_dealt()
        if user_input == true_count:
            print("well done buddy")
        else:
            print(f"sorry, the true count was {true_count}")


    def check_win_memory(self,deck_of_cards: Deck):
        """ checks if player has won in genius mode """
        user_guesses = dict()
        for card_value in possible_card_values:
            user_inp = input(f"how many {card_value}s are left in the deck? ")
            user_guesses[card_value] = int(user_inp)

        if user_guesses == deck_of_cards.count_remaining():
            print("well done buddy")
        else:
            print(f"no, here is the correct amount of each value {deck_of_cards.count_remaining()}")

    def check_win_memory_super(self,deck_of_cards: Deck):
        """ checks if player has won in super genius mode """
        user_guesses = list()
        print(f"there are {len(deck_of_cards.show_cards())} cards left in the deck, can you name them all")
        for i,card in enumerate(deck_of_cards.show_cards()):
            card_guess = input(f"please type in the cards, one card at a time. Card number {i+1} was: ")
            user_guesses.append(card_guess)
        if set(user_guesses) == set(deck_of_cards.show_cards()):
            print("well done buddy")
        else:
            print(f"sorry, the cards left were \n {deck_of_cards.show_cards()}")


    def play(self):
        """ main method - spawns the deck, shuffles them and deals a random amount """
        all_cards = [card for card in CARDS for _ in [x for x in range(self.amount_of_decks)]]
        deck_of_cards = Deck(all_cards)
        deck_of_cards.shuffle()
        deck_of_cards.deal_cards(amount_to_deal_manually=False)
        if self.mode == "g":
            self.check_win_memory(deck_of_cards=deck_of_cards)
        elif self.mode == "n":
            self.check_win_high_low(deck_of_cards=deck_of_cards)
        else:
            self.check_win_memory_super(deck_of_cards=deck_of_cards)






# GAME START
#Players chooses a mode and amount of decks
MODE = input("What mode would you like, normal 👎 or genius (g) or super genius (sg)? \n normal uses the high low system for counting cards while genius expects you to say how many of each value are left in the deck and supe genius expexts you to write all remaining cards in the deck \n")
if MODE in ["g","n","sg"]:
    deck_num = int(input("how many decks would you like to play? "))
    game = Game(MODE,deck_num)
    game.play()

else:
    print("please type in g or n or sg for the mode")
    sys.exit()
