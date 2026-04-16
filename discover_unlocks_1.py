# Discovery script - test questionable unlock constants
# Run this to find which of these exist. If it crashes, 
# tell me the error and I'll narrow it down.
#
# Batch 1: Auto_Unlock, Cactus, Costs, Debug_2
quick_print("Auto_Unlock: " + num_unlocked(Unlocks.Auto_Unlock))
quick_print("Cactus: " + num_unlocked(Unlocks.Cactus))
quick_print("Costs: " + num_unlocked(Unlocks.Costs))
quick_print("Debug_2: " + num_unlocked(Unlocks.Debug_2))
