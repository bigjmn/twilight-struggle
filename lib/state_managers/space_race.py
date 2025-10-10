from ..game_sets.constants import Superpower
from ..game_sets.cards import Card 


space_squares = [
    {
        "ops_required":2,
        "vps_gained": [2,0]
    },
    {
        "ops_required":2,
        "vps_gained": [0,0]
    },
    {
        "ops_required":2,
        "vps_gained": [3,1]
    },
    {
        "ops_required":2,
        "vps_gained": [0,0]
    },
    {
        "ops_required":3,
        "vps_gained": [3,1]
    },
    {
        "ops_required":2,
        "vps_gained": [3,1]
    }
]
class SpaceRace:
    def __init__(self):
        self.usa_token: int = 0 
        self.ussr_token: int = 0 

        # spaces taken by each side this turn 
        self.usa_missions: int = 0 
        self.ussr_missions: int = 0 

    @property 
    def usa_max(self):
        if self.usa_token >=2 and self.ussr_token < 2:
            return 2 
        return 1 
    @property
    def ussr_max(self):
        if self.ussr_token >= 2 and self.usa_token < 2:
            return 2 
        return 1 
    
    
    def can_space(self, card_ops:int, player:Superpower):
        if player == Superpower.USA:
            if self.usa_max >= self.usa_missions: return False
        if player == Superpower.USSR:
            if self.ussr_max >= self.ussr_missions: return False 
        mission_idx = self._get_spacesquare(player) + 1 
        if mission_idx >= len(space_squares):
            return False 
        return space_squares[mission_idx]["ops_required"] >= card_ops 
         

    def _get_spacesquare(self, player:Superpower):
        return self.usa_token if player == Superpower.USA else self.ussr_token 

    @property 
    def usa_ahead(self):
        return self.usa_token > self.ussr_token 
    @property 
    def ussr_ahead(self):
        return self.ussr_token > self.usa_token 
    def player_ahead(self, player:Superpower):
        return self.usa_ahead if player == Superpower.USA else self.ussr_ahead
    