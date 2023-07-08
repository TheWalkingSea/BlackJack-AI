import random
import string
from typing import Any


class Hand:
    suits = ['♠', '♥', '♣', '♦']

    def __init__(self):
        self.cards = self._getCards(2)
    
    @property
    def _fcards(self) -> list[int]:
        """Property method that formats the cards to something a computer can read where Jack-King are represented as a 10
        
        Returns:
        (list[int]): List of the updated integers
        
        """
        fcards = list()
        for card in self.cards:
            fcards.append(10 if card > 10 else card)
        return fcards
    
    @staticmethod
    def getRandomCard() -> int:
        """Static method that returns a random integer from 1-14
        
        Returns:
        (int): Number from 1-14, Ace-King
        
        """
        return random.randint(1, 14)
    
    @staticmethod
    def _getCards() -> list[int]:
        """Static method that returns a list of two random cards 1-14

        Returns:
        (list[int]): Returns a list of 2 random numbers from 1-14

        """
        return [Hand.getRandomCard() for i in range(2)]

    def getCount(self) -> int:
        """Integer representing the count of the hand
        
        Returns:
        (int): An int representing the count
        
        """
        cnt = 0
        aces = 0
        for card in self._fcards:
            if (card == 1): aces += 1
            cnt += card
        # Check if there are any aces and if the count if 11 or less add the remaining 10 to make a stronger hand
        while (cnt <= 11 and aces > 0):
            cnt += 10 # The remaining 10 that we didnt add earlier
            aces -= 1
        return cnt

    def isBusted(self) -> bool:
        """Checks if the hand is a bust
        
        Returns:
        (bool): Boolean representing if the hand was a bust (True)
        
        """
        return self.getCount > 21 # If greater than 21 it is a bust

    def hit(self) -> bool:
        """Takes a hit and adds a card to cards; returns if busted
        
        Returns:
        (bool): A boolean representing if the hand was a bust (True)
        
        """
        self.cards.append(Hand.getRandomCard())
    
    def __str__(self): 
        """Returns a joined string of cards with their corresponding values aswell as a suit (Randomly chosen)
        
        Note: This should only be ran once because the suits are chosen randomly for each call of this function
        
        """
        return " ".join(list(map(lambda x: f"{random.choice(self.suits)}{x}", self.cards)))

    def checkBJ(self) -> bool:
        """Returns a boolean representing whether or not the hand has BJ
        
        Returns:
        (bool): If the hand has BJ returns True

        Prereq:
        len(self.cards) == 2

        """
        return sum(self.cards) == 21
    
class Balance:
    """Represents a round of blackjack as a dealer"""
    def __init__(self, initAmt: float, betAmt: float, ratio: tuple=(3, 2)):
        self.amt = initAmt
        self.betAmt = betAmt
        self.ratio = ratio
        self.flags = {"dd": False, "insure": False}

    def __iadd__(self, other: int):
        """Adds other and amt"""
        return self.amt + other

    def __isub__(self, other: int):
        """Subtracts amt from other"""
        return self.amt - other

    def bet(self, betAmt: float=None) -> bool:
        """Subtracts amt from betAmt
        
        Parameters:
        (betAmt): The bet amount, most of the time this will be self.betAmt but may adjust for insurance

        Returns:
        (bool): Boolean that will be False when there are insufficient funds
        
        """
        if (not betAmt): betAmt = self.betAmt
        if (self.amt < betAmt): return False
        self.amt -= betAmt
        return True

    def payout(self, ratio: tuple=None, bet: float=None) -> float:
        """Calculates the payout of the bet according to the ratio and changes the balance accordingly
        
        Parameters:
        ratio(tuple): Tuple representing the ratio. Ex: 3:2 means you will win $3 for every $2 you wager. Defaults to self.ratio
        bet(float): The bet amt in case you doubled down or split, defaults to self.betAmt
        
        Returns:
        (float): The payout
        """
        if (not ratio): ratio = self.ratio
        if (not bet): bet = self.betAmt
        payout = bet + bet/ratio[1]*ratio[0] # Give money back and then calculate the payout aswell
        self.amt += payout

        if (self.flags['dd']): # If double down is True, then double the payout
            self.amt += payout
            self.flags['dd'] = False # Set the flag to False

        if (self.flags['insure'] and ratio[1] == 0): # If insurance flag is set and the ratio signals pushing
            self.payout((2, 1), self.betAmt/2) # Insurance is half of a NEW bet and pays 2:1
            self.flags['insure'] = False

        return payout

