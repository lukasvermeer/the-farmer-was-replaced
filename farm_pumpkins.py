# Pumpkin farming script
# Strategy: grow one massive mega pumpkin across the entire field
# Yield = n^2 * 6 = 32^2 * 6 = 6144 per harvest
# Optimizations:
# - Serpentine scan (zigzag) to exploit wrap-around movement
# - Track dead pumpkins in a list, only revisit those
# - Handles restart with existing pumpkins already on the field
# - Auto-farms carrots with polyculture (10x yield) when running low
# - Auto-farms sunflowers to maintain power (2x drone speed)

# Each pumpkin costs 512 carrots to plant at upgrade level 10
# 1024 tiles = 524,288 carrots per full plant
# ~20% death rate means ~1.3x replants, so ~680K per cycle
# Keep a buffer above that
CARROT_THRESHOLD = 750000
POWER_THRESHOLD = 1000

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

def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()

# --- Sunflower farming for power ---

def farm_sunflowers():
	# Plant sunflowers on whole field, grow them, harvest the one
	# with max petals for power = sqrt(num_sunflowers)
	size = get_world_size()
	# Plant pass
	for y in range(size):
		if y % 2 == 0:
			for x in range(size):
				go_to(x, y)
				ensure_soil()
				entity = get_entity_type()
				if entity != Entities.Sunflower:
					if entity != None:
						harvest()
					plant(Entities.Sunflower)
				if not can_harvest():
					if get_water() < 0.75:
						use_item(Items.Water)
					use_item(Items.Fertilizer)
					use_item(Items.Fertilizer)
		else:
			for x in range(size - 1, -1, -1):
				go_to(x, y)
				ensure_soil()
				entity = get_entity_type()
				if entity != Entities.Sunflower:
					if entity != None:
						harvest()
					plant(Entities.Sunflower)
				if not can_harvest():
					if get_water() < 0.75:
						use_item(Items.Water)
					use_item(Items.Fertilizer)
					use_item(Items.Fertilizer)
	# Find the sunflower with the most petals and harvest it
	max_petals = 0
	max_x = 0
	max_y = 0
	for y in range(size):
		if y % 2 == 0:
			for x in range(size):
				go_to(x, y)
				if get_entity_type() == Entities.Sunflower:
					if can_harvest():
						p = measure()
						if p > max_petals:
							max_petals = p
							max_x = x
							max_y = y
		else:
			for x in range(size - 1, -1, -1):
				go_to(x, y)
				if get_entity_type() == Entities.Sunflower:
					if can_harvest():
						p = measure()
						if p > max_petals:
							max_petals = p
							max_x = x
							max_y = y
	if max_petals > 0:
		go_to(max_x, max_y)
		harvest()

# --- Carrot farming with polyculture ---

def farm_carrots():
	# Plant carrots one by one, place their companion for 10x yield,
	# then fertilize and harvest
	size = get_world_size()
	while num_items(Items.Carrot) < CARROT_THRESHOLD:
		for y in range(size):
			if y % 2 == 0:
				for x in range(size):
					go_to(x, y)
					grow_carrot_with_companion(x, y)
			else:
				for x in range(size - 1, -1, -1):
					go_to(x, y)
					grow_carrot_with_companion(x, y)
		# Harvest pass -- all should be ready after fertilizer
		for y in range(size):
			if y % 2 == 0:
				for x in range(size):
					go_to(x, y)
					if can_harvest():
						harvest()
			else:
				for x in range(size - 1, -1, -1):
					go_to(x, y)
					if can_harvest():
						harvest()

def grow_carrot_with_companion(x, y):
	ensure_soil()
	entity = get_entity_type()
	if entity != Entities.Carrot:
		if entity != None:
			harvest()
		plant(Entities.Carrot)
	# Place companion for polyculture 10x bonus
	comp = get_companion()
	if comp != None:
		comp_type = comp[0]
		comp_pos = comp[1]
		comp_x = comp_pos[0]
		comp_y = comp_pos[1]
		# Save position, go place companion, come back
		go_to(comp_x, comp_y)
		ensure_soil()
		# Only place if something different is there
		if get_entity_type() != comp_type:
			# Don't destroy another carrot we already planted
			if get_entity_type() == Entities.Carrot:
				# Skip -- don't overwrite our carrots
				pass
			else:
				if get_entity_type() != None:
					harvest()
				plant(comp_type)
		go_to(x, y)
	# Fertilize the carrot
	if not can_harvest():
		if get_water() < 0.75:
			use_item(Items.Water)
		use_item(Items.Fertilizer)
		use_item(Items.Fertilizer)

# --- Pumpkin farming ---

def handle_pumpkin_tile(x, y, broken):
	ensure_soil()
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
	# Top up power if low
	if num_items(Items.Power) < POWER_THRESHOLD:
		farm_sunflowers()
	# Top up carrots if low
	if num_items(Items.Carrot) < CARROT_THRESHOLD:
		farm_carrots()
	# Grow mega pumpkin
	broken = plant_and_grow_all()
	while len(broken) > 0:
		broken = fix_broken(broken)
	harvest()
