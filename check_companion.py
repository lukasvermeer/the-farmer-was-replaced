# Check what get_companion actually returns

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

go_to(0, 0)
if get_ground_type() != Grounds.Soil:
	till()
if get_entity_type() != None:
	harvest()
plant(Entities.Carrot)
comp = get_companion()
quick_print("companion raw:", comp)
quick_print("len:", len(comp))
quick_print("elem 0:", comp[0])
quick_print("elem 1:", comp[1])
