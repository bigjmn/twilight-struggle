import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum

from ..game_sets.countries import Country, COUNTRIES, Region, Superpower, calculate_region_control, InfluenceChange
from ..game_sets.cards import Card, CARDS, CardType, Side, get_cards_by_era, get_scoring_cards
from ..game_sets.constants import GamePhase, Superpower 

from .deck import Deck


# Todo - common subroutines (usa_choosecard, triggers chooser to be usa and options to be usa hand, China card parameter as flag etc)
@dataclass
class GameState:

    turn:int = 1 
    phase: GamePhase = GamePhase.SETUP
    action_round:int = 1 
    player_ar: Optional[Superpower] = None 

    # chooser is player making decision
    chooser: Superpower = Superpower.USA

    vp_track: int = 0 # positive = USA! USA! USA! 

    # hands have card ids? 
    usa_hand: List[str] = []
    ussr_hand: List[str] = []

    deck:Deck = Deck()

    def __post_init__(self):
        if not self.countries:
            # Deep copy countries to avoid modifying the original
            self.countries = {name: Country(
                name=country.name,
                region=country.region,
                stability=country.stability,
                battleground=country.battleground,
                adjacent_countries=country.adjacent_countries.copy(),
                us_influence=country.us_influence,
                ussr_influence=country.ussr_influence
            ) for name, country in COUNTRIES.items()}

    def _fill_hands(self):
        self.deck.fill_hand(self.usa_hand)
        self.deck.fill_hand(self.ussr_hand)

    def _apply_influence_changes(self, changes:List[InfluenceChange]):
        for (country_name, usa_change, ussr_change) in changes:
            self.countries[country_name]._change_influence(usa_change, ussr_change)
            

            



