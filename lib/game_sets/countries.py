"""Country definitions and board representation for Twilight Struggle."""

from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from .constants import Superpower
from collections import namedtuple
class Region(Enum):
    EUROPE = "Europe"
    ASIA = "Asia"
    MIDDLE_EAST = "Middle East"
    AFRICA = "Africa"
    CENTRAL_AMERICA = "Central America"
    SOUTH_AMERICA = "South America"





@dataclass
class Country:
    name: str
    region: Region
    stability: int
    battleground: bool = False
    adjacent_countries: List[str] = []
    us_influence: int = 0
    ussr_influence: int = 0
    
    def __post_init__(self):
        if self.adjacent_countries is None:
            self.adjacent_countries = []

    
    def _change_influence(self, usa_change:int, ussr_change:int):
        self.us_influence += usa_change 
        self.ussr_influence += ussr_change 

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the country to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "region": self.region.value,
            "stability": self.stability,
            "battleground": self.battleground,
            "adjacent_countries": list(self.adjacent_countries),
            "us_influence": self.us_influence,
            "ussr_influence": self.ussr_influence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Country":
        """Rehydrate a country instance from serialized data."""
        return cls(
            name=data["name"],
            region=Region(data["region"]),
            stability=data["stability"],
            battleground=data.get("battleground", False),
            adjacent_countries=list(data.get("adjacent_countries", [])),
            us_influence=data.get("us_influence", 0),
            ussr_influence=data.get("ussr_influence", 0),
        )

    @property
    def controlled_by(self) -> Optional[Superpower]:
        """Determine which superpower controls this country."""
        if self.us_influence == 0 and self.ussr_influence == 0:
            return None
        
        required_influence = self.stability + max(self.us_influence, self.ussr_influence)
        
        if self.us_influence >= required_influence and self.us_influence > self.ussr_influence:
            return Superpower.USA
        elif self.ussr_influence >= required_influence and self.ussr_influence > self.us_influence:
            return Superpower.USSR
        
        return None
    
    @property 
    def has_us_influence(self):
        return self.us_influence > 0 
    @property 
    def has_ussr_influence(self):
        return self.ussr_influence > 0

    
    @property
    def us_control(self) -> bool:
        return self.controlled_by == Superpower.USA
    
    @property
    def ussr_control(self) -> bool:
        return self.controlled_by == Superpower.USSR
    
    # this wil also have to check special conditions 
    def can_coup_or_realign(self, defcon_level, player:Superpower):
        if not self._has_opp_influence(player):
            return False 
        if self._region_restricted(defcon_level):
            return False 
        return True 

    # for using ops, not event triggered
    def _has_access(self, player:Superpower):
        if self._has_influence(player):
            return True 
        for a in self.adjacent_countries:
            adj_country = COUNTRIES[a]
            if adj_country._has_influence(player):
                return True 
        return False 
    # get influence cost 
    def influence_cost(self, player:Superpower):
        opp_controlled = self.us_control if player == Superpower.USSR else self.ussr_control 
        return 2 if opp_controlled else 1 

    
    def _has_influence(self, player:Superpower):
        return self.has_us_influence if player == Superpower.USA else self.has_ussr_influence 

    def _has_opp_influence(self, player:Superpower):
        return self._opp_influence(player) > 0
    
    def _opp_influence(self, player:Superpower):
        return self.us_influence if player == Superpower.USSR else self.ussr_influence
    def _region_restricted(self, defcon_level):
        if defcon_level < 5 and self.region == Region.EUROPE: return True 
        if defcon_level < 4 and self.region == Region.ASIA: return True 
        if defcon_level < 3 and self.region == Region.MIDDLE_EAST: return True 
        return False  


