# Maze solving script
# Strategy: wall follower (right-hand rule)
# - No loops in fresh mazes, so right-hand wall following is guaranteed to find treasure
# - Spawn full-field maze, follow right wall until we find treasure, harvest

# Directions indexed for rotation: North=0, East=1, South=2, West=3
directions = [North, East, South, West]

def turn_right(index):
	return (index + 1) % 4

def turn_left(index):
	return (index - 1) % 4

def create_maze():
	# Plant a bush and grow it into a maze
	# Clear field first
	clear()
	plant(Entities.Bush)
	# Amount of weird substance needed for full-field maze
	size = get_world_size()
	n = size * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, n)

def solve_maze():
	# Right-hand wall following
	# Start facing North
	facing = 0
	
	while get_entity_type() != Entities.Treasure:
		# Try to turn right and move
		right = turn_right(facing)
		if move(directions[right]):
			# Turned right and moved -- now facing right
			facing = right
		elif move(directions[facing]):
			# Couldn't turn right, but could go straight
			pass
		else:
			# Can't go right or straight, turn left
			left = turn_left(facing)
			if move(directions[left]):
				facing = left
			else:
				# Dead end, turn around
				facing = turn_left(left)
				move(directions[facing])
	
	# Found treasure, harvest it
	harvest()

# Main loop
while True:
	create_maze()
	solve_maze()
