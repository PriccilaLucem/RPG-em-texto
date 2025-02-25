from models.abilities_model import DamageAbility, HealAbility

natures_wrath = DamageAbility(name="Nature's Wrath",damage= 40, description= "Entangles the enemy with vines", cooldown= 3, level=2),
healing_aura = HealAbility(name= "Healing Aura", cooldown=5, description = "Restores health to allies", effect_value=30 ,level= 2)
 