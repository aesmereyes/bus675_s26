# Star Wars : What If

## Story
The galaxy teeters on the edge of catastrophe. It's Episode III, and Palpatine's web of manipulation is tightening around Anakin Skywalker. The Jedi Council is blind. The Senate has fallen.
You have 24 hours to travel across Coruscant — from the smoking corridors of the Invisible Hand to the lava fields of Mustafar — and stop Anakin from becoming Darth Vader forever. Trust must be earned. Evidence must be gathered. Choose your words carefully, and your battles wisely.

## How to Play
Run the game and play in the terminal using the commands provided. 
### Running the Game
```bash
python game.py
```

### Commands
Command                      Description 
go [direction]               Move between locations: north, south, east, west, or ship
look                         Describe your current locationsearchSearch the room for hidden items (costs 2 hours)
talk                         Engage in dialogue that may earn Trust Points
attack                       Fight the enemy in the current room
equip [weapon]               Equip a weapon from your inventory (e.g., equip lightsaber)
use [item]                   Use a consumable item (e.g., use bacta patch)
inventory or i               Show all items you're carrying
status                       Display your HP, Trust Score, and equipped weapon
help                         Show the full command list
quit                         Exit the game
During combat, your available actions are: attack, run, or use [item]

## Goal
Reach Mustafar before your 24-hour clock runs out and convince Anakin Skywalker not to fall to the Dark Side. Your character is chosen randomly at the start of each game (via a d4 roll), and each has a different win condition:

Obi-Wan Kenobi — Earn 3 Trust Points by defending Anakin like a brother across dialogue choices.
Padmé Amidala — Earn 1 Trust Point AND find the Sith Holocron to expose Palpatine's manipulation.
Ahsoka Tano — Earn 3 Trust Points by validating Anakin's frustrations with the Jedi Order.
Mace Windu (Hard Mode) — Earn 3 Trust Points through three selfless choices, starting with granting Anakin the rank of Jedi Master.

If you arrive at Mustafar without enough Trust (and the Holocron, if playing as Padmé), you'll face Corrupted Anakin as a final boss. Win the fight for a tragic pyrrhic victory, or lose and watch the Empire rise.

## Tips
  - Talk everywhere you can. Dialogue choices at the Jedi Council Room, Jedi Temple, and Padmé's Apartment all have opportunities to earn
  - Trust Points — but only the right answers count.
- Search the Senate Building if you're playing as Padmé. That's where the Sith Holocron is hidden. Don't skip it!
- Watch the clock. Moving costs 1 hour; searching costs 2. With only 24 hours, plan your route — you can't visit every room twice.
- You can't kill Palpatine — fighting him in the Senate is a survival battle. Hold out for 3 turns and you'll escape.
- Ahsoka attacks twice per turn, making her the strongest combatant. If you roll her, don't be afraid to fight.
- Bacta Patches restore 20 HP. Save them for tough fights like Count Dooku or the final boss.
- Running from combat has a 50/50 chance of success — sometimes it's worth the gamble if you're low on health.
