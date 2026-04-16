# Pumpkin farming script
# Strategy: grow one massive mega pumpkin across the entire field
# Yield = n^2 * 6 = 32^2 * 6 = 6144 per harvest
# Optimizations:
# - Serpentine scan (zigzag) to exploit wrap-around movement
# - Track dead pumpkins in a list, only revisit those
# - Handles restart with existing pumpkins already on the field
# - Auto-farms carrots when running low

# Each pumpkin costs 512 carrots to plant at upgrade level 10
# 1024 tiles = 524,288 carrots per full plant
# ~20% death rate means ~1.3x replants, so ~680K per cycle
# Keep a buffer above that
CARROT_THRESHOLD = 750000

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

# --- Carrot farming ---

def plant_carrot_tile():
	if get_ground_type() != Grounds.Soil:
		till()
	entity = get_entity_type()
	if entity != Entities.Carrot:
		if entity != None:
			harvest()
		plant(Entities.Carrot)
	if not can_harvest():
		if get_water() < 0.75:
			use_item(Items.Water)
		# Carrots take 4.8-7.2s, fertilizer gives 2s * water multiplier
		# At 0.75 water: 2s * 4 = 8s per dose, so one dose might not be enough
		use_item(Items.Fertilizer)
		use_item(Items.Fertilizer)

def harvest_carrot_tile():
	if can_harvest():
		harvest()

def farm_carrots():
	size = get_world_size()
	while num_items(Items.Carrot) < CARROT_THRESHOLD:
		# Plant and fertilize pass
		for y in range(size):
			if y % 2 == 0:
				for x in range(size):
					go_to(x, y)
					plant_carrot_tile()
			else:
				for x in range(size - 1, -1, -1):
					go_to(x, y)
					plant_carrot_tile()
		# Harvest pass
		for y in range(size):
			if y % 2 == 0:
				for x in range(size):
					go_to(x, y)
					harvest_carrot_tile()
			else:
				for x in range(size - 1, -1, -1):
					go_to(x, y)
					harvest_carrot_tile()

# --- Pumpkin farming ---

def handle_pumpkin_tile(x, y, broken):
	if get_ground_type() != Grounds.Soil:
		till()
	entity = get_entity_type()
	if entity != Entities.Pumpkin:
		if entity != None:
			harvest()
		plant(Entities.Pumpkin)
	if can_harvest():
		return
	if get_water() < 0.75:
		use_item(Items.Water)
	use_item(Items.Fertilizer)
	if not can_harvest():
		broken.append((x, y))

def plant_and_grow_all():
	size = get_world_size()
	broken = list()
	for y in range(size):
		if y % 2 == 0:
			for x in range(size):
				go_to(x, y)
				handle_pumpkin_tile(x, y, broken)
		else:
			for x in range(size - 1, -1, -1):
				go_to(x, y)
				handle_pumpkin_tile(x, y, broken)
	return broken

def fix_broken(broken):
	still_broken = list()
	for pos in broken:
		go_to(pos[0], pos[1])
		if get_entity_type() != Entities.Pumpkin:
			plant(Entities.Pumpkin)
		elif not can_harvest():
			plant(Entities.Pumpkin)
		if not can_harvest():
			if get_water() < 0.75:
				use_item(Items.Water)
			use_item(Items.Fertilizer)
			if not can_harvest():
				still_broken.append(pos)
	return still_broken

# Main loop
while True:
	if num_items(Items.Carrot) < CARROT_THRESHOLD:
		farm_carrots()
	broken = plant_and_grow_all()
	while len(broken) > 0:
		broken = fix_broken(broken)
	harvest()
