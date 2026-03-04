"""
Lab 1: Text-Based Adventure RPG
================================
Abigail Reyes

Star Wars "What If" Text Adventure
Set during Episode III - Prevent Anakin from falling to the Dark Side.

Run with: python game.py
"""

import random

# =============================================================================
# Dice Utilities
# =============================================================================

def roll_d20():
    """Roll a 20-sided die."""
    return random.randint(1, 20)

def roll_d4():
    """Roll a 4-sided die."""
    return random.randint(1, 4)

def roll_dice(num_dice, sides):
    """Roll multiple dice and return the total."""
    return sum(random.randint(1, sides) for _ in range(num_dice))


# =============================================================================
# Item Classes
# =============================================================================

class Item:
    """Base class for all items."""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


class Weapon(Item):
    """A weapon item that can be equipped."""
    def __init__(self, name, description, damage_bonus, accuracy):
        super().__init__(name, description)
        self.damage_bonus = damage_bonus
        self.accuracy = accuracy


class Lightsaber(Weapon):
    def __init__(self):
        super().__init__(
            "Lightsaber",
            "An elegant weapon for a more civilized age.",
            damage_bonus=6,
            accuracy=8
        )

class Blaster(Weapon):
    def __init__(self):
        super().__init__(
            "Blaster",
            "A ranged weapon favored by soldiers and civilians alike.",
            damage_bonus=4,
            accuracy=7
        )

class ForceLightning(Weapon):
    def __init__(self):
        super().__init__(
            "Force Lightning",
            "Unlimited power! A Sith ability crackling with dark energy.",
            damage_bonus=8,
            accuracy=9
        )


class Consumable(Item):
    """An item that can be used to heal."""
    def __init__(self, name, description, heal_amount):
        super().__init__(name, description)
        self.heal_amount = heal_amount


class BactaPatch(Consumable):
    def __init__(self):
        super().__init__(
            "Bacta Patch",
            "A medical patch infused with bacta. Restores 20 HP.",
            heal_amount=20
        )


class KeyItem(Item):
    """A key item used for story progression."""
    def __init__(self, name, description, is_evidence=False):
        super().__init__(name, description)
        self.is_evidence = is_evidence


class SithHolocron(KeyItem):
    def __init__(self):
        super().__init__(
            "Sith Holocron",
            "A dark pyramid pulsing with Sith knowledge. Contains proof of Palpatine's manipulation of Anakin.",
            is_evidence=True
        )


# =============================================================================
# Character Classes
# =============================================================================

class Character:
    """Base class for all characters."""

    def __init__(self, name, hp, max_hp):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp

    def is_alive(self):
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        print(f"  💥 {self.name} takes {amount} damage! (HP: {self.hp}/{self.max_hp})")

    def __str__(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"


class Player(Character):
    """Player character base class."""

    def __init__(self, name, hp, max_hp, base_damage, defense_threshold):
        super().__init__(name, hp, max_hp)
        self.trust_score = 0
        self.equipped_weapon = None
        self.inventory = []
        self.base_damage = base_damage
        self.defense_threshold = defense_threshold

    def attack(self, target):
        """d20 combat roll vs target defense."""
        damage_bonus = self.equipped_weapon.damage_bonus if self.equipped_weapon else self.base_damage
        roll = roll_d20()
        total = roll + damage_bonus
        print(f"  🎲 {self.name} rolls {roll} + {damage_bonus} (bonus) = {total} vs Defense {target.defense_threshold}")
        if total >= target.defense_threshold:
            damage = damage_bonus
            print(f"  ✅ Hit!")
            target.take_damage(damage)
        else:
            print(f"  ❌ Miss!")

    def talk(self, location_name, game):
        """Override in subclasses for character-specific dialogue."""
        print(f"  You speak, but have nothing specific to say here.")

    def equip_item(self, item_name):
        """Equip a weapon from inventory."""
        for item in self.inventory:
            if isinstance(item, Weapon) and item.name.lower() == item_name.lower():
                self.equipped_weapon = item
                print(f"  ⚔️ You equip the {item.name}.")
                return
        print(f"  You don't have a weapon called '{item_name}'.")

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"  🎒 Added {item.name} to inventory.")

    def use_item(self, item_name):
        """Use a consumable item."""
        for item in self.inventory:
            if isinstance(item, Consumable) and item.name.lower() == item_name.lower():
                self.hp = min(self.max_hp, self.hp + item.heal_amount)
                self.inventory.remove(item)
                print(f"  💚 Used {item.name}. HP restored to {self.hp}/{self.max_hp}.")
                return
        print(f"  You don't have '{item_name}' or it can't be used.")

    def show_inventory(self):
        if not self.inventory:
            print("  🎒 Your inventory is empty.")
        else:
            print("  🎒 Inventory:")
            for item in self.inventory:
                print(f"    - {item.name}: {item.description}")

    def show_status(self):
        print(f"\n  📊 STATUS: {self.name}")
        print(f"    HP: {self.hp}/{self.max_hp}")
        print(f"    Trust Score: {self.trust_score}")
        equipped = self.equipped_weapon.name if self.equipped_weapon else "None"
        print(f"    Equipped: {equipped}")
        print(f"    Inventory: {len(self.inventory)} item(s)")


