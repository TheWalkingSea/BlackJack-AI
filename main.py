import random
import string



class Hand:
    suits = ['♠', '♥', '♣', '♦']

    def __init__(self, numCards: int):
        self.cards = self._getCards(numCards)
    
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
    
    def _getCards(self, num: int) -> list[int]|int:
        """Gets num amount of cards to play with
        
        Parameters:
        num(int): The number of cards to generate
        
        Returns:
        (list[int]|int): Returns one card or a list of cards if num > 1
        
        Pre:
        num <= 2; If not then a nested list will be returned
        """
        card = Hand.getRandomCard() # Ace - King
        if (num == 1): return card
        return [card, self._getCards(num-1)]

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

    def checkBust(self) -> bool:
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

class Player(Hand):
    def __init__(self):
        super(Hand, self).__init__(2)

class Dealer(Hand):
    def __init__(self):
        super(Hand, self).__init__(1)
