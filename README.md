## general implementation plan


1. get input string from user (or vectorize action from bot)
2. parse, return if syntax error 
3. check legality (higher level checker.) confirm input type is right (countries if placing influence, card if discarding, etc)
4. resolve action, check for triggers (event triggers, reshuffle etc). possibly change chooser (player actually making action)
5. Check if game over: score >= 20, defcon 1, scoring card held, war games, final scoring (that may be turn management tho)
6. change AR player, turn management 
 