# --- Player Subclasses ---

class ObiWan(Player):
    """Balanced stats. Needs 3 Trust Points (earned by defending Anakin, acting like a brother)."""
    def __init__(self):
        super().__init__("Obi-Wan Kenobi", hp=100, max_hp=100, base_damage=5, defense_threshold=10)
        self.equipped_weapon = Lightsaber()
        self.inventory = [self.equipped_weapon, BactaPatch()]
        self.trust_needed = 3
        self.needs_holocron = False

    def talk(self, location_name, game):
        if location_name == "Jedi Council Room":
            print("\n  You speak with the Council about Anakin's struggles.")
            print("  1. 'Anakin is like a brother to me. Give him a chance.'")
            print("  2. 'The Council's concerns are valid. Anakin must prove himself.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. You defend Anakin before the Council.")
            else:
                print("  You side with the Council. Anakin feels dismissed.")
        elif location_name == "Jedi Temple":
            print("\n  Amidst the chaos of Order 66, you think of Anakin.")
            print("  1. 'Anakin, whatever has happened — I am still your brother.'")
            print("  2. 'The Jedi are gone. Anakin must answer for this.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Your loyalty reaches Anakin through the Force.")
            else:
                print("  Cold logic. But Anakin slips further from reach.")
        elif location_name == "Padmé's Apartment":
            print("\n  Senator Amidala is pacing anxiously in the living room.")
            print("  Padmé: 'Master Kenobi... I'm so glad you're here. Anakin is acting strange.'")
            print("  Padmé: 'He keeps talking about Chancellor Palpatine. I think he is hiding something dangerous.'")
            print("\n  How do you respond?")
            print("  1. 'I love him like a brother, Padmé. We can still reach him.'")
            print("  2. 'He has gone too far. He is no longer the man we knew.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Padmé's hope strengthens your resolve.")
                print("  💡 CLUE: She urges you to search the Senate Building for proof of Palpatine's manipulation.")
            else:
                print("  Sadness fills the room. Padmé weeps quietly.")
        else:
            print("  There's nothing specific to talk about here.")


class Padme(Player):
    """Low combat, high stealth. Needs 1 Trust Point + SithHolocron to win."""
    def __init__(self):
        super().__init__("Padmé Amidala", hp=70, max_hp=70, base_damage=3, defense_threshold=12)
        self.equipped_weapon = Blaster()
        self.inventory = [self.equipped_weapon, BactaPatch()]
        self.trust_needed = 1
        self.needs_holocron = True

    def talk(self, location_name, game):
        if location_name == "Padmé's Apartment":
            print("\n  You walk into your apartment. Anakin is standing on the balcony, staring into the Coruscant night.")
            print("  Anakin: 'I had the dream again... I can't lose you, Padmé. Chancellor Palpatine says there is a way to stop death...'")
            print("\n  How do you respond?")
            print("  1. 'We will figure this out together, my love. I am not going anywhere.'")
            print("  2. 'You're being paranoid, Anakin. It was just a dream.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Anakin relaxes slightly, the tension leaving his shoulders.")
                print("     He pulls you close. The fear in his eyes softens — for now.")
                print("  💡 CLUE: Palpatine's knowledge of stopping death is unnatural.")
                print("     You need to search his office in the Senate Building.")
            else:
                print("  Anakin turns away, his face hardening.")
                print("  'You don't understand. I will do whatever it takes to save you.'")
                print("  He leaves abruptly. You gained no trust.")
        elif location_name == "The Senate Building":
            print("\n  You confront Palpatine in the Senate halls.")
            print("  1. 'I know what you've done to Anakin. I will expose you.'")
            print("  2. 'Chancellor, there must be another way.'")
            choice = input("  > ").strip()
            if choice == "1":
                print("  ⚡ Palpatine smirks. 'Brave words, Senator.' The confrontation intensifies.")
            else:
                print("  Palpatine's smile grows. He has your measure.")
        else:
            print("  There's nothing specific to talk about here.")