class Dealer(Hand):
    def __init__(self):
        super(Hand, self).__init__() # Card 2 will be hidden from the player
    
    def getUpCard(self):
        """Getter function that will return the first card shown upwards to the player"""
        return self.cards[0]
    
    def playHand(self) -> None:
        """Plays the hand for the dealer and stops once it goes over 21"""

        # While 17 is greater than the count just keep hitting, we will deal with whether it busts or not later
        while (self.getCount() < 17): self.hit()
    
    def checkInsurance(self) -> bool:
        """Checks whether or not you can insurance is available or when the upCard is an Ace"""
        return self.getUpCard() == 1


class Player(Hand, Balance):
    """Represents a round of blackjack as a player"""
    dealer: Dealer = None

    def __init__(self, balance: Balance):
        super(Hand, self).__init__()
        self.bal = balance
    
    def predeterminedWin(self) -> int|None:
        """Checks for a predetermined win through blackjack represented as an int
        
        Returns:
        (int|None): 1 if the player has BJ, -0 if both the dealer and player have BJ,
            -1 if the dealer has BJ, and None if neither have BJ
            
        """
        if (self.dealer.checkBJ() and self.checkBJ()): # Push
            self.bal.payout((1, 0))
            return 0 
        if (self.dealer.checkBJ()):
            return -1
        if (self.checkBJ()):
            self.bal.payout()
            return 1
        return None


    def stand(self) -> int:
        """Player stands and this function will tell you if you win or lose
        
        Returns:
        (int): An integer representing whether you won (1), pushed (0), or loss (-1)
        
        """
        if (self.isBusted()): 
            return -1 # Checks if the player busts first

        self.dealer.playHand()
        if (self.dealer.isBusted()): 
            self.bal.payout()
            return 1 # Checks if the dealer busted

        playerCnt = self.getCount()
        dealerCnt = self.dealer.getCount()
        if (playerCnt == dealerCnt): # Push
            self.bal.payout((1, 0))
            return 0 
        
        # Finally just check the counts
        if playerCnt > dealerCnt:
            self.bal.payout()
            return 1
        return -1

    def checkSplit():
        raise NotImplementedError("Splitting is not supported yet")
    
    def split():
        raise NotImplementedError("Splitting is not supported yet")

    def __iadd__(self, other: Any): 
        raise NotImplementedError("In-place addition has not been implemented for the Player class")

    def __isub__(self, other: Any): 
        raise NotImplementedError("In-place subtraction has not been implemented for the Player class")

    def doubleDown(self) -> None:
        """Double bet and in return hit ONE card and stand. Also sets the flag for DD"""
        self.bal.bet() # Double the bet
        self.bal.flags['dd'] = True
        self.hit()
        self.stand()
    
    def checkEvenMoney(self) -> bool:
        """Checks if the player is eligible to even money; 
            when you have BJ and the dealer has an Ace as their upcard
            
        Note: Even money pays 1 to 1 with a guarenteed win rate but comes at an opportunity cost
        
        """
        return self.checkBJ() and self.dealer.checkInsurance()

    def insure(self) -> None:
        """Insures your bet by setting insurance flag
        
        Note: Insurance works by placing up to half your bet and
            if the dealer has blackjack the player is paid 2:1.
            Insurance and the bet are separate

        """
        self.bal.bet(self.bal.betAmt/2) # You have to bet half the original bet
        self.bal.flags['insure'] = True
    
    def evenMoney(self) -> None:
        """Changes the balance accordingly to even money, pays out 1:1
        
        Pre-req:
        checkEvenMoney is True
        
        """
        self.bal.payout((1, 1))