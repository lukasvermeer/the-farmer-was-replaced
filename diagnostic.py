# Diagnostic script to figure out current game state
# Run this and share the output so we know where we're at

def diagnose():
	# Check farm size
	size = get_world_size()
	quick_print("=== FARM STATE ===")
	quick_print("Farm size: " + size)
	
	# Check drone position
	quick_print("Drone pos: (" + get_pos_x() + ", " + get_pos_y() + ")")
	
	# Scan the full grid: entities and ground types
	quick_print("")
	quick_print("=== GRID SCAN ===")
	for y in range(size):
		for x in range(size):
			entity = get_entity_type()
			ground = get_ground_type()
			water = get_water()
			quick_print("(" + x + "," + y + ") entity=" + entity + " ground=" + ground + " water=" + water)
			if x < size - 1:
				move(East)
		for x in range(size - 1):
			move(West)
		if y < size - 1:
			move(North)
	
	# Move back to origin
	for y in range(size - 1):
		move(South)
	
	# Check unlocks
	quick_print("")
	quick_print("=== UNLOCKS ===")
	quick_print("Speed: " + num_unlocked(Unlocks.Speed))
	quick_print("Expand: " + num_unlocked(Unlocks.Expand))
	quick_print("Plant: " + num_unlocked(Unlocks.Plant))
	quick_print("Grass: " + num_unlocked(Unlocks.Grass))
	quick_print("Trees: " + num_unlocked(Unlocks.Trees))
	quick_print("Carrots: " + num_unlocked(Unlocks.Carrots))
	quick_print("Pumpkins: " + num_unlocked(Unlocks.Pumpkins))
	quick_print("Sunflowers: " + num_unlocked(Unlocks.Sunflowers))
	quick_print("Cactus: " + num_unlocked(Unlocks.Cactus))
	quick_print("Dinosaurs: " + num_unlocked(Unlocks.Dinosaurs))
	quick_print("Mazes: " + num_unlocked(Unlocks.Mazes))
	quick_print("Polyculture: " + num_unlocked(Unlocks.Polyculture))
	quick_print("Fertilizer: " + num_unlocked(Unlocks.Fertilizer))
	quick_print("Watering: " + num_unlocked(Unlocks.Watering))
	quick_print("Senses: " + num_unlocked(Unlocks.Senses))
	quick_print("Operators: " + num_unlocked(Unlocks.Operators))
	quick_print("Variables: " + num_unlocked(Unlocks.Variables))
	quick_print("Functions: " + num_unlocked(Unlocks.Functions))
	quick_print("Lists: " + num_unlocked(Unlocks.Lists))
	quick_print("Dictionaries: " + num_unlocked(Unlocks.Dictionaries))
	quick_print("Loops: " + num_unlocked(Unlocks.Loops))
	quick_print("Conditions: " + num_unlocked(Unlocks.Conditions))
	quick_print("Debug: " + num_unlocked(Unlocks.Debug))
	quick_print("Benchmark: " + num_unlocked(Unlocks.Benchmark))
	quick_print("Costs: " + num_unlocked(Unlocks.Costs))
	quick_print("Auto_Unlock: " + num_unlocked(Unlocks.Auto_Unlock))
	quick_print("Multi_Trade: " + num_unlocked(Unlocks.Multi_Trade))
	quick_print("Leaderboard: " + num_unlocked(Unlocks.Leaderboard))
	
	# Check inventory
	quick_print("")
	quick_print("=== INVENTORY ===")
	quick_print("Hay: " + num_items(Items.Hay))
	quick_print("Wood: " + num_items(Items.Wood))
	quick_print("Carrot: " + num_items(Items.Carrot))
	quick_print("Carrot_Seed: " + num_items(Items.Carrot_Seed))
	quick_print("Pumpkin: " + num_items(Items.Pumpkin))
	quick_print("Pumpkin_Seed: " + num_items(Items.Pumpkin_Seed))
	quick_print("Sunflower_Seed: " + num_items(Items.Sunflower_Seed))
	quick_print("Power: " + num_items(Items.Power))
	quick_print("Water_Tank: " + num_items(Items.Water_Tank))
	quick_print("Fertilizer: " + num_items(Items.Fertilizer))
	quick_print("Egg: " + num_items(Items.Egg))
	quick_print("Cactus: " + num_items(Items.Cactus))
	quick_print("Cactus_Seed: " + num_items(Items.Cactus_Seed))
	quick_print("Bone: " + num_items(Items.Bone))
	quick_print("Gold: " + num_items(Items.Gold))
	
	quick_print("")
	quick_print("=== DONE ===")

diagnose()
