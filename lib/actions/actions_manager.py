import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from ..game_sets.countries import Country
from ..game_sets.constants import Superpower
from ..state_managers.game_state import GameState
from .selectors import Selectors
from collections import Counter
class ActionType(Enum):
    INFLUENCE = "influence"
    COUP = "coup"
    REALIGNMENT = "realignment"
    EVENT = "event"
    SPACE_RACE = "space_race"
    EVENT_CHOICE = "event_choice"
    HEADLINE_CHOICE = "headline_choice"


@dataclass 
class GameAction:
    
    # -- legality of specific actions -- 

    # legality of placing influence for ops. choices is list of country ids 
    def _influence_placements_legal(self, player:Superpower, gamestate:GameState, choices:List[str], ops_available:int):
        # track remaining ops 
        ops_remaining = ops_available
        # get list of countries where influence can be placed 
        
        access_countries = {key: value for key, value in gamestate.countries.items() if value._has_access(player)}

        

        
        for country_id in choices:
            country = access_countries[country_id]
            ops_remaining -= country.influence_cost(player)
            if player == Superpower.USA:
                country.us_influence += 1 
            else:
                country.ussr_influence += 1 
        return ops_remaining == 0
    
    # legality of coup. choices is list (size 1) of target ids
    def _coup_legal(self, player:Superpower, gamestate:GameState, choices:List[str], ops_available:int):
        if len(choices) != 1:
            return False 
        coup_target_id = choices[0]
        curr_defcon = gamestate.defcon_level
        if gamestate.countries[coup_target_id].can_coup_or_realign(curr_defcon, player):
            return True 
        return False 
    
    # legality of re-align. choices is list (size 1) of target ids
    def _realign_legal(self, player:Superpower, gamestate:GameState, choices:List[str], ops_available:int):
        if len(choices) != 1:
            return False 
        realign_target_id = choices[0]
        curr_defcon = gamestate.defcon_level 
        if gamestate.countries[realign_target_id].can_coup_or_realign(curr_defcon, player):
            return True 
        return False 
    
    def _can_space(self, player:Superpower, gamestate:GameState, available_ops):
        return gamestate.space_race.can_space(available_ops, player)
    
    # legality of headline choice
    def _can_headline(self, player:Superpower, gamestate:GameState, headline_choice:str):
        player_hand = gamestate.usa_hand if player == Superpower.USA else gamestate.ussr_hand
        if headline_choice in player_hand:
            return True 
        return False 
    
    # -- logic for influence addition/removal events -- 
    def _addition_list_legal(self, total_addable:int, gamestate:GameState, country_list:List[str], countries_chosen:List[str], player:Superpower, max_target:int = 2):
        if len(countries_chosen) > total_addable:
            return False 
        addition_counts = Counter(countries_chosen)
        for (cid, count) in addition_counts.most_common():
            if not cid in country_list:
                return False 
            if count > max_target:
                return False 

    def _removal_list_legal(self, total_removal:int, gamestate:GameState, country_list:List[str], countries_chosen:List[str],player:Superpower, max_target:int = 2):
        if len(countries_chosen) > total_removal:
            return False 
        removal_counts = Counter(countries_chosen)
        if removal_counts.most_common(1)[0][1] > max_target:
            return False 
        valid_countries = self._countries_removable(gamestate, country_list, player)
        for (cid, count) in removal_counts.most_common():
            if not valid_countries[cid] or valid_countries[cid]._opp_influence(player)<count:
                return False 
            return True 


    def _countries_removable(self, gamestate:GameState, country_list:List[str], player:Superpower):
        return {key: value for key, value in gamestate.countries.items() if value._has_opp_influence(player) and key in country_list}






        
        
    