# Cactus farming script
# Strategy: plant full 32x32 grid, grow, sort, harvest for n^2 yield
# Sort approach: bubble sort rows (West->East), then columns (South->North)
# Yield: 1024^2 = 1,048,576 cactus per harvest cycle

def go_to(tx, ty):
	size = get_world_size()
	cx = get_pos_x()
	cy = get_pos_y()
	dx = (tx - cx) % size
	if dx > size / 2:
		for i in range(size - dx):
			move(West)
	else:
		for i in range(dx):
			move(East)
	dy = (ty - cy) % size
	if dy > size / 2:
		for i in range(size - dy):
			move(South)
	else:
		for i in range(dy):
			move(North)

def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()

def plant_and_grow_cacti():
	# Plant cacti on the whole field and fertilize to grow
	size = get_world_size()
	all_ready = False
	while not all_ready:
		all_ready = True
		for y in range(size):
			if y % 2 == 0:
				for x in range(size):
					go_to(x, y)
					ensure_soil()
					entity = get_entity_type()
					if entity != Entities.Cactus:
						if entity != None:
							harvest()
						plant(Entities.Cactus)
					if not can_harvest():
						all_ready = False
						use_item(Items.Fertilizer)
			else:
				for x in range(size - 1, -1, -1):
					go_to(x, y)
					ensure_soil()
					entity = get_entity_type()
					if entity != Entities.Cactus:
						if entity != None:
							harvest()
						plant(Entities.Cactus)
					if not can_harvest():
						all_ready = False
						use_item(Items.Fertilizer)

def sort_rows():
	# Cocktail shaker sort each row with shrinking bounds
	size = get_world_size()
	for y in range(size):
		lower = 0
		upper = size - 1
		while lower < upper:
			# Forward pass: bubble largest to upper bound
			new_upper = lower
			for x in range(lower, upper):
				go_to(x, y)
				if measure() > measure(East):
					swap(East)
					new_upper = x
			upper = new_upper
			# Backward pass: bubble smallest to lower bound
			new_lower = upper
			for x in range(upper, lower, -1):
				go_to(x, y)
				if measure() < measure(West):
					swap(West)
					new_lower = x
			lower = new_lower

def sort_columns():
	# Cocktail shaker sort each column with shrinking bounds
	size = get_world_size()
	for x in range(size):
		lower = 0
		upper = size - 1
		while lower < upper:
			# Forward pass: bubble largest to upper bound
			new_upper = lower
			for y in range(lower, upper):
				go_to(x, y)
				if measure() > measure(North):
					swap(North)
					new_upper = y
			upper = new_upper
			# Backward pass: bubble smallest to lower bound
			new_lower = upper
			for y in range(upper, lower, -1):
				go_to(x, y)
				if measure() < measure(South):
					swap(South)
					new_lower = y
			lower = new_lower

# Main loop
while True:
	plant_and_grow_cacti()
	sort_rows()
	sort_columns()
	# Harvest from bottom-left corner (smallest) to trigger chain
	go_to(0, 0)
	harvest()
