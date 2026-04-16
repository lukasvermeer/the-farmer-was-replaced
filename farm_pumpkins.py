# Pumpkin farming script
# Strategy: grow one massive mega pumpkin across the entire field
# Yield = n^2 * 6 = 32^2 * 6 = 6144 per harvest

def go_to(tx, ty):
	cx = get_pos_x()
	cy = get_pos_y()
	dx = tx - cx
	if dx > 0:
		for i in range(dx):
			move(East)
	elif dx < 0:
		for i in range(-dx):
			move(West)
	dy = ty - cy
	if dy > 0:
		for i in range(dy):
			move(North)
	elif dy < 0:
		for i in range(-dy):
			move(South)

def prepare_soil():
	size = get_world_size()
	for y in range(size):
		for x in range(size):
			go_to(x, y)
			if get_ground_type() != Grounds.Soil:
				till()

def plant_and_grow():
	# Plant pumpkins on empty tiles, water + fertilize non-ready ones
	size = get_world_size()
	for y in range(size):
		for x in range(size):
			go_to(x, y)
			if get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
			if not can_harvest():
				if get_water() < 0.75:
					use_item(Items.Water)
				use_item(Items.Fertilizer)

def check_and_replant():
	# Returns True if all tiles are harvestable pumpkins
	# Replants any dead/missing ones
	size = get_world_size()
	all_ready = True
	for y in range(size):
		for x in range(size):
			go_to(x, y)
			if get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
				all_ready = False
			elif not can_harvest():
				# Dead pumpkin -- replant over it
				plant(Entities.Pumpkin)
				all_ready = False
	return all_ready

# Main loop
prepare_soil()
while True:
	# Plant and fertilize everything
	plant_and_grow()
	# Keep replanting dead ones until all 1024 are ready
	while not check_and_replant():
		plant_and_grow()
	# Harvest the mega pumpkin
	harvest()
