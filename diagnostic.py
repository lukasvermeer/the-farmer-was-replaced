# Diagnostic script to figure out current game state
# Run this and share the output so we know where we're at
#
# NOTE: Only uses constants confirmed to exist in-game.
# If this fails to compile, report the error and we'll fix it.

def diagnose():
	size = get_world_size()
	quick_print("=== FARM STATE ===")
	quick_print("Farm size:", size)
	quick_print("Drone pos:", get_pos_x(), get_pos_y())
	
	# Scan the full grid
	quick_print("")
	quick_print("=== GRID SCAN ===")
	for y in range(size):
		for x in range(size):
			entity = get_entity_type()
			ground = get_ground_type()
			water = get_water()
			quick_print(x, y, "entity:", entity, "ground:", ground, "water:", water)
			if x < size - 1:
				move(East)
		for x in range(size - 1):
			move(West)
		if y < size - 1:
			move(North)
	
	# Move back to origin
	for y in range(size - 1):
		move(South)
	
	# Check unlocks - only confirmed valid constants
	quick_print("")
	quick_print("=== UNLOCKS ===")
	quick_print("Carrots:", num_unlocked(Unlocks.Carrots))
	quick_print("Debug:", num_unlocked(Unlocks.Debug))
	quick_print("Expand:", num_unlocked(Unlocks.Expand))
	quick_print("Fertilizer:", num_unlocked(Unlocks.Fertilizer))
	quick_print("Functions:", num_unlocked(Unlocks.Functions))
	quick_print("Grass:", num_unlocked(Unlocks.Grass))
	quick_print("Lists:", num_unlocked(Unlocks.Lists))
	quick_print("Loops:", num_unlocked(Unlocks.Loops))
	quick_print("Operators:", num_unlocked(Unlocks.Operators))
	quick_print("Plant:", num_unlocked(Unlocks.Plant))
	quick_print("Senses:", num_unlocked(Unlocks.Senses))
	quick_print("Speed:", num_unlocked(Unlocks.Speed))
	quick_print("Trees:", num_unlocked(Unlocks.Trees))
	quick_print("Variables:", num_unlocked(Unlocks.Variables))
	quick_print("Watering:", num_unlocked(Unlocks.Watering))
	
	# Check inventory - only confirmed valid constants
	quick_print("")
	quick_print("=== INVENTORY ===")
	quick_print("Hay:", num_items(Items.Hay))
	quick_print("Wood:", num_items(Items.Wood))
	quick_print("Carrot:", num_items(Items.Carrot))
	quick_print("Pumpkin:", num_items(Items.Pumpkin))
	quick_print("Power:", num_items(Items.Power))
	quick_print("Gold:", num_items(Items.Gold))
	
	quick_print("")
	quick_print("=== DONE ===")

diagnose()
