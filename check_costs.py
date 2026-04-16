# Check what pumpkin seeds actually cost at current upgrade level
cost = get_cost(Entities.Pumpkin)
quick_print("Pumpkin plant cost:", cost)
cost2 = get_cost(Entities.Carrot)
quick_print("Carrot plant cost:", cost2)
quick_print("Current carrots:", num_items(Items.Carrot))
