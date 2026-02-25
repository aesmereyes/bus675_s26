# Game Design Document

## Theme / Setting
[What's your theme? Fantasy, sci-fi, horror, action movie, etc.?]
A gritty, alternate-history Star Wars: Episode III text adventure. The game starts during the rescue of Chancellor Palpatine and stretches to the fateful events of Order 66 and Mustafar. It is a tense race against a "Galactic Clock" where every move takes time, and your choices determine the fate of the galaxy.

## Player's Goal
[What does the player need to accomplish to win?]
The Goal: To prevent Anakin Skywalker from falling to the Dark Side. At the start of the game, a d4 dice roll selects your character: Obi-Wan Kenobi, Padmé Amidala, Ahsoka Tano, or Mace Windu. Your goal is to navigate the world, survive combat, and build a Trust Score with Anakin or find Evidence of Palpatine's manipulation. Each character has a unique playstyle and different narrative ways to earn Anakin's trust.
## Locations (4-6)
[List your locations and sketch how they connect]
[The Invisible Hand] (Start/Tutorial Room)
          |
       (South)
          |
 [Jedi Council Room] (Debate Anakin's rank)
          |
       (South)
          |
   [Jedi Temple] <====== (East) =====> [Padmé's Apartment] <====== (East) =====> [The Senate Building]
(Order 66 Ambush)                       (Safe Room/Clues)                        (Palpatine's Office)
          |                                     |
       (Ship)                                 (Ship)
          |                                     |
          +-----------------v-------------------+
                            |
                       [Mustafar] 
                 (The Final Confrontation)
```
[Your map here]
```

## Enemies (2-4 types)
[Describe your enemy types and their stats/behaviors]
4 distinct enemies to satisfy the combat requirements:

Count Dooku: An early-game tutorial boss on The Invisible Hand to teach the dice-combat mechanics.

Clone Troopers (501st Legion): Swarm enemies that flood the Jedi Temple once the clock runs down and Order 66 begins.

Emperor Palpatine: A terrifying boss in the Senate Building. You likely can't beat him in a straight fight; you must survive enough turns to escape with his Sith Holocron.

Corrupted Anakin: The Final Boss. You only fight him if you fail the Trust checks at the end.
## Win Condition
[How does the player win?]
The Victory Condition: You must survive until the final encounter on Mustafar and successfully pull Anakin back to the Light Side. You win if:

The Trust Victory: You accumulated enough Trust Points during the game (e.g., as Mace Windu, you granted him the rank of Master; as Obi-Wan, you defended him).

The Evidence Victory: You have at least 1 Trust Point and you successfully stole the Sith Holocron from the Senate Building to prove Palpatine is the villain.

How each character wins: 
Obi-Wan's Win (The Brotherhood): You must accumulate 3 Trust Points (earned by defending Anakin to the Council and fighting by his side) to talk him down on Mustafar purely through your bond as brothers.

Padmé's Win (The Truth): Because you have very low combat stats, your win relies entirely on stealth and investigation. You must sneak into the Senate Building, avoid Palpatine, and find the Evidence (Sith Holocron). Combine this with 1 Trust Point (earned by comforting him about his nightmares) to prove Palpatine is manipulating his visions, causing Anakin to stand down.

Ahsoka's Win (The Rebel Bond): You skip the political Council rooms entirely. To win, you must earn 3 Trust Points by validating Anakin's frustrations with the Jedi Order and fighting alongside him. You win by using your shared disillusionment and your "Snips and Skyguy" dynamic to snap him out of the Dark Side's trance on Mustafar.

Mace Windu's Win (The Ultimate Respect - Hard Mode): You must make the choices Mace didn't make in the movie. To win, you must swallow your pride, grant Anakin the rank of Master (earning massive Trust), and invite him to help you arrest Palpatine, proving the Jedi Council truly respects him.
## Lose Condition
[How does the player lose?]
The Defeat Conditions:

Combat Death: Your HP reaches 0 during any fight (e.g., failing your dice rolls against Dooku or the Clones).

Out of Time: The game tracks an internal "Galactic Clock" (e.g., 24 in-game hours). Moving between rooms or searching areas burns hours. If you run out of time before reaching Mustafar, Anakin falls completely and the Empire is born.

Tragic Ending: You make it to Mustafar, but your Trust Score is too low and you don't have the Evidence. You are forced to fight Anakin to the death, repeating the tragedy of the movie.
## Class Hierarchy
[Sketch your class design]

```
Character (Base class: handles hp, name, is_alive)
├── Player (Inherits from Character: adds trust_score, inventory)
│   ├── ObiWan (Balanced stats, Brotherhood trust abilities)
│   ├── Padme (Low combat, high stealth/persuasion)
│   ├── Ahsoka (High speed/dodge, Rebel trust abilities)
│   └── MaceWindu (High combat, Respect trust abilities)
│
└── Enemy (Inherits from Character: adds damage_output, descriptions)
    ├── CountDooku (Tutorial Boss)
    ├── CloneTrooper (Swarm Enemy)
    ├── Palpatine (Stealth/Survival Boss)
    └── CorruptedAnakin (Final Boss)

Location (Base class)
├── SafeRoom (e.g., Padmé's Apartment - heals or gives clues)
└── CombatRoom (e.g., Jedi Temple, Senate - triggers enemy encounters)
Item (Base class: has a name and description)
├── Weapon (Adds damage_bonus and accuracy)
│   ├── Lightsaber (High damage, equipped by Obi-Wan, Ahsoka, Mace, Dooku, Anakin)
│   ├── Blaster (Ranged damage, equipped by Padmé, Clones)
│   └── ForceLightning (Special weapon equipped by Palpatine)
│
├── Consumable (Adds heal_amount)
│   └── BactaPatch (Restores HP, found in locations)
│
└── KeyItem (Used to progress the story or win)
    └── SithHolocron (The Evidence found in the Senate Building)
Game
```

## Additional Notes
[Any other design decisions, ideas, or plans]
