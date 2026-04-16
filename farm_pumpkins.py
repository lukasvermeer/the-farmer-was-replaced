# Pumpkin farming script
# Strategy: grow one massive mega pumpkin across the entire field
# Yield = n^2 * 6 = 32^2 * 6 = 6144 per harvest
# Optimizations:
# - Serpentine scan (zigzag) to exploit wrap-around movement
# - Track dead pumpkins in a list, only revisit those

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

def plant_and_grow_all():
	# Serpentine scan: go east on even rows, west on odd rows
	# Returns list of (x, y) positions that need replanting
	size = get_world_size()
	broken = list()
	for y in range(size):
		if y % 2 == 0:
			for x in range(size):
				go_to(x, y)
				handle_tile(x, y, broken)
		else:
			for x in range(size - 1, -1, -1):
				go_to(x, y)
				handle_tile(x, y, broken)
	return broken

def handle_tile(x, y, broken):
	# Plant if needed, water + fertilize, track if not ready
	if get_entity_type() != Entities.Pumpkin:
		plant(Entities.Pumpkin)
	if not can_harvest():
		if get_water() < 0.75:
			use_item(Items.Water)
		use_item(Items.Fertilizer)
		# If still not ready after fertilizer, it might be freshly planted
		# or dead -- either way we need to come back
		if not can_harvest():
			broken.append((x, y))

def fix_broken(broken):
	# Visit only the broken positions, replant and fertilize
	# Returns new list of still-broken positions
	still_broken = list()
	for pos in broken:
		go_to(pos[0], pos[1])
		if get_entity_type() != Entities.Pumpkin:
			plant(Entities.Pumpkin)
		elif not can_harvest():
			# Dead -- replant over it
			plant(Entities.Pumpkin)
		if not can_harvest():
			if get_water() < 0.75:
				use_item(Items.Water)
			use_item(Items.Fertilizer)
			if not can_harvest():
				still_broken.append(pos)
	return still_broken

# Main loop
prepare_soil()
while True:
	broken = plant_and_grow_all()
	while len(broken) > 0:
		broken = fix_broken(broken)
	# All 1024 pumpkins ready -- harvest the mega pumpkin
	harvest()
