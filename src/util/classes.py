from abilities.wizard_abilities import Polymorph, ManaBurst, MagicMissile, Fireball, HealWounds
from abilities.paladin_abilities import AuraOfProtection, DivineSmite, LayOnHands, OathOfDevotion, ShieldOfFaith
from abilities.cleric_abilities import  BlessingOfProtection, DivineIntervention,  DivineSmite, HealingWord, TurnUndead
from abilities.warrior_abilities import ActionSurge,  SecondWind, Indomitable
from abilities.rogue_abilities  import DisarmTrap, Evasion, UncannyDodge, SneakAttack 
from models.item_model import HeavyArmor, LightArmor, Shield, Mace, LightShield,  HeavyShield, Axe, Bow, Crossbow, Club, Dagger, Spellbook, Wand, Sword
ABILITY_CLASSES = {
    # Rogue abilities
    DisarmTrap: DisarmTrap,
    Evasion: Evasion,
    SneakAttack: SneakAttack,
    UncannyDodge: UncannyDodge,
    
    # Wizard abilities
    Polymorph: Polymorph,
    ManaBurst: ManaBurst,
    MagicMissile: MagicMissile,
    Fireball: Fireball,
    HealWounds: HealWounds,
    
    # Paladin abilities
    AuraOfProtection: AuraOfProtection,
    DivineSmite: DivineSmite,
    LayOnHands: LayOnHands,
    OathOfDevotion: OathOfDevotion,
    ShieldOfFaith: ShieldOfFaith,
    
    # Cleric abilities
    BlessingOfProtection: BlessingOfProtection,
    DivineIntervention: DivineIntervention,
    HealingWord: HealingWord,
    TurnUndead: TurnUndead,
    
    # Warrior abilities
    ActionSurge: ActionSurge,
    SecondWind: SecondWind,
    Indomitable: Indomitable
}

ITEM_CLASSES = {
    # Armor Classes
    "HeavyArmor": HeavyArmor,
    "LightArmor": LightArmor,
    "Shield": Shield,
    "LightShield": LightShield,
    "HeavyShield": HeavyShield,
    
    # Weapon Classes
    "Sword": Sword,
    "Axe": Axe,
    "Bow": Bow,
    "Dagger": Dagger,
    "Mace": Mace,
    "Wand": Wand,
    "Crossbow": Crossbow,
    "Club": Club, 
    
    # Misc Classes
    "Spellbook": Spellbook
}