import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from ..game_sets.cards import Card, CARDS, CardType, Side, get_cards_by_era, get_scoring_cards

class Deck:
    def __init__(self):
        self.draw_pile:List[str] = []
        self.discard_pile:List[str] = []
        self.removed_pile:List[str] = []
        self._add_era()

    def _add_era(self, era:str = "Early War"):
        card_names = [name for name, card in CARDS.items() if card.era == era]
        self.draw_pile.extend(card_names)
        random.shuffle(self.draw_pile)

    def fill_hand(self, player_hand:List[str], n_cards:int = 8):
        while len(player_hand) < n_cards: 
            card_id = self._draw_card()
            player_hand.append(card_id)

    def _draw_card(self):
        if len(self.draw_pile) <= 0:
            raise Exception("Not enough draw pile cards!")
        card = self.draw_pile.pop()
        if len(self.draw_pile) == 0:
            self.discard_pile, self.draw_pile = self.draw_pile, self.discard_pile 
            random.shuffle(self.draw_pile)
        return card 

