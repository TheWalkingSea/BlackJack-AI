import random
import string



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

    def IsBusted(self) -> bool:
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

    def hasBJ(self) -> bool:
        """Returns a boolean representing whether or not the hand has BJ
        
        Returns:
        (bool): If the hand has BJ returns True

        Prereq:
        len(self.cards) == 2

        """
        return sum(self.cards) == 21
    
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
    

class Player(Hand):
    dealer: Dealer = None

    def __init__(self):
        super(Hand, self).__init__()
    
    def stand(self) -> int:
        """Player stands and this function will tell you if you win or lose
        
        Returns:
        (int): An integer representing whether you won (1), pushed (0), or loss (-1)
        
        """
        if (self.isBusted()): return -1 # Checks if the player busts first

        self.dealer.playHand()
        if (self.dealer.IsBusted()): return 1 # Checks if the dealer busted

        playerCnt = self.getCount()
        dealerCnt = self.dealer.getCount()
        if (playerCnt == dealerCnt): return 0 # Push
        return 1 if playerCnt > dealerCnt else -1 # Finally just check the counts
