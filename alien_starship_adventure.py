#!/usr/bin/env python3
"""
Alien Starship Adventure Game
A text-based adventure set on an abandoned alien starship orbiting a desolate planet.
Objective: Find escape pods to get off the ship by collecting items and solving puzzles.
"""

from typing import Optional

class Item:
    def __init__(self, name: str, description: str, usable: bool = False):
        self.name = name
        self.description = description
        self.usable = usable

class Room:
    def __init__(self, name: str, description: str, level: int):
        self.name = name
        self.description = description
        self.level = level
        self.exits = {}
        self.items = []
        self.visited = False
        self.locked = False
        self.lock_description = ""
        self.required_item = None

class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []
        self.max_inventory = 10

    def add_item(self, item: Item) -> bool:
        if len(self.inventory) < self.max_inventory:
            self.inventory.append(item)
            return True
        return False

    def has_item(self, item_name: str) -> bool:
        return any(item.name.lower() == item_name.lower() for item in self.inventory)

    def get_item(self, item_name: str) -> Optional[Item]:
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def remove_item(self, item_name: str) -> bool:
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                del self.inventory[i]
                return True
        return False

class AlienStarshipGame:
    def __init__(self):
        self.player = Player()
        self.rooms = {}
        self.items = {}
        self.game_over = False
        self.victory = False
        self.escape_pods_found = 0
        self.required_escape_pods = 1
        
        self.create_items()
        self.create_rooms()
        self.setup_connections()
        self.place_items()
        
        # Start in the docking bay
        self.player.current_room = self.rooms["docking_bay"]

    def create_items(self):
        """Create all items in the game"""
        items_data = [
            ("security_keycard", "A magnetic keycard with alien symbols", True),
            ("plasma_torch", "A portable cutting tool that still has power", True),
            ("oxygen_canister", "Emergency oxygen supply", True),
            ("alien_crystal", "A glowing crystal that hums with energy", True),
            ("maintenance_tool", "Alien maintenance device with multiple attachments", True),
            ("data_pad", "An alien tablet displaying navigation data", False),
            ("energy_cell", "High-capacity power cell", True),
            ("neural_interface", "Alien neural interface headset", True),
            ("gravity_boots", "Magnetic boots for zero-gravity movement", True),
            ("translation_device", "Device that translates alien text", True),
            ("emergency_beacon", "Distress beacon still functional", False),
            ("alien_weapon", "Strange alien energy weapon", False),
            ("medical_kit", "Alien medical supplies", True),
            ("ship_schematic", "Holographic ship layout", False),
            ("command_codes", "Access codes for ship systems", True),
        ]
        
        for name, desc, usable in items_data:
            self.items[name] = Item(name, desc, usable)

    def create_rooms(self):
        """Create all 50+ rooms across multiple levels"""
        rooms_data = [
            # Level 1 - Lower Decks
            ("docking_bay", "The ship's main docking bay. Your shuttle is docked here, but it's damaged beyond repair. Strange alien symbols cover the walls.", 1),
            ("cargo_hold_1", "A vast cargo hold with massive alien containers. Some are open, revealing strange artifacts.", 1),
            ("cargo_hold_2", "Another cargo hold, this one mostly empty except for scattered debris.", 1),
            ("maintenance_shaft_1", "A narrow maintenance corridor with exposed conduits and alien machinery.", 1),
            ("storage_room_1", "A storage room filled with alien equipment and supplies.", 1),
            ("storage_room_2", "Another storage room, this one seems to have been ransacked.", 1),
            ("engine_room_lower", "The lower section of the massive engine room. Alien technology hums quietly.", 1),
            ("waste_processing", "The ship's waste processing facility. The smell is... alien.", 1),
            ("water_recycling", "Water recycling systems still function, creating an eerie dripping sound.", 1),
            ("emergency_stairwell_1", "A emergency stairwell leading to upper levels.", 1),
            ("airlock_1", "An airlock leading to the ship's exterior. The outer door is sealed.", 1),
            ("power_distribution_1", "A room full of alien power distribution systems.", 1),
            
            # Level 2 - Crew Quarters
            ("crew_quarters_1", "Personal quarters with an alien sleeping alcove and strange personal effects.", 2),
            ("crew_quarters_2", "More crew quarters, these seem hastily abandoned.", 2),
            ("crew_quarters_3", "Crew quarters with signs of a struggle.", 2),
            ("crew_quarters_4", "Luxurious quarters, possibly for an officer.", 2),
            ("crew_mess_hall", "The crew's dining area with alien food preparation stations.", 2),
            ("recreation_room", "A room with alien entertainment devices and games.", 2),
            ("gymnasium", "Exercise facility with strange alien fitness equipment.", 2),
            ("medical_bay", "The ship's medical facility with advanced alien medical equipment.", 2),
            ("laboratory_1", "A scientific laboratory with specimens in alien containers.", 2),
            ("laboratory_2", "Another lab focused on materials science.", 2),
            ("corridor_2a", "A main corridor running the length of level 2.", 2),
            ("corridor_2b", "Another corridor with viewports showing the desolate planet below.", 2),
            ("emergency_stairwell_2", "Emergency stairwell connecting levels 1 and 3.", 2),
            
            # Level 3 - Operations
            ("navigation_room", "The ship's navigation center with star charts and alien computers.", 3),
            ("communications", "Communications array with long-range transmitters.", 3),
            ("security_office", "Security station with monitors showing various ship areas.", 3),
            ("armory", "Weapons storage with alien armaments secured behind energy barriers.", 3),
            ("workshop", "Engineering workshop with alien tools and partially assembled devices.", 3),
            ("computer_core", "The ship's main computer systems room, humming with activity.", 3),
            ("hydroponics", "Alien plant cultivation facility with strange, wilted vegetation.", 3),
            ("observation_deck", "A deck with large windows overlooking the planet surface.", 3),
            ("conference_room", "A meeting room with a large holographic display table.", 3),
            ("corridor_3a", "Main corridor of the operations level.", 3),
            ("corridor_3b", "Secondary corridor with access to specialized rooms.", 3),
            ("emergency_stairwell_3", "Stairwell providing access to the bridge level.", 3),
            ("maintenance_shaft_2", "Another maintenance area with complex alien systems.", 3),
            
            # Level 4 - Command
            ("bridge", "The ship's command center with the captain's chair and main controls.", 4),
            ("captain_quarters", "Luxurious captain's quarters with alien artifacts and a personal safe.", 4),
            ("ready_room", "The captain's private meeting room adjacent to the bridge.", 4),
            ("tactical_center", "Advanced tactical systems and weapons control.", 4),
            ("sensor_array", "Long-range sensor control room with displays of nearby space.", 4),
            ("escape_pod_bay_1", "Primary escape pod bay. Several pods are missing, but one remains.", 4),
            ("escape_pod_bay_2", "Secondary escape pod bay. All pods appear to be gone.", 4),
            ("commander_quarters", "First officer's quarters.", 4),
            ("vip_quarters", "Guest quarters for important visitors.", 4),
            ("bridge_corridor", "Corridor leading to various command level rooms.", 4),
            
            # Level 5 - Upper Systems
            ("engine_room_upper", "Upper section of the engine room with main reactor controls.", 5),
            ("shield_generator", "Ship's defensive shield generation systems.", 5),
            ("power_core", "The ship's main power generation facility.", 5),
            ("environmental_control", "Life support and environmental systems control.", 5),
            ("maintenance_shaft_3", "Upper maintenance areas with access to ship's exterior systems.", 5),
            ("emergency_systems", "Emergency power and backup systems.", 5),
            ("upper_corridor", "The highest accessible corridor on the ship.", 5),
        ]
        
        for name, desc, level in rooms_data:
            self.rooms[name] = Room(name, desc, level)

    def setup_connections(self):
        """Set up connections between rooms"""
        connections = [
            # Level 1 connections
            ("docking_bay", {"north": "cargo_hold_1", "east": "maintenance_shaft_1", "up": "emergency_stairwell_1"}),
            ("cargo_hold_1", {"south": "docking_bay", "north": "cargo_hold_2", "east": "storage_room_1"}),
            ("cargo_hold_2", {"south": "cargo_hold_1", "east": "storage_room_2", "north": "engine_room_lower"}),
            ("maintenance_shaft_1", {"west": "docking_bay", "north": "power_distribution_1", "up": "maintenance_shaft_2"}),
            ("storage_room_1", {"west": "cargo_hold_1", "north": "storage_room_2"}),
            ("storage_room_2", {"south": "storage_room_1", "west": "cargo_hold_2", "north": "waste_processing"}),
            ("engine_room_lower", {"south": "cargo_hold_2", "east": "water_recycling", "up": "engine_room_upper"}),
            ("waste_processing", {"south": "storage_room_2", "east": "water_recycling"}),
            ("water_recycling", {"west": "waste_processing", "south": "engine_room_lower"}),
            ("emergency_stairwell_1", {"down": "docking_bay", "up": "emergency_stairwell_2"}),
            ("airlock_1", {"north": "power_distribution_1"}),
            ("power_distribution_1", {"south": "airlock_1", "west": "maintenance_shaft_1"}),
            
            # Level 2 connections
            ("emergency_stairwell_2", {"down": "emergency_stairwell_1", "up": "emergency_stairwell_3", "north": "corridor_2a"}),
            ("corridor_2a", {"south": "emergency_stairwell_2", "north": "crew_mess_hall", "east": "crew_quarters_1", "west": "corridor_2b"}),
            ("corridor_2b", {"east": "corridor_2a", "north": "recreation_room", "south": "medical_bay"}),
            ("crew_quarters_1", {"west": "corridor_2a", "north": "crew_quarters_2"}),
            ("crew_quarters_2", {"south": "crew_quarters_1", "north": "crew_quarters_3"}),
            ("crew_quarters_3", {"south": "crew_quarters_2", "west": "crew_quarters_4"}),
            ("crew_quarters_4", {"east": "crew_quarters_3", "south": "crew_mess_hall"}),
            ("crew_mess_hall", {"north": "crew_quarters_4", "south": "corridor_2a", "east": "gymnasium"}),
            ("recreation_room", {"south": "corridor_2b", "east": "laboratory_1"}),
            ("gymnasium", {"west": "crew_mess_hall", "north": "laboratory_2"}),
            ("medical_bay", {"north": "corridor_2b", "east": "laboratory_1"}),
            ("laboratory_1", {"west": "medical_bay", "north": "recreation_room", "east": "laboratory_2"}),
            ("laboratory_2", {"west": "laboratory_1", "south": "gymnasium"}),
            
            # Level 3 connections
            ("emergency_stairwell_3", {"down": "emergency_stairwell_2", "up": "bridge_corridor", "east": "corridor_3a"}),
            ("corridor_3a", {"west": "emergency_stairwell_3", "north": "navigation_room", "east": "corridor_3b", "south": "computer_core"}),
            ("corridor_3b", {"west": "corridor_3a", "north": "communications", "south": "workshop"}),
            ("navigation_room", {"south": "corridor_3a", "east": "communications", "west": "security_office"}),
            ("communications", {"west": "navigation_room", "south": "corridor_3b", "east": "observation_deck"}),
            ("security_office", {"east": "navigation_room", "south": "armory"}),
            ("armory", {"north": "security_office", "east": "computer_core"}),
            ("computer_core", {"north": "corridor_3a", "west": "armory", "east": "workshop"}),
            ("workshop", {"west": "computer_core", "north": "corridor_3b", "east": "hydroponics"}),
            ("hydroponics", {"west": "workshop", "north": "observation_deck", "east": "conference_room"}),
            ("observation_deck", {"south": "hydroponics", "west": "communications"}),
            ("conference_room", {"west": "hydroponics"}),
            ("maintenance_shaft_2", {"down": "maintenance_shaft_1", "up": "maintenance_shaft_3"}),
            
            # Level 4 connections
            ("bridge_corridor", {"down": "emergency_stairwell_3", "north": "bridge", "east": "captain_quarters", "south": "escape_pod_bay_1"}),
            ("bridge", {"south": "bridge_corridor", "east": "ready_room", "west": "tactical_center"}),
            ("ready_room", {"west": "bridge", "south": "captain_quarters"}),
            ("captain_quarters", {"north": "ready_room", "west": "bridge_corridor", "south": "commander_quarters"}),
            ("tactical_center", {"east": "bridge", "south": "sensor_array"}),
            ("sensor_array", {"north": "tactical_center", "east": "escape_pod_bay_2"}),
            ("escape_pod_bay_1", {"north": "bridge_corridor", "east": "escape_pod_bay_2", "south": "vip_quarters"}),
            ("escape_pod_bay_2", {"west": "escape_pod_bay_1", "north": "sensor_array"}),
            ("commander_quarters", {"north": "captain_quarters", "south": "vip_quarters"}),
            ("vip_quarters", {"north": "commander_quarters", "west": "escape_pod_bay_1"}),
            
            # Level 5 connections
            ("engine_room_upper", {"down": "engine_room_lower", "north": "power_core", "east": "shield_generator"}),
            ("power_core", {"south": "engine_room_upper", "east": "environmental_control"}),
            ("shield_generator", {"west": "engine_room_upper", "north": "environmental_control"}),
            ("environmental_control", {"south": "shield_generator", "west": "power_core", "north": "upper_corridor"}),
            ("upper_corridor", {"south": "environmental_control", "east": "emergency_systems", "west": "maintenance_shaft_3"}),
            ("emergency_systems", {"west": "upper_corridor"}),
            ("maintenance_shaft_3", {"down": "maintenance_shaft_2", "east": "upper_corridor"}),
        ]
        
        for room_name, exits in connections:
            if room_name in self.rooms:
                self.rooms[room_name].exits = exits

    def place_items(self):
        """Place items throughout the ship and set up locked rooms"""
        item_placements = [
            ("security_keycard", "security_office"),
            ("plasma_torch", "workshop"),
            ("oxygen_canister", "emergency_systems"),
            ("alien_crystal", "power_core"),
            ("maintenance_tool", "maintenance_shaft_1"),
            ("data_pad", "navigation_room"),
            ("energy_cell", "power_distribution_1"),
            ("neural_interface", "laboratory_1"),
            ("gravity_boots", "maintenance_shaft_3"),
            ("translation_device", "communications"),
            ("emergency_beacon", "escape_pod_bay_2"),
            ("alien_weapon", "armory"),
            ("medical_kit", "medical_bay"),
            ("ship_schematic", "computer_core"),
            ("command_codes", "captain_quarters"),
        ]
        
        for item_name, room_name in item_placements:
            if item_name in self.items and room_name in self.rooms:
                self.rooms[room_name].items.append(self.items[item_name])
        
        # Set up locked rooms and their requirements
        locked_rooms = [
            ("armory", "security_keycard", "The armory is sealed with a magnetic lock requiring a security keycard."),
            ("captain_quarters", "command_codes", "The captain's quarters require command authorization codes."),
            ("power_core", "maintenance_tool", "The power core is protected by a maintenance panel that needs special tools."),
            ("escape_pod_bay_1", "energy_cell", "The escape pod bay needs power to unlock the launch sequence."),
        ]
        
        for room_name, required_item, lock_desc in locked_rooms:
            if room_name in self.rooms:
                self.rooms[room_name].locked = True
                self.rooms[room_name].required_item = required_item
                self.rooms[room_name].lock_description = lock_desc

    def display_room(self):
        """Display current room information

        Prints a full description the first time a room is visited and a
        shorter reminder on subsequent visits.
        """
        room = self.player.current_room
        print(f"\n=== {room.name.replace('_', ' ').title()} (Level {room.level}) ===")

        if room.visited:
            print(f"You are back in the {room.name.replace('_', ' ')}.")
        else:
            print(room.description)
            room.visited = True
        
        if room.items:
            print(f"\nItems here: {', '.join([item.name.replace('_', ' ').title() for item in room.items])}")
        
        exits = list(room.exits.keys())
        if exits:
            print(f"Exits: {', '.join(exits)}")
        
        if room.locked and room.required_item:
            print(f"\n{room.lock_description}")

    def move_player(self, direction: str) -> bool:
        """Move player to adjacent room"""
        current_room = self.player.current_room
        
        if direction not in current_room.exits:
            print("You can't go that way.")
            return False
        
        next_room_name = current_room.exits[direction]
        next_room = self.rooms.get(next_room_name)
        
        if not next_room:
            print("There's nowhere to go in that direction.")
            return False
        
        if next_room.locked:
            if not next_room.required_item or not self.player.has_item(next_room.required_item):
                print(f"The way is blocked. {next_room.lock_description}")
                return False
            else:
                print(f"You use the {next_room.required_item.replace('_', ' ')} to unlock the way forward.")
                next_room.locked = False
        
        self.player.current_room = next_room
        return True

    def take_item(self, item_name: str):
        """Take an item from the current room"""
        room = self.player.current_room
        item_name = item_name.lower().replace(' ', '_')
        
        for item in room.items:
            if item.name.lower() == item_name:
                if self.player.add_item(item):
                    room.items.remove(item)
                    print(f"You take the {item.name.replace('_', ' ')}.")
                    
                    # Check for escape pod
                    if room.name in ["escape_pod_bay_1", "escape_pod_bay_2"] and item.name == "emergency_beacon":
                        self.escape_pods_found += 1
                        print("\n*** You've found a working escape pod! ***")
                        if self.escape_pods_found >= self.required_escape_pods:
                            self.victory = True
                            print("You can now escape the alien starship!")
                else:
                    print("Your inventory is full!")
                return
        
        print(f"There's no {item_name.replace('_', ' ')} here.")

    def use_item(self, item_name: str):
        """Use an item from inventory"""
        item_name = item_name.lower().replace(' ', '_')
        item = self.player.get_item(item_name)
        
        if not item:
            print(f"You don't have a {item_name.replace('_', ' ')}.")
            return
        
        if not item.usable:
            print(f"You can't use the {item.name.replace('_', ' ')} here.")
            return
        
        room = self.player.current_room
        
        # Special use cases
        if item.name == "plasma_torch" and room.name == "docking_bay":
            print("You use the plasma torch to cut through some debris, revealing a hidden compartment!")
            if "hidden_keycard" not in [i.name for i in room.items]:
                room.items.append(Item("hidden_keycard", "A backup security keycard", True))
        
        elif item.name == "translation_device":
            print("The translation device reveals the meaning of alien symbols around you.")
            print("You learn more about the ship's layout and purpose.")
        
        elif item.name == "neural_interface" and room.name == "computer_core":
            print("You interface with the alien computer system!")
            print("You download critical ship schematics and escape pod locations.")
            if not self.player.has_item("ship_schematic"):
                self.player.add_item(self.items["ship_schematic"])
        
        else:
            print(f"You use the {item.name.replace('_', ' ')}, but nothing happens here.")

    def show_inventory(self):
        """Display player inventory"""
        if not self.player.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.player.inventory:
                print(f"  - {item.name.replace('_', ' ').title()}: {item.description}")

    def show_help(self):
        """Display help information"""
        print("""
Available commands:
  go <direction> - Move in a direction (north, south, east, west, up, down)
  take <item> - Pick up an item
  use <item> - Use an item from your inventory
  inventory - Show your inventory
  look - Look around the current room
  help - Show this help message
  quit - Exit the game
  
Objective: Explore the abandoned alien starship and find escape pods to get off the ship.
Collect items to solve puzzles and unlock new areas.
        """)

    def trigger_random_event(self):
        """Occasionally trigger a small random event."""
        roll = random.random()
        room = self.player.current_room

        # 5% chance to discover an additional item
        if roll < 0.05:
            bonus_items = ["energy_cell", "oxygen_canister", "medical_kit", "alien_crystal"]
            item_name = random.choice(bonus_items)
            item = self.items[item_name]
            room.items.append(item)
            print(f"\n*** You discover a hidden {item.name.replace('_', ' ')}! ***")

        # Another 5% chance for a minor hazard
        elif roll < 0.10:
            print("\n*** A sudden burst of cold air startles you. You manage to stay safe. ***")
            if self.player.inventory and random.random() < 0.5:
                dropped = random.choice(self.player.inventory)
                self.player.inventory.remove(dropped)
                room.items.append(dropped)
                print(f"You fumble and drop your {dropped.name.replace('_', ' ')}!")

    def game_loop(self):
        """Main game loop"""
        print("=== ALIEN STARSHIP ADVENTURE ===")
        print("You dock with an abandoned alien starship orbiting a desolate planet.")
        print("Your mission: explore the ship, collect items, and find escape pods to get off alive!")
        print("Type 'help' for commands.\n")
        
        self.display_room()
        
        while not self.game_over and not self.victory:
            self.trigger_random_event()
            try:
                command = input("\n> ").strip().lower()
                
                if not command:
                    continue
                
                parts = command.split()
                action = parts[0]
                
                if action in ["quit", "exit"]:
                    print("Thanks for playing!")
                    self.game_over = True
                
                elif action in ["help", "?"]:
                    self.show_help()
                
                elif action in ["look", "l"]:
                    self.display_room()
                
                elif action in ["inventory", "inv", "i"]:
                    self.show_inventory()
                
                elif action in ["go", "move", "walk"]:
                    if len(parts) < 2:
                        print("Go where? (north, south, east, west, up, down)")
                    else:
                        direction = parts[1]
                        if self.move_player(direction):
                            self.display_room()
                
                elif action in ["take", "get", "pick"]:
                    if len(parts) < 2:
                        print("Take what?")
                    else:
                        item_name = " ".join(parts[1:])
                        self.take_item(item_name)
                
                elif action in ["use"]:
                    if len(parts) < 2:
                        print("Use what?")
                    else:
                        item_name = " ".join(parts[1:])
                        self.use_item(item_name)
                
                # Allow movement without "go"
                elif action in ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]:
                    direction_map = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}
                    direction = direction_map.get(action, action)
                    if self.move_player(direction):
                        self.display_room()
                
                else:
                    print("I don't understand that command. Type 'help' for available commands.")
                
            except KeyboardInterrupt:
                print("\n\nThanks for playing!")
                self.game_over = True
            except EOFError:
                print("\n\nThanks for playing!")
                self.game_over = True
        
        if self.victory:
            print("\n" + "="*50)
            print("🚀 CONGRATULATIONS! 🚀")
            print("You successfully found an escape pod and escaped the alien starship!")
            print("The mysterious vessel continues its orbit around the desolate planet,")
            print("its secrets partially revealed but many mysteries still remaining...")
            print("="*50)

def main():
    """Main function to start the game"""
    game = AlienStarshipGame()
    game.game_loop()

if __name__ == "__main__":
    main()