class Ahsoka(Player):
    """Fast combat. Skips Council politics. Needs 3 Trust Points (earned by agreeing with Anakin's Jedi frustrations)."""
    def __init__(self):
        super().__init__("Ahsoka Tano", hp=90, max_hp=90, base_damage=5, defense_threshold=9)
        self.equipped_weapon = Lightsaber()
        self.inventory = [self.equipped_weapon, BactaPatch()]
        self.trust_needed = 3
        self.needs_holocron = False

    def attack(self, target):
        """Ahsoka attacks twice (fast combat)."""
        print(f"  ⚡ Ahsoka moves with blinding speed — TWO strikes!")
        super().attack(target)
        if target.is_alive():
            super().attack(target)

    def talk(self, location_name, game):
        if location_name == "Jedi Council Room":
            print("\n  You address the Council — as an outsider who left the Order.")
            print("  1. 'The Jedi failed Anakin. They fail everyone who questions them.'")
            print("  2. 'The Jedi are not perfect, but they are necessary.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Anakin, listening from afar, feels understood.")
            else:
                print("  You defend the system that cast you out. It feels hollow.")
        elif location_name == "Jedi Temple":
            print("\n  Surrounded by clone troopers, you think of Anakin's warnings.")
            print("  1. 'He was right. The Republic, the Jedi — it's all corrupt.'")
            print("  2. 'Even if he was right, this violence is not the answer.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Shared rage — a dangerous but real connection.")
            else:
                print("  A noble thought. But Anakin can't hear nuance anymore.")
        elif location_name == "Padmé's Apartment":
            print("\n  Senator Amidala looks up from a holotable covered in datapads.")
            print("  Padmé: 'Ahsoka... I wasn't sure who else to call. Anakin won't listen to me. He trusts you. He always has.'")
            print("\n  How do you respond?")
            print("  1. 'Skyguy — I understand now. The Order never deserved you.'")
            print("  2. 'Your anger at the Jedi is real, but don't let it define you.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. A spark of the old bond ignites.")
                print("  💡 CLUE: Padmé whispers that Palpatine's office in the Senate holds dark secrets.")
            else:
                print("  Wise words. But Anakin is past wisdom right now.")
        else:
            print("  There's nothing specific to talk about here.")


