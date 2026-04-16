# Pumpkin farming script
# Strategy: grow 6x6 mega pumpkins for max yield (n^2 * 6 = 216 per harvest)
# Uses fertilizer + water to speed growth, replants dead pumpkins
# Tiles the full 32x32 grid with 25 patches of 6x6

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

def prepare_soil(px, py, size):
	for y in range(size):
		for x in range(size):
			go_to(px + x, py + y)
			if get_ground_type() != Grounds.Soil:
				till()

def plant_and_grow(px, py, size):
	# Plant pumpkins, water, and fertilize in one pass
	for y in range(size):
		for x in range(size):
			go_to(px + x, py + y)
			entity = get_entity_type()
			if entity != Entities.Pumpkin:
				plant(Entities.Pumpkin)
			# Water + fertilize to insta-grow
			# Max growth time 3.8s, fertilizer gives 2s * (1 + water*4)
			# At water 0.75: 2s * 4 = 8s effective -- one dose is enough
			if not can_harvest():
				if get_water() < 0.75:
					use_item(Items.Water_Tank)
				use_item(Items.Fertilizer)

def all_harvestable(px, py, size):
	# Check if all tiles have harvestable pumpkins
	# Also replant dead ones (pumpkin entity but not harvestable 
	# after fertilization means dead)
	all_ready = True
	for y in range(size):
		for x in range(size):
			go_to(px + x, py + y)
			if get_entity_type() != Entities.Pumpkin:
				# Empty or wrong entity
				plant(Entities.Pumpkin)
				all_ready = False
			elif not can_harvest():
				# Dead or still growing -- replant to be safe
				# (planting on dead pumpkin replaces it)
				plant(Entities.Pumpkin)
				all_ready = False
	return all_ready

def farm_patch(px, py, size):
	prepare_soil(px, py, size)
	
	# Plant + fertilize, then check. Repeat until all 36 alive.
	planted = False
	while not planted:
		plant_and_grow(px, py, size)
		planted = all_harvestable(px, py, size)
	
	# Harvest the mega pumpkin
	go_to(px, py)
	harvest()

# Main loop: farm 25 patches of 6x6 across the 32x32 grid
patch_size = 6
# Only prepare soil once on first run
first_run = True
while True:
	for py in range(0, 30, patch_size):
		for px in range(0, 30, patch_size):
			if first_run:
				farm_patch(px, py, patch_size)
			else:
				# Soil is already tilled, skip prepare_soil
				planted = False
				while not planted:
					plant_and_grow(px, py, patch_size)
					planted = all_harvestable(px, py, patch_size)
				go_to(px, py)
				harvest()
	first_run = False
