from enum import Enum

class GamePhase(Enum):
    SETUP="setup"
    HEADLINE = "headline"
    ACTION_ROUNDS = "action_rounds"
    CLEANUP="cleanup"
    MILITARY_OPS_CHECK = "military_ops_check"
    SCORING = "scoring"
    GAME_OVER = "game_over"

class Superpower(Enum):
    USA="usa"
    USSR="ussr"