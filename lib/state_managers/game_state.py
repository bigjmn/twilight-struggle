import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum

from ..game_sets.countries import Country, COUNTRIES, Region, Superpower, calculate_region_control, InfluenceChange
from ..game_sets.cards import Card, CARDS, CardType, Side, get_cards_by_era, get_scoring_cards
from ..game_sets.constants import GamePhase, Superpower 
from .space_race import SpaceRace
from .deck import Deck


# Todo - common subroutines (usa_choosecard, triggers chooser to be usa and options to be usa hand, China card parameter as flag etc)
@dataclass
class GameState:

    turn:int = 1 
    phase: GamePhase = GamePhase.SETUP
    action_round:int = 1 
    player_ar: Optional[Superpower] = None 

    space_race = SpaceRace()

    # chooser is player making decision
    chooser: Superpower = Superpower.USA

    vp_track: int = 0 # positive = USA! USA! USA! 

    # hands have card ids? 
    usa_hand: List[str] = []
    ussr_hand: List[str] = []

    # visible cards 
    usa_hand_visible: List[str] = []
    ussr_hand_visible: List[str] = []

    deck:Deck = Deck()
    defcon_level:int = 0

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

    # -- observation array converter and helpers -- 

    # deck to observation
    def _deck_to_obs(self, player:Superpower):
        deck_obs = []
        # [in_hand, in_discard, is_removed, drawpile_or_opphand, in_opphand, not_in_game]
        playerhand = self.usa_hand if player == Superpower.USA else self.ussr_hand
        opphand = self.ussr_hand if player == Superpower.USA else self.usa_hand
        oppvisible = self.ussr_hand_visible if player == Superpower.USA else self.usa_hand_visible
        
        for key, value in CARDS.items():
            card_ob = [0, 0, 0, 0, 0, 0]
            if key in playerhand:
                card_ob[0] = 1 
            if key in self.deck.discard_pile:
                card_ob[1] = 1 
            if key in self.deck.removed_pile:
                card_ob[2] = 1 
            if key in self.deck.draw_pile or key in opphand:
                card_ob[3] = 1 
            if key in oppvisible:
                card_ob[4] = 1 
            if key not in self.deck.added_list:
                card_ob[5] = 1 
            deck_obs.extend(card_ob)
        return deck_obs
            
            

            



