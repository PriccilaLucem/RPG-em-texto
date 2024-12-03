def calculate_defense(weight, rarity, base=3, f1=2.0, f2=5.0):
    return base + (weight * f1) + (rarity * f2)
def calculate_attack(weight, rarity, crit_chance, base=5, f3=1.5, f4=3.0, f5=10.0):
    return base + (weight * f3) + (rarity * f4) + (crit_chance * f5)
