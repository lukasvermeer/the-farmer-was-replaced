#!/usr/bin/env python3
"""
Validate that game scripts only use known-valid constant names.
Parses .py files and checks Unlocks.X, Items.X, Entities.X, Grounds.X
against the canonical list from the wiki.

Run: python3 validate.py [file ...]
If no files given, validates all .py files in the current directory (except this one).
"""

import re
import sys
import glob

VALID_UNLOCKS = {
    "Auto_Unlock", "Cactus", "Carrots", "Costs", "Debug",
    "Debug_2", "Dictionaries", "Dinosaurs", "Expand", "Fertilizer",
    "Functions", "Grass", "Leaderboard", "Lists", "Loops", "Mazes",
    "Multi_Trade", "Operators", "Plant", "Polyculture", "Pumpkin",
    "Senses", "Speed", "Sunflowers", "Trees", "Utilities", "Variables",
    "Watering",
}

VALID_ENTITIES = {
    "Grass", "Bush", "Tree", "Carrots", "Pumpkin", "Sunflower",
    "Cactus", "Hedge", "Treasure", "Dinosaur",
}

VALID_GROUNDS = {
    "Grassland", "Soil",
}

VALID_ITEMS = {
    "Hay", "Wood", "Carrot", "Carrot_Seed", "Pumpkin", "Pumpkin_Seed",
    "Sunflower_Seed", "Power", "Water_Tank", "Fertilizer", "Egg",
    "Cactus", "Cactus_Seed", "Bone", "Gold",
}

NAMESPACES = {
    "Unlocks": VALID_UNLOCKS,
    "Items": VALID_ITEMS,
    "Entities": VALID_ENTITIES,
    "Grounds": VALID_GROUNDS,
}

# Match patterns like Unlocks.Something, Items.Something, etc.
PATTERN = re.compile(r'\b(Unlocks|Items|Entities|Grounds)\.(\w+)')


def validate_file(filepath):
    errors = []
    with open(filepath) as f:
        for lineno, line in enumerate(f, 1):
            # Skip comments
            stripped = line.split("#")[0]
            for match in PATTERN.finditer(stripped):
                namespace = match.group(1)
                name = match.group(2)
                valid_set = NAMESPACES[namespace]
                if name not in valid_set:
                    errors.append((lineno, namespace, name))
    return errors


def main():
    files = sys.argv[1:]
    if not files:
        files = [f for f in glob.glob("*.py") if f != "validate.py"]
        files.sort()

    if not files:
        print("No .py files found to validate.")
        return

    total_errors = 0
    for filepath in files:
        errors = validate_file(filepath)
        if errors:
            for lineno, namespace, name in errors:
                print(f"ERROR {filepath}:{lineno} - {namespace}.{name} is not a valid constant")
                # Suggest closest match
                valid_set = NAMESPACES[namespace]
                for valid_name in sorted(valid_set):
                    if valid_name.lower().startswith(name[:3].lower()):
                        print(f"  Did you mean {namespace}.{valid_name}?")
            total_errors += len(errors)
        else:
            print(f"OK    {filepath}")

    print()
    if total_errors:
        print(f"FAILED: {total_errors} error(s) found")
        sys.exit(1)
    else:
        print("ALL PASSED")


if __name__ == "__main__":
    main()
