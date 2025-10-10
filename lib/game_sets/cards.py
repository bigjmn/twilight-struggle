"""Card definitions and effects for Twilight Struggle."""

from enum import Enum
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass


class CardType(Enum):
    EVENT = "event"
    SCORING = "scoring"

class Side(Enum):
    USA = "usa"
    USSR = "ussr"
    NEUTRAL = "neutral"


@dataclass
class Card:
    name: str
    ops: int
    side: Side
    card_type: CardType
    early_war: bool = False
    mid_war: bool = False
    late_war: bool = False
    removed_after_event: bool = False
    prerequisite: Optional[str] = None
    effect_description: str = ""
    
    @property
    def era(self) -> str:
        """Return the era this card belongs to."""
        if self.early_war:
            return "Early War"
        elif self.mid_war:
            return "Mid War"
        elif self.late_war:
            return "Late War"
        return "Unknown"


CARDS: Dict[str, Card] = {
    # Early War Cards (1-35)
    "Asia Scoring": Card("Asia Scoring", 0, Side.NEUTRAL, CardType.SCORING, early_war=True),
    "Europe Scoring": Card("Europe Scoring", 0, Side.NEUTRAL, CardType.SCORING, early_war=True),
    "Middle East Scoring": Card("Middle East Scoring", 0, Side.NEUTRAL, CardType.SCORING, early_war=True),
    "Duck and Cover": Card("Duck and Cover", 3, Side.USA, CardType.EVENT, early_war=True, 
                          effect_description="Degrade DEFCON level by 1. US gains VP equal to 5 minus current DEFCON level."),
    "Five Year Plan": Card("Five Year Plan", 3, Side.USA, CardType.EVENT, early_war=True,
                          effect_description="USSR must randomly discard a card. If it is a USSR card, gain 1 VP."),
    "The China Card": Card("The China Card", 4, Side.NEUTRAL, CardType.EVENT, early_war=True,
                          effect_description="This card is passed to the other player after use. When played, gain +1 influence in all countries adjacent to China."),
    "Socialist Governments": Card("Socialist Governments", 3, Side.USSR, CardType.EVENT, early_war=True,
                                 effect_description="Remove 3 US influence from Western Europe (user's choice)."),
    "Fidel": Card("Fidel", 2, Side.USSR, CardType.EVENT, early_war=True, removed_after_event=True,
                 effect_description="Remove all US influence from Cuba. USSR gains 1 influence in Cuba."),
    "Vietnam Revolts": Card("Vietnam Revolts", 2, Side.USSR, CardType.EVENT, early_war=True,
                          effect_description="Add 2 USSR influence to Vietnam. If the US is in Vietnam, they lose 1 influence."),
    "Blockade": Card("Blockade", 1, Side.USSR, CardType.EVENT, early_war=True,
                    prerequisite="USSR controls East Germany", removed_after_event=True,
                    effect_description="Remove all US influence from West Germany unless US plays D-Day."),
    "Korean War": Card("Korean War", 2, Side.USSR, CardType.EVENT, early_war=True,
                      effect_description="North Korea invades South Korea. Roll dice to determine outcome."),
    "Romanian Abdication": Card("Romanian Abdication", 1, Side.USSR, CardType.EVENT, early_war=True, removed_after_event=True,
                              effect_description="Remove all US influence from Romania. USSR gains 1 influence in Romania."),
    "Arab-Israeli War": Card("Arab-Israeli War", 2, Side.USSR, CardType.EVENT, early_war=True,
                           effect_description="Pan-Arab Coalition invades Israel. Roll dice to determine outcome."),
    "Comecon": Card("Comecon", 3, Side.USSR, CardType.EVENT, early_war=True,
                   effect_description="Add 1 USSR influence to each of 4 non-US controlled countries in Eastern Europe."),
    "Nasser": Card("Nasser", 1, Side.USSR, CardType.EVENT, early_war=True,
                  effect_description="Add 2 USSR influence to Egypt. Remove half of US influence (rounded up) from Egypt."),
    "Warsaw Pact Formed": Card("Warsaw Pact Formed", 3, Side.USSR, CardType.EVENT, early_war=True, removed_after_event=True,
                             effect_description="Remove all US influence from 4 countries in Eastern Europe OR add 5 USSR influence to Eastern Europe."),
    "De Gaulle Leads France": Card("De Gaulle Leads France", 3, Side.USSR, CardType.EVENT, early_war=True, removed_after_event=True,
                                 effect_description="Remove 2 US influence from France. Add 1 USSR influence to France."),
    "Captured Nazi Scientist": Card("Captured Nazi Scientist", 1, Side.NEUTRAL, CardType.EVENT, early_war=True,
                                   effect_description="Move the Space Race marker one box in your favor."),
    "Truman Doctrine": Card("Truman Doctrine", 1, Side.USA, CardType.EVENT, early_war=True, removed_after_event=True,
                           effect_description="Remove all USSR influence from one uncontrolled country in Europe."),
    "Olympic Games": Card("Olympic Games", 2, Side.NEUTRAL, CardType.EVENT, early_war=True,
                         effect_description="Sponsor may add 2 influence to any countries. Opponent must either boycott or participate."),
    "NATO": Card("NATO", 4, Side.USA, CardType.EVENT, early_war=True, removed_after_event=True,
                effect_description="USSR cannot coup or attempt realignment against any NATO country."),
    "Independent Reds": Card("Independent Reds", 2, Side.USA, CardType.EVENT, early_war=True,
                           effect_description="Add 1 US influence to either Yugoslavia, Romania, Bulgaria, Hungary, or Czechoslovakia."),
    "Marshall Plan": Card("Marshall Plan", 4, Side.USA, CardType.EVENT, early_war=True, removed_after_event=True,
                         effect_description="Add 1 US influence to each of 7 non-USSR controlled countries in Western Europe."),
    "Indo-Pakistani War": Card("Indo-Pakistani War", 2, Side.NEUTRAL, CardType.EVENT, early_war=True,
                             effect_description="India invades Pakistan or vice versa. Roll dice to determine outcome."),
    "Containment": Card("Containment", 3, Side.USA, CardType.EVENT, early_war=True,
                       effect_description="All US operations in the remainder of this turn are +1 to their operations value."),
    "CIA Created": Card("CIA Created", 1, Side.USA, CardType.EVENT, early_war=True,
                       effect_description="USSR reveals their hand of cards. US may use the event of one USSR card."),
    "US/Japan Mutual Defense Pact": Card("US/Japan Mutual Defense Pact", 4, Side.USA, CardType.EVENT, early_war=True, removed_after_event=True,
                                        effect_description="US gains 1 influence in Japan. USSR cannot coup or attempt realignment against Japan."),
    "Suez Crisis": Card("Suez Crisis", 3, Side.USSR, CardType.EVENT, early_war=True,
                       effect_description="Remove 4 US influence from France and UK (user's choice)."),
    "East European Unrest": Card("East European Unrest", 3, Side.USA, CardType.EVENT, early_war=True,
                                effect_description="Early or Mid War: Remove 1 USSR influence from 3 countries in Eastern Europe."),
    "Decolonization": Card("Decolonization", 2, Side.USSR, CardType.EVENT, early_war=True,
                          effect_description="Add 1 USSR influence to any 4 countries in Africa and/or Southeast Asia."),
    "Red Scare/Purge": Card("Red Scare/Purge", 4, Side.NEUTRAL, CardType.EVENT, early_war=True,
                           effect_description="All opponent's operations in the remainder of this turn are -1 to their operations value."),
    "UN Intervention": Card("UN Intervention", 1, Side.NEUTRAL, CardType.EVENT, early_war=True,
                           effect_description="Play this card along with a card containing an invasion or war. The phasing player's die roll receives -1."),
    "De-Stalinization": Card("De-Stalinization", 3, Side.USSR, CardType.EVENT, early_war=True, removed_after_event=True,
                            effect_description="USSR may realign against any 4 countries. No dice roll required."),
    "Nuclear Test Ban": Card("Nuclear Test Ban", 4, Side.NEUTRAL, CardType.EVENT, early_war=True,
                            effect_description="Improve DEFCON by 2. Gain 2 VP. Opponent must discard a card with 2+ Ops."),
    "Formosan Resolution": Card("Formosan Resolution", 2, Side.USA, CardType.EVENT, early_war=True, removed_after_event=True,
                              effect_description="If the US controls Taiwan, USSR cannot coup or attempt realignment against Taiwan."),
    
    # Mid War Cards (36-70)
    "Brush War": Card("Brush War", 3, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                     effect_description="Attack any country with a stability number of 1 or 2. Roll dice to determine outcome."),
    "Central America Scoring": Card("Central America Scoring", 0, Side.NEUTRAL, CardType.SCORING, mid_war=True),
    "Southeast Asia Scoring": Card("Southeast Asia Scoring", 0, Side.NEUTRAL, CardType.SCORING, mid_war=True),
    "Arms Race": Card("Arms Race", 3, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                     effect_description="Compare military operations. Player with more wins VP. Loser must discard a card."),
    "Cuban Missile Crisis": Card("Cuban Missile Crisis", 3, Side.NEUTRAL, CardType.EVENT, mid_war=True, removed_after_event=True,
                                effect_description="Set DEFCON to 2. Each player rolls dice. Highest roller wins VP."),
    "Nuclear Subs": Card("Nuclear Subs", 2, Side.USA, CardType.EVENT, mid_war=True,
                        effect_description="US operations may be used to coup or realign in any ocean-adjacent country."),
    "Quagmire": Card("Quagmire", 3, Side.USSR, CardType.EVENT, mid_war=True,
                    effect_description="US is stuck in Quagmire. Must discard a card of 2+ Ops to escape."),
    "SALT Negotiations": Card("SALT Negotiations", 3, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                             effect_description="Improve DEFCON by 2. Each player gains 2 VP. Nuclear War cards are removed."),
    "Bear Trap": Card("Bear Trap", 3, Side.USA, CardType.EVENT, mid_war=True,
                     effect_description="USSR is stuck in Bear Trap. Must discard a card of 2+ Ops to escape."),
    "Summit": Card("Summit", 1, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                  effect_description="Both players roll dice. Higher roller may realign in any 2 countries."),
    "How I Learned to Stop Worrying": Card("How I Learned to Stop Worrying", 2, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                                          effect_description="Set DEFCON to any level. Gain VP equal to 5 minus new DEFCON level."),
    "Junta": Card("Junta", 2, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                 effect_description="Add 2 influence to any 1 country in Central or South America."),
    "Kitchen Debates": Card("Kitchen Debates", 1, Side.USA, CardType.EVENT, mid_war=True,
                           effect_description="If US controls more Battleground countries than USSR, gain 2 VP."),
    "Missile Envy": Card("Missile Envy", 2, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                        effect_description="Exchange this card with a random card from opponent's hand."),
    "We Will Bury You": Card("We Will Bury You", 4, Side.USSR, CardType.EVENT, mid_war=True,
                            effect_description="Degrade DEFCON by 1. USSR gains 3 VP. May be cancelled by UN Intervention."),
    "Brezhnev Doctrine": Card("Brezhnev Doctrine", 3, Side.USSR, CardType.EVENT, mid_war=True,
                             effect_description="All USSR operations to coup or realign in Europe are +1 to their operations value."),
    "Portuguese Empire Crumbles": Card("Portuguese Empire Crumbles", 2, Side.USSR, CardType.EVENT, mid_war=True,
                                      effect_description="Add 2 USSR influence to any 2 countries in Africa."),
    "South African Unrest": Card("South African Unrest", 2, Side.USSR, CardType.EVENT, mid_war=True,
                                effect_description="USSR gains 2 influence in South Africa. If DEFCON is at 2, USSR gains 1 VP."),
    "Allende": Card("Allende", 1, Side.USSR, CardType.EVENT, mid_war=True,
                   effect_description="Add 2 USSR influence to Chile."),
    "Willy Brandt": Card("Willy Brandt", 2, Side.USSR, CardType.EVENT, mid_war=True, removed_after_event=True,
                        effect_description="USSR gains 1 VP. USSR gains 1 influence in West Germany."),
    "Muslim Revolution": Card("Muslim Revolution", 4, Side.USSR, CardType.EVENT, mid_war=True,
                             effect_description="Remove all US influence from 2 countries in the Middle East."),
    "ABM Treaty": Card("ABM Treaty", 4, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                      effect_description="Improve DEFCON by 1. Each player gains 1 VP. Nuclear War cards are removed."),
    "Cultural Revolution": Card("Cultural Revolution", 3, Side.USSR, CardType.EVENT, mid_war=True,
                               effect_description="If USSR controls China, gain 1 VP. China Card is given to US."),
    "Flower Power": Card("Flower Power", 4, Side.USSR, CardType.EVENT, mid_war=True,
                        effect_description="USSR gains 2 VP for each War in progress. End all Wars."),
    "U2 Incident": Card("U2 Incident", 3, Side.USSR, CardType.EVENT, mid_war=True,
                       effect_description="USSR gains 1 VP. If Summit is in effect, USSR gains 1 additional VP."),
    "OPEC": Card("OPEC", 3, Side.USSR, CardType.EVENT, mid_war=True,
                effect_description="USSR gains 1 VP for each US-controlled country in the Middle East."),
    "Lone Gunman": Card("Lone Gunman", 1, Side.USSR, CardType.EVENT, mid_war=True,
                       effect_description="USSR reveals US hand. USSR may use the event of one US card."),
    "Colonial Rear Guards": Card("Colonial Rear Guards", 2, Side.USA, CardType.EVENT, mid_war=True,
                                effect_description="Add 1 US influence to any 4 countries in Africa and/or Southeast Asia."),
    "Panama Canal Returned": Card("Panama Canal Returned", 1, Side.USA, CardType.EVENT, mid_war=True,
                                 effect_description="Add 1 US influence to Panama and any 2 countries in Central America."),
    "Camp David Accords": Card("Camp David Accords", 2, Side.USA, CardType.EVENT, mid_war=True,
                              effect_description="US gains 1 VP. US gains 1 influence in Israel, Jordan, and Egypt."),
    "Puppet Governments": Card("Puppet Governments", 2, Side.USA, CardType.EVENT, mid_war=True,
                              effect_description="US may place 3 influence in countries where they have influence."),
    "Grain Sales to Soviets": Card("Grain Sales to Soviets", 2, Side.USA, CardType.EVENT, mid_war=True,
                                  effect_description="Random event from USSR hand is triggered. Gain 2 VP."),
    "John Paul II Elected Pope": Card("John Paul II Elected Pope", 2, Side.USA, CardType.EVENT, mid_war=True,
                                     effect_description="Remove 2 USSR influence from Poland. Add 1 US influence to Poland."),
    "Latin American Death Squads": Card("Latin American Death Squads", 2, Side.NEUTRAL, CardType.EVENT, mid_war=True,
                                       effect_description="Coup any country in Central or South America."),
    "OAS Founded": Card("OAS Founded", 1, Side.USA, CardType.EVENT, mid_war=True,
                       effect_description="Add 2 US influence to any 2 countries in Central or South America."),
    "Nixon Plays the China Card": Card("Nixon Plays the China Card", 2, Side.USA, CardType.EVENT, mid_war=True,
                                      effect_description="If US controls China, gain 2 VP. China Card is given to USSR."),
    "Sadat Expels Soviets": Card("Sadat Expels Soviets", 1, Side.USA, CardType.EVENT, mid_war=True,
                                effect_description="Remove all USSR influence from Egypt. Add 1 US influence to Egypt."),
    
    # Late War Cards (71-110)
    "The Voice of America": Card("The Voice of America", 2, Side.USA, CardType.EVENT, late_war=True,
                                effect_description="Remove 4 USSR influence from any countries without US influence."),
    "Liberation Theology": Card("Liberation Theology", 2, Side.USSR, CardType.EVENT, late_war=True,
                               effect_description="Add 3 USSR influence to any countries in Central America."),
    "Ussuri River Skirmish": Card("Ussuri River Skirmish", 3, Side.USA, CardType.EVENT, late_war=True,
                                 effect_description="If US controls China, gain 4 VP. If USSR controls China, gain 2 VP."),
    "Ask Not What Your Country Can Do For You": Card("Ask Not What Your Country Can Do For You", 3, Side.USA, CardType.EVENT, late_war=True,
                                                     effect_description="US may discard up to their entire hand and redraw."),
    "Alliance for Progress": Card("Alliance for Progress", 3, Side.USA, CardType.EVENT, late_war=True,
                                 effect_description="US gains 1 VP for each US-controlled Battleground country in Central and South America."),
    "Africa Scoring": Card("Africa Scoring", 0, Side.NEUTRAL, CardType.SCORING, late_war=True),
    "One Small Step": Card("One Small Step", 2, Side.NEUTRAL, CardType.EVENT, late_war=True,
                          effect_description="Gain 2 VP if you are behind in the Space Race."),
    "South America Scoring": Card("South America Scoring", 0, Side.NEUTRAL, CardType.SCORING, late_war=True),
    "Che": Card("Che", 3, Side.USSR, CardType.EVENT, late_war=True,
               effect_description="USSR may attempt 3 coup attempts in Central and South America."),
    "Our Man in Tehran": Card("Our Man in Tehran", 2, Side.USA, CardType.EVENT, late_war=True,
                             effect_description="If US controls Iran, gain 2 VP. May coup or realign Iran."),
    "Iranian Hostage Crisis": Card("Iranian Hostage Crisis", 3, Side.USSR, CardType.EVENT, late_war=True,
                                  effect_description="Remove all US influence from Iran. USSR gains 2 VP if it controls Iran."),
    "The Iron Lady": Card("The Iron Lady", 3, Side.USA, CardType.EVENT, late_war=True,
                         effect_description="Add 1 US influence to any 3 countries in Western Europe."),
    "Reagan Bombs Libya": Card("Reagan Bombs Libya", 2, Side.USA, CardType.EVENT, late_war=True,
                              effect_description="US gains 2 VP. Libya becomes ineligible for coup attempts."),
    "Star Wars": Card("Star Wars", 2, Side.USA, CardType.EVENT, late_war=True,
                     effect_description="If US ahead in Space Race, gain 1 VP. USSR discards a card."),
    "North Sea Oil": Card("North Sea Oil", 3, Side.USA, CardType.EVENT, late_war=True,
                         effect_description="US gains 1 VP for each US-controlled country in Western Europe."),
    "The Reformer": Card("The Reformer", 3, Side.USSR, CardType.EVENT, late_war=True,
                        effect_description="Add 4 USSR influence to any European countries."),
    "Marine Barracks Bombing": Card("Marine Barracks Bombing", 2, Side.USSR, CardType.EVENT, late_war=True,
                                   effect_description="Remove all US influence from Lebanon and any 2 countries in the Middle East."),
    "Soviets Shoot Down KAL-007": Card("Soviets Shoot Down KAL-007", 4, Side.USA, CardType.EVENT, late_war=True,
                                       effect_description="US gains 2 VP. USSR loses 1 influence in any 4 countries."),
    "Glasnost": Card("Glasnost", 4, Side.USSR, CardType.EVENT, late_war=True,
                    effect_description="Improve DEFCON by 1. USSR gains 2 VP. USSR may realign against any 4 countries."),
    "Ortega Elected in Nicaragua": Card("Ortega Elected in Nicaragua", 2, Side.USSR, CardType.EVENT, late_war=True,
                                       effect_description="Remove all US influence from Nicaragua. Add 3 USSR influence to Nicaragua."),
    "Terrorism": Card("Terrorism", 2, Side.NEUTRAL, CardType.EVENT, late_war=True,
                     effect_description="Your opponent must randomly discard a card. Gain 1 VP."),
    "Iran Contra Scandal": Card("Iran Contra Scandal", 2, Side.USSR, CardType.EVENT, late_war=True,
                               effect_description="All US operations in Central America are -1 to their operations value."),
    "Chernobyl": Card("Chernobyl", 3, Side.USA, CardType.EVENT, late_war=True,
                     effect_description="USSR must discard their highest value Ops card. No operations may be conducted in Europe."),
    "Latin American Debt Crisis": Card("Latin American Debt Crisis", 2, Side.USSR, CardType.EVENT, late_war=True,
                                      effect_description="USSR gains 1 VP for each USSR-controlled Battleground country in South America."),
    "Tear Down This Wall": Card("Tear Down This Wall", 3, Side.USA, CardType.EVENT, late_war=True,
                               effect_description="Add 3 US influence to any countries in Eastern Europe."),
    "An Evil Empire": Card("An Evil Empire", 3, Side.USA, CardType.EVENT, late_war=True,
                          effect_description="US gains 1 VP. May coup or realign against any 3 countries."),
    "Aldrich Ames Remix": Card("Aldrich Ames Remix", 2, Side.USSR, CardType.EVENT, late_war=True,
                              effect_description="USSR reveals US hand. USSR may use the event of one US card."),
    "Pershing II Deployed": Card("Pershing II Deployed", 3, Side.USSR, CardType.EVENT, late_war=True,
                                effect_description="USSR gains 1 VP. Remove 1 US influence from any 3 countries in Western Europe."),
    "Wargames": Card("Wargames", 4, Side.NEUTRAL, CardType.EVENT, late_war=True,
                    effect_description="Set DEFCON to 1. Gain 6 VP. May be cancelled by a successful Space Race attempt."),
    "Solidarity": Card("Solidarity", 2, Side.USA, CardType.EVENT, late_war=True,
                      effect_description="Add 3 US influence to Poland. Remove 1 USSR influence from Poland."),
    "Iran-Iraq War": Card("Iran-Iraq War", 2, Side.NEUTRAL, CardType.EVENT, late_war=True,
                         effect_description="Iran invades Iraq or vice versa. Roll dice to determine outcome."),
    "Yuri and Samantha": Card("Yuri and Samantha", 2, Side.USSR, CardType.EVENT, late_war=True,
                             effect_description="USSR gains 1 VP. Improve DEFCON by 1."),
    "AWACS Sale to Saudis": Card("AWACS Sale to Saudis", 3, Side.USA, CardType.EVENT, late_war=True,
                                effect_description="Add 2 US influence to Saudi Arabia. US gains 1 VP."),
}


def get_cards_by_era(early_war: bool = False, mid_war: bool = False, late_war: bool = False) -> List[Card]:
    """Get cards by era."""
    cards = []
    for card in CARDS.values():
        if (early_war and card.early_war) or (mid_war and card.mid_war) or (late_war and card.late_war):
            cards.append(card)
    return cards


def get_scoring_cards() -> List[Card]:
    """Get all scoring cards."""
    return [card for card in CARDS.values() if card.card_type == CardType.SCORING]


def get_event_cards() -> List[Card]:
    """Get all event cards."""
    return [card for card in CARDS.values() if card.card_type == CardType.EVENT]


def get_cards_by_side(side: Side) -> List[Card]:
    """Get cards by side."""
    return [card for card in CARDS.values() if card.side == side]