COUNTRIES: Dict[str, Country] = {
    # Europe
    "Canada": Country("Canada", Region.EUROPE, 4, battleground=True, adjacent_countries=["USA"]),
    "UK": Country("UK", Region.EUROPE, 5, battleground=True, adjacent_countries=["Norway", "Benelux", "France"]),
    "Norway": Country("Norway", Region.EUROPE, 4, adjacent_countries=["UK", "Sweden", "Finland"]),
    "Sweden": Country("Sweden", Region.EUROPE, 4, adjacent_countries=["Norway", "Finland", "Denmark"]),
    "Finland": Country("Finland", Region.EUROPE, 4, adjacent_countries=["Norway", "Sweden", "USSR"]),
    "Denmark": Country("Denmark", Region.EUROPE, 3, adjacent_countries=["Sweden", "West Germany", "Benelux"]),
    "Benelux": Country("Benelux", Region.EUROPE, 3, adjacent_countries=["UK", "Denmark", "West Germany", "France"]),
    "France": Country("France", Region.EUROPE, 3, battleground=True, adjacent_countries=["UK", "Benelux", "West Germany", "Spain/Portugal", "Italy", "Algeria"]),
    "Spain/Portugal": Country("Spain/Portugal", Region.EUROPE, 2, adjacent_countries=["France", "Italy", "Morocco"]),
    "Italy": Country("Italy", Region.EUROPE, 2, battleground=True, adjacent_countries=["France", "Spain/Portugal", "West Germany", "Austria", "Yugoslavia", "Greece"]),
    "West Germany": Country("West Germany", Region.EUROPE, 4, battleground=True, adjacent_countries=["Benelux", "Denmark", "France", "Italy", "Austria", "East Germany"]),
    "East Germany": Country("East Germany", Region.EUROPE, 3, battleground=True, adjacent_countries=["West Germany", "Austria", "Czechoslovakia", "Poland"]),
    "Austria": Country("Austria", Region.EUROPE, 4, adjacent_countries=["Italy", "West Germany", "East Germany", "Czechoslovakia", "Hungary"]),
    "Czechoslovakia": Country("Czechoslovakia", Region.EUROPE, 3, adjacent_countries=["East Germany", "Austria", "Hungary", "Poland"]),
    "Hungary": Country("Hungary", Region.EUROPE, 3, adjacent_countries=["Austria", "Czechoslovakia", "Romania", "Yugoslavia"]),
    "Poland": Country("Poland", Region.EUROPE, 3, battleground=True, adjacent_countries=["East Germany", "Czechoslovakia", "USSR"]),
    "Yugoslavia": Country("Yugoslavia", Region.EUROPE, 3, adjacent_countries=["Italy", "Hungary", "Romania", "Bulgaria", "Greece"]),
    "Romania": Country("Romania", Region.EUROPE, 3, adjacent_countries=["Hungary", "Yugoslavia", "Bulgaria", "Turkey", "USSR"]),
    "Bulgaria": Country("Bulgaria", Region.EUROPE, 3, adjacent_countries=["Yugoslavia", "Romania", "Greece", "Turkey"]),
    "Greece": Country("Greece", Region.EUROPE, 2, adjacent_countries=["Italy", "Yugoslavia", "Bulgaria", "Turkey"]),
    "Turkey": Country("Turkey", Region.EUROPE, 2, battleground=True, adjacent_countries=["Bulgaria", "Greece", "Romania", "Syria", "Lebanon", "Israel"]),
    
    # Asia  
    "USSR": Country("USSR", Region.ASIA, 6, battleground=True, adjacent_countries=["Finland", "Poland", "Romania", "Afghanistan", "China", "Mongolia", "North Korea"]),
    "China": Country("China", Region.ASIA, 5, battleground=True, adjacent_countries=["USSR", "Mongolia", "North Korea", "South Korea", "Japan", "Laos/Cambodia", "Vietnam", "Myanmar", "India", "Pakistan", "Afghanistan"]),
    "Mongolia": Country("Mongolia", Region.ASIA, 4, adjacent_countries=["USSR", "China"]),
    "North Korea": Country("North Korea", Region.ASIA, 3, battleground=True, adjacent_countries=["USSR", "China", "South Korea"]),
    "South Korea": Country("South Korea", Region.ASIA, 3, battleground=True, adjacent_countries=["China", "North Korea", "Japan"]),
    "Japan": Country("Japan", Region.ASIA, 4, battleground=True, adjacent_countries=["China", "South Korea", "Philippines", "Taiwan"]),
    "Taiwan": Country("Taiwan", Region.ASIA, 3, adjacent_countries=["Japan", "Philippines", "South Korea"]),
    "Philippines": Country("Philippines", Region.ASIA, 2, adjacent_countries=["Japan", "Taiwan", "Malaysia", "Indonesia", "Australia"]),
    "Australia": Country("Australia", Region.ASIA, 4, adjacent_countries=["Philippines", "Indonesia"]),
    "Indonesia": Country("Indonesia", Region.ASIA, 1, adjacent_countries=["Philippines", "Australia", "Malaysia"]),
    "Malaysia": Country("Malaysia", Region.ASIA, 2, adjacent_countries=["Philippines", "Indonesia", "Thailand"]),
    "Thailand": Country("Thailand", Region.ASIA, 2, battleground=True, adjacent_countries=["Malaysia", "Myanmar", "Laos/Cambodia", "Vietnam"]),
    "Laos/Cambodia": Country("Laos/Cambodia", Region.ASIA, 1, adjacent_countries=["China", "Thailand", "Vietnam"]),
    "Vietnam": Country("Vietnam", Region.ASIA, 1, adjacent_countries=["China", "Thailand", "Laos/Cambodia"]),
    "Myanmar": Country("Myanmar", Region.ASIA, 2, adjacent_countries=["China", "Thailand", "India", "Bangladesh"]),
    "India": Country("India", Region.ASIA, 3, battleground=True, adjacent_countries=["China", "Myanmar", "Bangladesh", "Pakistan"]),
    "Bangladesh": Country("Bangladesh", Region.ASIA, 2, adjacent_countries=["Myanmar", "India"]),
    "Pakistan": Country("Pakistan", Region.ASIA, 2, battleground=True, adjacent_countries=["China", "India", "Afghanistan", "Iran"]),
    "Afghanistan": Country("Afghanistan", Region.ASIA, 2, adjacent_countries=["USSR", "China", "Pakistan", "Iran"]),
    
    # Middle East
    "Iran": Country("Iran", Region.MIDDLE_EAST, 2, battleground=True, adjacent_countries=["Pakistan", "Afghanistan", "Iraq", "Gulf States", "Saudi Arabia"]),
    "Iraq": Country("Iraq", Region.MIDDLE_EAST, 3, battleground=True, adjacent_countries=["Iran", "Gulf States", "Saudi Arabia", "Jordan", "Syria", "Turkey"]),
    "Gulf States": Country("Gulf States", Region.MIDDLE_EAST, 3, adjacent_countries=["Iran", "Iraq", "Saudi Arabia"]),
    "Saudi Arabia": Country("Saudi Arabia", Region.MIDDLE_EAST, 3, battleground=True, adjacent_countries=["Iran", "Iraq", "Gulf States", "Jordan", "Egypt"]),
    "Jordan": Country("Jordan", Region.MIDDLE_EAST, 2, adjacent_countries=["Iraq", "Saudi Arabia", "Israel", "Syria", "Lebanon"]),
    "Syria": Country("Syria", Region.MIDDLE_EAST, 2, adjacent_countries=["Turkey", "Iraq", "Jordan", "Lebanon", "Israel"]),
    "Lebanon": Country("Lebanon", Region.MIDDLE_EAST, 1, adjacent_countries=["Turkey", "Jordan", "Syria", "Israel"]),
    "Israel": Country("Israel", Region.MIDDLE_EAST, 4, battleground=True, adjacent_countries=["Turkey", "Jordan", "Syria", "Lebanon", "Egypt"]),
    "Egypt": Country("Egypt", Region.MIDDLE_EAST, 2, battleground=True, adjacent_countries=["Saudi Arabia", "Israel", "Sudan", "Libya"]),
    "Libya": Country("Libya", Region.MIDDLE_EAST, 2, adjacent_countries=["Egypt", "Sudan", "Chad", "Tunisia", "Algeria"]),
    
    # Africa
    "Morocco": Country("Morocco", Region.AFRICA, 3, adjacent_countries=["Spain/Portugal", "Algeria", "West African States"]),
    "Algeria": Country("Algeria", Region.AFRICA, 2, battleground=True, adjacent_countries=["France", "Morocco", "Tunisia", "Libya", "West African States", "Saharan States"]),
    "Tunisia": Country("Tunisia", Region.AFRICA, 2, adjacent_countries=["Algeria", "Libya"]),
    "West African States": Country("West African States", Region.AFRICA, 2, adjacent_countries=["Morocco", "Algeria", "Saharan States", "Ivory Coast"]),
    "Saharan States": Country("Saharan States", Region.AFRICA, 1, adjacent_countries=["Algeria", "Libya", "West African States", "Nigeria", "Chad"]),
    "Ivory Coast": Country("Ivory Coast", Region.AFRICA, 2, adjacent_countries=["West African States", "Nigeria"]),
    "Nigeria": Country("Nigeria", Region.AFRICA, 1, battleground=True, adjacent_countries=["Saharan States", "Ivory Coast", "Cameroon"]),
    "Cameroon": Country("Cameroon", Region.AFRICA, 1, adjacent_countries=["Nigeria", "Chad", "Zaire"]),
    "Chad": Country("Chad", Region.AFRICA, 1, adjacent_countries=["Libya", "Saharan States", "Nigeria", "Cameroon", "Sudan"]),
    "Sudan": Country("Sudan", Region.AFRICA, 1, adjacent_countries=["Egypt", "Libya", "Chad", "Ethiopia", "Somalia", "Kenya"]),
    "Ethiopia": Country("Ethiopia", Region.AFRICA, 1, adjacent_countries=["Sudan", "Somalia", "Kenya"]),
    "Somalia": Country("Somalia", Region.AFRICA, 2, adjacent_countries=["Sudan", "Ethiopia", "Kenya"]),
    "Kenya": Country("Kenya", Region.AFRICA, 2, adjacent_countries=["Sudan", "Ethiopia", "Somalia", "Southeast African States"]),
    "Zaire": Country("Zaire", Region.AFRICA, 1, battleground=True, adjacent_countries=["Cameroon", "Angola", "Zimbabwe", "Southeast African States"]),
    "Angola": Country("Angola", Region.AFRICA, 1, battleground=True, adjacent_countries=["Zaire", "Zimbabwe", "South Africa", "Botswana"]),
    "Zimbabwe": Country("Zimbabwe", Region.AFRICA, 1, adjacent_countries=["Zaire", "Angola", "Botswana", "South Africa", "Southeast African States"]),
    "Botswana": Country("Botswana", Region.AFRICA, 2, adjacent_countries=["Angola", "Zimbabwe", "South Africa"]),
    "South Africa": Country("South Africa", Region.AFRICA, 3, battleground=True, adjacent_countries=["Angola", "Zimbabwe", "Botswana"]),
    "Southeast African States": Country("Southeast African States", Region.AFRICA, 1, adjacent_countries=["Kenya", "Zaire", "Zimbabwe"]),
    
    # Central America
    "USA": Country("USA", Region.CENTRAL_AMERICA, 6, battleground=True, adjacent_countries=["Canada", "Mexico", "Cuba"]),
    "Mexico": Country("Mexico", Region.CENTRAL_AMERICA, 2, battleground=True, adjacent_countries=["USA", "Guatemala"]),
    "Guatemala": Country("Guatemala", Region.CENTRAL_AMERICA, 1, adjacent_countries=["Mexico", "El Salvador", "Honduras", "Nicaragua"]),
    "El Salvador": Country("El Salvador", Region.CENTRAL_AMERICA, 1, adjacent_countries=["Guatemala", "Honduras"]),
    "Honduras": Country("Honduras", Region.CENTRAL_AMERICA, 2, adjacent_countries=["Guatemala", "El Salvador", "Nicaragua", "Costa Rica"]),
    "Nicaragua": Country("Nicaragua", Region.CENTRAL_AMERICA, 1, adjacent_countries=["Guatemala", "Honduras", "Costa Rica"]),
    "Costa Rica": Country("Costa Rica", Region.CENTRAL_AMERICA, 3, adjacent_countries=["Honduras", "Nicaragua", "Panama"]), 
    "Panama": Country("Panama", Region.CENTRAL_AMERICA, 2, battleground=True, adjacent_countries=["Costa Rica", "Colombia"]),
    "Cuba": Country("Cuba", Region.CENTRAL_AMERICA, 3, battleground=True, adjacent_countries=["USA", "Haiti", "Dominican Republic"]),
    "Haiti": Country("Haiti", Region.CENTRAL_AMERICA, 1, adjacent_countries=["Cuba", "Dominican Republic"]),
    "Dominican Republic": Country("Dominican Republic", Region.CENTRAL_AMERICA, 1, adjacent_countries=["Cuba", "Haiti"]),
    
    # South America
    "Colombia": Country("Colombia", Region.SOUTH_AMERICA, 1, adjacent_countries=["Panama", "Venezuela", "Ecuador"]),
    "Venezuela": Country("Venezuela", Region.SOUTH_AMERICA, 2, battleground=True, adjacent_countries=["Colombia", "Brazil", "Ecuador"]),
    "Ecuador": Country("Ecuador", Region.SOUTH_AMERICA, 2, adjacent_countries=["Colombia", "Venezuela", "Peru"]),
    "Peru": Country("Peru", Region.SOUTH_AMERICA, 2, adjacent_countries=["Ecuador", "Bolivia", "Brazil"]),
    "Bolivia": Country("Bolivia", Region.SOUTH_AMERICA, 2, adjacent_countries=["Peru", "Paraguay", "Chile", "Argentina", "Brazil"]),
    "Paraguay": Country("Paraguay", Region.SOUTH_AMERICA, 2, adjacent_countries=["Bolivia", "Brazil", "Argentina", "Uruguay"]),
    "Uruguay": Country("Uruguay", Region.SOUTH_AMERICA, 2, adjacent_countries=["Paraguay", "Brazil", "Argentina"]),
    "Brazil": Country("Brazil", Region.SOUTH_AMERICA, 2, battleground=True, adjacent_countries=["Venezuela", "Peru", "Bolivia", "Paraguay", "Uruguay", "Argentina"]),
    "Argentina": Country("Argentina", Region.SOUTH_AMERICA, 2, battleground=True, adjacent_countries=["Bolivia", "Paraguay", "Uruguay", "Brazil", "Chile"]),
    "Chile": Country("Chile", Region.SOUTH_AMERICA, 3, battleground=True, adjacent_countries=["Bolivia", "Argentina"]),
}


