# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a text-based adventure game called "Alien Starship Adventure" implemented as a single Python file. The game simulates exploring an abandoned alien starship with the objective of finding escape pods to get off the ship.

## Running the Game

```bash
python3 alien_starship_adventure.py
```

## Architecture

The game follows a class-based architecture with four main components:

### Core Classes

- **Item**: Represents collectible objects with name, description, and usability flag
- **Room**: Represents game locations with connections, items, locking mechanisms, and level hierarchy  
- **Player**: Manages player state including current location, inventory (max 10 items), and item operations
- **AlienStarshipGame**: Main game controller that orchestrates room creation, item placement, game logic, and user interaction

### Game Structure

The starship consists of 50+ interconnected rooms across 5 levels:
- Level 1: Lower decks (docking bay, cargo, maintenance)
- Level 2: Crew quarters (living spaces, medical, labs)  
- Level 3: Operations (navigation, communications, computer systems)
- Level 4: Command (bridge, captain's quarters, escape pod bays)
- Level 5: Upper systems (engines, power, life support)

### Key Mechanics

- **Room Locking**: Certain rooms require specific items to unlock (security_keycard, command_codes, etc.)
- **Item Interactions**: Special behaviors when using items in specific locations (e.g., plasma_torch in docking_bay reveals hidden items)
- **Victory Condition**: Find working escape pods in the escape pod bays to win
- **Navigation**: Rooms connected via directional exits (north, south, east, west, up, down)

### Game Initialization

The game setup follows this sequence:
1. `create_items()` - Defines all 15+ collectible items
2. `create_rooms()` - Creates all 50+ rooms with descriptions and level assignments  
3. `setup_connections()` - Establishes directional connections between rooms
4. `place_items()` - Distributes items throughout rooms and configures locked room requirements

### Command System

The game loop processes natural language commands:
- Movement: `go north`, `north`, `n`
- Items: `take keycard`, `use plasma torch`  
- Info: `look`, `inventory`, `help`
- Exit: `quit`, `exit`

## Development Notes

Since this is a single-file game with no external dependencies, testing and modifications are straightforward. The modular class structure allows for easy extension of rooms, items, or game mechanics.

The game state is entirely in-memory with no persistence - each run starts fresh from the docking bay.