# Check polyculture and sunflower status

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

quick_print("Polyculture:", num_unlocked(Unlocks.Polyculture))
quick_print("Sunflowers:", num_unlocked(Unlocks.Sunflowers))
quick_print("Power:", num_items(Items.Power))
quick_print("Sunflower seed cost:", get_cost(Entities.Sunflower))

# Test get_companion on a carrot
go_to(0, 0)
if get_ground_type() != Grounds.Soil:
	till()
plant(Entities.Carrot)
comp = get_companion()
quick_print("Carrot companion:", comp)