def get_countries_by_region(region: Region) -> List[Country]:
    """Get all countries in a specific region."""
    return [country for country in COUNTRIES.values() if country.region == region]


def get_battleground_countries() -> List[Country]:
    """Get all battleground countries."""
    return [country for country in COUNTRIES.values() if country.battleground]


def get_controlled_countries(superpower: Superpower) -> List[Country]:
    """Get all countries controlled by a superpower."""
    return [country for country in COUNTRIES.values() if country.controlled_by == superpower]


def calculate_region_control(region: Region) -> Dict[str, int]:
    """Calculate regional control scoring for a region."""
    countries = get_countries_by_region(region)
    battlegrounds = [c for c in countries if c.battleground]
    
    us_controlled = sum(1 for c in countries if c.us_control)
    ussr_controlled = sum(1 for c in countries if c.ussr_control)
    us_battlegrounds = sum(1 for c in battlegrounds if c.us_control)
    ussr_battlegrounds = sum(1 for c in battlegrounds if c.ussr_control)
    
    return {
        "us_countries": us_controlled,
        "ussr_countries": ussr_controlled,
        "us_battlegrounds": us_battlegrounds,
        "ussr_battlegrounds": ussr_battlegrounds,
        "total_countries": len(countries),
        "total_battlegrounds": len(battlegrounds)
    }

# utility for influence change 
InfluenceChange = namedtuple("InfluenceChange", ["country_name", "usa_change", "ussr_change"])