class MaceWindu(Player):
    """Heavy combat (Hard Mode). Needs to grant Anakin the rank of Master to win."""
    def __init__(self):
        super().__init__("Mace Windu", hp=110, max_hp=110, base_damage=7, defense_threshold=9)
        self.equipped_weapon = Lightsaber()
        self.inventory = [self.equipped_weapon]
        self.trust_needed = 3  # Represented as 3 hard choices
        self.needs_holocron = False
        self.granted_rank = False

    def attack(self, target):
        """Mace's Vaapad form hits harder."""
        damage_bonus = (self.equipped_weapon.damage_bonus if self.equipped_weapon else self.base_damage) + 2
        roll = roll_d20()
        total = roll + damage_bonus
        print(f"  🎲 {self.name} rolls {roll} + {damage_bonus} (Vaapad bonus) = {total} vs Defense {target.defense_threshold}")
        if total >= target.defense_threshold:
            print(f"  ✅ Crushing hit!")
            target.take_damage(damage_bonus)
        else:
            print(f"  ❌ Miss!")

    def talk(self, location_name, game):
        if location_name == "Jedi Council Room":
            print("\n  The Council awaits your decision on Anakin's rank.")
            print("  1. 'I move to grant Anakin Skywalker the rank of Jedi Master.'")
            print("  2. 'He is not ready. The rank is denied.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                self.granted_rank = True
                print("  💙 Trust +1. Anakin's shock turns to gratitude — a crack in Palpatine's grip.")
            else:
                print("  'This is outrageous!' Anakin storms out. The rift deepens.")
        elif location_name == "Jedi Temple":
            print("\n  Clone troopers swarm the Temple. You sense Anakin's presence in the Force.")
            print("  1. 'Skywalker — if you can hear me — you are still a Jedi.'")
            print("  2. 'Skywalker has betrayed the Order. He is the enemy now.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Even Mace Windu can bend. Anakin feels it.")
            else:
                print("  Cold and final. The door slams shut on any reconciliation.")
        elif location_name == "Padmé's Apartment":
            print("\n  Senator Amidala stands when you enter, arms crossed, jaw set.")
            print("  Padmé: 'Master Windu. You denied him the rank. You pushed him toward Palpatine. You have to fix this.'")
            print("\n  How do you respond?")
            print("  1. 'You're right, Senator. I misjudged him. I will make it right.'")
            print("  2. 'My duty is to the Order, not to one man's feelings.'")
            choice = input("  > ").strip()
            if choice == "1":
                self.trust_score += 1
                print("  💙 Trust +1. Humility from Mace Windu — rare and powerful.")
                print("  💡 CLUE: Padmé points you toward the Senate Building. 'That's where Palpatine has him.'")
            else:
                print("  Padmé stares at you. 'Then you have already lost him.'")
        else:
            print("  There's nothing specific to talk about here.")


# =============================================================================
# Enemy Classes
# =============================================================================

class Enemy(Character):
    """Base class for enemies."""

    def __init__(self, name, hp, max_hp, damage_output, defense_threshold, description, xp_value=10):
        super().__init__(name, hp, max_hp)
        self.damage_output = damage_output
        self.defense_threshold = defense_threshold
        self.description = description
        self.xp_value = xp_value

    def enemy_attack(self, target):
        roll = roll_d20()
        total = roll + self.damage_output
        print(f"  🎲 {self.name} rolls {roll} + {self.damage_output} = {total} vs your defense ({target.defense_threshold})")
        if total >= target.defense_threshold:
            print(f"  ✅ {self.name} hits!")
            target.take_damage(self.damage_output)
        else:
            print(f"  ❌ {self.name} misses!")


class CountDooku(Enemy):
    def __init__(self):
        super().__init__(
            "Count Dooku", hp=60, max_hp=60,
            damage_output=5, defense_threshold=10,
            description="The elegant Sith Lord regards you with cold amusement.",
            xp_value=25
        )

class CloneTrooper(Enemy):
    def __init__(self):
        super().__init__(
            "Clone Trooper", hp=30, max_hp=30,
            damage_output=4, defense_threshold=9,
            description="A CT-series trooper, visor gleaming, blaster raised. Execute Order 66.",
            xp_value=10
        )

class Palpatine(Enemy):
    """Survival boss — cannot be killed, must survive 3 turns."""
    def __init__(self):
        super().__init__(
            "Emperor Palpatine", hp=999, max_hp=999,
            damage_output=8, defense_threshold=15,
            description="The Emperor's true face is revealed — ancient, terrifying, and infinitely patient.",
            xp_value=0
        )

    def take_damage(self, amount):
        print(f"  ⚡ The Force deflects your attack! Palpatine cannot be defeated by combat alone.")

class CorruptedAnakin(Enemy):
    def __init__(self):
        super().__init__(
            "Darth Vader (Corrupted Anakin)", hp=80, max_hp=80,
            damage_output=7, defense_threshold=11,
            description="The man who was Anakin Skywalker is gone. Only Darth Vader remains.",
            xp_value=0
        )


# =============================================================================
# Location Class
# =============================================================================

class Location:
    """A location in the game world."""

    def __init__(self, name, description, is_safe_room=False):
        self.name = name
        self.description = description
        self.connections = {}
        self.items = []
        self.enemy = None
        self.is_safe_room = is_safe_room
        self.visited = False
        self.searched = False
        self._description_count = 0  # guard against duplicate prints

    def add_connection(self, direction, location):
        self.connections[direction] = location

    def describe_room(self):
        self._description_count += 1
        if self._description_count > 1:
            return  # already described on this arrival — skip duplicate
        print(f"\n{'='*55}")
        print(f"  📍 {self.name}")
        print(f"{'='*55}")
        print(f"  {self.description}")
        if self.is_safe_room:
            print(f"  ✨ (Safe Zone — no enemies will attack here.)")
        if self.enemy and self.enemy.is_alive():
            print(f"\n  ⚠️  ENEMY PRESENT: {self.enemy.name}")
            print(f"     {self.enemy.description}")
        if self.items:
            print(f"\n  📦 Items visible: {', '.join(str(i) for i in self.items)}")
        exits = list(self.connections.keys())
        print(f"\n  🚪 Exits: {', '.join(exits) if exits else 'None'}")

    def search(self, game_engine):
        """Search the room for items. Costs 2 hours."""
        game_engine.hours_remaining -= 2
        print(f"\n  🔍 You search the area... (2 hours pass | {game_engine.hours_remaining}h remaining)")
        if self.searched:
            print("  You find nothing new.")
            return
        self.searched = True
        if self.items:
            for item in self.items[:]:
                print(f"  ✨ You found: {item.name} — {item.description}")
                game_engine.current_player.add_to_inventory(item)
            self.items.clear()
        else:
            print("  Nothing of interest here.")


# =============================================================================
# World Builder
# =============================================================================

def create_world():
    """Create and connect all six locations. Returns starting location."""

    invisible_hand = Location(
        "The Invisible Hand",
        "The flagship of General Grievous. Smoke fills the corridors. Droids lie defeated. "
        "Count Dooku stands at the far end, lightsaber ignited, waiting.",
    )

    council_room = Location(
        "Jedi Council Room",
        "The circular chamber of the Jedi High Council. Holographic figures flicker in the seats. "
        "The air is heavy with unspoken tension — Anakin's promotion hangs over everything.",
    )

    jedi_temple = Location(
        "Jedi Temple",
        "The great Coruscant Temple, now a battlefield. Clone troopers storm the halls. "
        "The screams of Younglings echo. Order 66 is in effect.",
    )

    padme_apartment = Location(
        "Padmé's Apartment",
        "A luxurious penthouse overlooking the glittering Coruscant skyline. The balcony doors are open, "
        "letting in the hum of the city. Holopads and datapads are scattered across the table.",
        is_safe_room=True
    )

    senate_building = Location(
        "The Senate Building",
        "The vast rotunda of the Galactic Senate. Pod-chairs float in the dark. "
        "Palpatine moves through the shadows. A Sith Holocron rests on the Chancellor's desk.",
    )

    mustafar = Location(
        "Mustafar",
        "A hellscape of molten lava and industrial platforms. The air burns. "
        "Anakin — no, Darth Vader — stands at the edge of a platform, eyes burning Sith yellow.",
    )

    # Connections
    invisible_hand.add_connection("south", council_room)
    council_room.add_connection("north", invisible_hand)
    council_room.add_connection("south", jedi_temple)
    jedi_temple.add_connection("north", council_room)
    jedi_temple.add_connection("east", padme_apartment)
    jedi_temple.add_connection("ship", mustafar)
    padme_apartment.add_connection("west", jedi_temple)
    padme_apartment.add_connection("east", senate_building)
    senate_building.add_connection("west", padme_apartment)

    # Enemies
    invisible_hand.enemy = CountDooku()
    jedi_temple.enemy = CloneTrooper()
    senate_building.enemy = Palpatine()

    # Items
    padme_apartment.items.append(BactaPatch())
    senate_building.items.append(SithHolocron())

    return invisible_hand


# =============================================================================
# Combat System
# =============================================================================

class Combat:
    """Manages turn-based combat."""

    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    COMBAT_END = "combat_end"

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.state = Combat.PLAYER_TURN
        self.turn_count = 0
        self.palpatine_survival_turns = 3  # Player must survive 3 turns

    def start(self):
        is_palpatine = isinstance(self.enemy, Palpatine)
        print(f"\n{'⚔️'*20}")
        print(f"  COMBAT: {self.player.name} vs {self.enemy.name}")
        if is_palpatine:
            print(f"  ⚡ SURVIVAL BATTLE — Survive {self.palpatine_survival_turns} turns!")
        print(f"{'⚔️'*20}")

        while self.state != Combat.COMBAT_END:
            if self.state == Combat.PLAYER_TURN:
                self.player_turn(is_palpatine)
            elif self.state == Combat.ENEMY_TURN:
                self.enemy_turn(is_palpatine)

        return self.get_result(is_palpatine)

    def player_turn(self, is_palpatine):
        print(f"\n  {self.player} | {self.enemy}")
        if is_palpatine:
            turns_left = self.palpatine_survival_turns - self.turn_count
            print(f"  ⏳ Survive {turns_left} more turn(s)!")
        print("  Actions: attack | run | use [item]")
        action = input("  > ").lower().strip()

        if action == "attack":
            self.player.attack(self.enemy)
            if not is_palpatine and not self.enemy.is_alive():
                print(f"\n  🎉 {self.enemy.name} has been defeated!")
                self.state = Combat.COMBAT_END
            else:
                self.state = Combat.ENEMY_TURN
        elif action == "run":
            if random.random() < 0.5:
                print("  You slip away into the shadows!")
                self.state = Combat.COMBAT_END
            else:
                print("  No escape! The enemy blocks your path.")
                self.state = Combat.ENEMY_TURN
        elif action.startswith("use "):
            item_name = action[4:].strip()
            self.player.use_item(item_name)
        else:
            print("  Unknown action.")

    def enemy_turn(self, is_palpatine):
        print(f"\n  {self.enemy.name}'s turn...")
        self.enemy.enemy_attack(self.player)
        self.turn_count += 1

        if not self.player.is_alive():
            print(f"\n  💀 {self.player.name} has fallen!")
            self.state = Combat.COMBAT_END
        elif is_palpatine and self.turn_count >= self.palpatine_survival_turns:
            print(f"\n  ⚡ You endured Palpatine's assault! He withdraws, furious.")
            self.state = Combat.COMBAT_END
        else:
            self.state = Combat.PLAYER_TURN

    def get_result(self, is_palpatine):
        if not self.player.is_alive():
            return "defeat"
        if is_palpatine and self.turn_count >= self.palpatine_survival_turns:
            return "survived"
        if not self.enemy.is_alive():
            return "victory"
        return "fled"


# =============================================================================
# Game Engine
# =============================================================================

class GameEngine:
    """Main game controller / engine."""

    EXPLORING = "exploring"
    IN_COMBAT = "in_combat"
    GAME_OVER = "game_over"
    VICTORY = "victory"

    def __init__(self):
        self.current_player = None
        self.current_location = None
        self.hours_remaining = 24
        self.game_active = True
        self.state = GameEngine.EXPLORING

    def start_game(self):
        self.show_intro()
        self.current_player = self.select_character()
        self.current_location = create_world()
        self.current_location.visited = True
        self.current_location.describe_room()
        self.main_loop()

    def show_intro(self):
        print("\n" + "★"*60)
        print("       STAR WARS: WHAT IF — A TEXT ADVENTURE")
        print("              Episode III: The Turning Point")
        print("★"*60)
        print("""
  The galaxy teeters on the edge of catastrophe.
  Palpatine's web of manipulation tightens around Anakin Skywalker.
  The Jedi Council is blind. The Senate has fallen.

  YOU have 24 hours to reach Mustafar and prevent Anakin
  from becoming Darth Vader forever.

  Trust must be earned. Evidence must be gathered.
  Choose your words carefully — and your battles wisely.

  May the Force be with you.
""")
        print("★"*60)
        input("\n  [Press ENTER to begin...]")

    def select_character(self):
        """Select player character via d4 roll."""
        print("\n  🎲 Rolling the Galactic Dice to determine your champion...")
        roll = roll_d4()
        characters = {1: ObiWan, 2: Padme, 3: Ahsoka, 4: MaceWindu}
        char_class = characters[roll]
        player = char_class()

        print(f"\n  You rolled a {roll}!")
        print(f"\n  ⚡ YOU ARE: {player.name}")

        descriptions = {
            "Obi-Wan Kenobi": "Balanced Jedi Master. Earn 3 Trust Points by defending Anakin like a brother.",
            "Padmé Amidala": "Low combat, high courage. Earn 1 Trust Point AND find the Sith Holocron.",
            "Ahsoka Tano": "Lightning-fast fighter. Earn 3 Trust Points by validating Anakin's Jedi frustrations.",
            "Mace Windu": "Heavy combat (Hard Mode). Make 3 selfless choices — starting with granting Anakin his rank.",
        }
        print(f"  {descriptions[player.name]}")
        print(f"\n  Trust Needed: {player.trust_needed} | Needs Holocron: {player.needs_holocron}")
        input("\n  [Press ENTER to begin your mission...]")
        return player

    def main_loop(self):
        """Main game loop."""
        while self.game_active:
            self.check_time()
            if not self.game_active:
                break

            if self.state == GameEngine.EXPLORING:
                self.show_prompt()
                command = input("\n  > ").lower().strip()
                self.process_command(command)

            elif self.state == GameEngine.GAME_OVER:
                self.show_game_over()
                break

            elif self.state == GameEngine.VICTORY:
                self.show_victory()
                break

    def show_prompt(self):
        print(f"\n  ⏱  Hours Remaining: {self.hours_remaining} | "
              f"Trust: {self.current_player.trust_score}/{self.current_player.trust_needed} | "
              f"HP: {self.current_player.hp}/{self.current_player.max_hp}")
        print("  Commands: go [dir/ship] | look | search | talk | attack | "
              "equip [item] | use [item] | inventory | status | help | quit")

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return
        action = parts[0]

        if action == "help":
            self.show_help()
        elif action == "look":
            self.current_location._description_count = 0
            self.current_location.describe_room()
        elif action == "go" and len(parts) > 1:
            self.move(parts[1])
        elif action in ["north", "south", "east", "west", "ship"]:
            self.move(action)
        elif action == "search":
            self.current_location.search(self)
        elif action == "talk":
            self.current_player.talk(self.current_location.name, self)
        elif action == "attack":
            self.trigger_combat()
        elif action == "equip" and len(parts) > 1:
            self.current_player.equip_item(" ".join(parts[1:]))
        elif action == "use" and len(parts) > 1:
            self.current_player.use_item(" ".join(parts[1:]))
        elif action in ["inventory", "i"]:
            self.current_player.show_inventory()
        elif action == "status":
            self.current_player.show_status()
        elif action == "quit":
            print("\n  Thanks for playing! May the Force be with you.")
            self.game_active = False
        else:
            print("  Unknown command. Type 'help' for options.")

    def move(self, direction):
        """Move the player to a new location."""
        if direction in self.current_location.connections:
            self.hours_remaining -= 1
            self.current_location = self.current_location.connections[direction]
            self.current_location._description_count = 0  # reset so new arrival describes once
            print(f"\n  ✈️  Traveling... (1 hour passes | {self.hours_remaining}h remaining)")
            self.current_location.describe_room()
            self.current_location.visited = True

            # Auto-trigger Mustafar ending
            if self.current_location.name == "Mustafar":
                self.evaluate_mustafar_ending()
        else:
            print(f"  You can't go '{direction}' from here.")

    def trigger_combat(self):
        """Initiate combat with the current room's enemy."""
        enemy = self.current_location.enemy
        if not enemy or not enemy.is_alive():
            print("  There's no enemy to fight here.")
            return

        battle = Combat(self.current_player, enemy)
        result = battle.start()

        if result == "victory":
            print(f"\n  🏆 Victory over {enemy.name}!")
            self.current_location.enemy = None
            # Special: defeating Dooku allows progress
            if isinstance(enemy, CountDooku):
                print("  The way forward is clear. You have escaped the Invisible Hand.")
        elif result == "survived":
            print("\n  🛡️  You survived Palpatine's assault! Barely.")
        elif result == "defeat":
            self.state = GameEngine.GAME_OVER
        elif result == "fled":
            print("  You retreat from the battle.")

    def check_time(self):
        """Check if the Galactic Clock has run out."""
        if self.hours_remaining <= 0:
            print("\n  ⏰ TIME'S UP! The Galactic Clock has struck zero.")
            print("  Anakin completes his fall. Darth Vader rises.")
            print("  The Republic is no more. You were too late.")
            self.game_active = False

    def evaluate_mustafar_ending(self):
        """Evaluate win/loss state when player reaches Mustafar."""
        player = self.current_player
        print("\n" + "🔥"*28)
        print("  THE MOMENT OF TRUTH — MUSTAFAR")
        print("🔥"*28)
        print(f"\n  Anakin Skywalker stands before you.")
        print(f"  Trust Score: {player.trust_score}/{player.trust_needed}")

        has_holocron = any(isinstance(i, KeyItem) and i.is_evidence for i in player.inventory)

        # Win condition: Evidence route (Padmé primarily)
        if player.needs_holocron and has_holocron and player.trust_score >= player.trust_needed:
            self.show_victory(
                win_type="evidence",
                message=f"  You present the Sith Holocron. Anakin stares at the proof of Palpatine's\n"
                        f"  manipulation. 'He lied to me... about everything.' The yellow fades from his eyes.\n"
                        f"  Anakin Skywalker has been saved."
            )

        # Win condition: Trust route
        elif not player.needs_holocron and player.trust_score >= player.trust_needed:
            self.show_victory(
                win_type="trust",
                message=f"  '{player.name}...' Anakin lowers his lightsaber. The bond between you holds.\n"
                        f"  He steps back from the edge — literally and spiritually.\n"
                        f"  'I don't have to do this. I... I choose not to.'\n"
                        f"  Anakin Skywalker has been saved."
            )

        # Loss condition: Trust/Evidence checks fail — fight Corrupted Anakin
        else:
            print("\n  Your bond wasn't strong enough. Anakin's eyes burn Sith yellow.")
            print("  'You cannot stop what has already begun.'\n")
            print("  FINAL BOSS: Darth Vader (Corrupted Anakin)")
            final_boss = CorruptedAnakin()
            battle = Combat(self.current_player, final_boss)
            result = battle.start()
            if result == "defeat":
                self.show_game_over(
                    message="  You fall on the volcanic plains of Mustafar.\n"
                            "  Darth Vader stands over you. The Empire rises.\n"
                            "  Hope dies with you."
                )
            else:
                # Beat Anakin in combat — tragic win
                self.show_victory(
                    win_type="tragic",
                    message="  Anakin collapses on the lava's edge. You've defeated him in combat —\n"
                            "  but at what cost? There was no Vader today. But the Anakin you knew\n"
                            "  is gone. The galaxy grieves a might-have-been."
                )

    def show_victory(self, win_type="trust", message=""):
        print("\n" + "★"*60)
        print("                    🎉 YOU WIN! 🎉")
        if win_type == "trust":
            print("            VICTORY: THE POWER OF CONNECTION")
        elif win_type == "evidence":
            print("            VICTORY: TRUTH EXPOSES THE DARKNESS")
        elif win_type == "tragic":
            print("          VICTORY (PYRRHIC): THE COST OF FAILURE")
        print("★"*60)
        if message:
            print(f"\n{message}")
        print("\n  The galaxy breathes again. For now.")
        print("\n  THANK YOU FOR PLAYING — STAR WARS: WHAT IF")
        print("★"*60)
        self.game_active = False

    def show_game_over(self, message=""):
        print("\n" + "☠"*60)
        print("                    GAME OVER")
        print("☠"*60)
        if message:
            print(f"\n{message}")
        else:
            print("\n  Your mission has failed. The dark side has won.")
        print("\n  (But a Jedi always has another chance — try again!)")
        print("☠"*60)
        self.game_active = False

    def show_help(self):
        print("\n  📜 COMMANDS:")
        print("  go [direction]   - Move: north / south / east / west / ship")
        print("  look             - Describe current location")
        print("  search           - Search room for items (costs 2 hours)")
        print("  talk             - Dialogue that may earn Trust Points")
        print("  attack           - Fight the enemy in this room")
        print("  equip [weapon]   - Equip a weapon from your inventory")
        print("  use [item]       - Use a consumable item (e.g., Bacta Patch)")
        print("  inventory        - Show your items")
        print("  status           - Show HP, Trust, weapon")
        print("  help             - Show this list")
        print("  quit             - Exit the game")


# =============================================================================
# Run the Game
# =============================================================================

if __name__ == "__main__":
    game = GameEngine()
    game.start_game()