from abilities.wizard_abilities import Polymorph, ManaBurst, MagicMissile, Fireball, HealWounds
from abilities.paladin_abilities import AuraOfProtection, DivineSmite, LayOnHands, OathOfDevotion, ShieldOfFaith
from abilities.cleric_abilities import  BlessingOfProtection, DamageAbility, DivineIntervention,  DivineSmite, HealingWord, TurnUndead
from abilities.warrior_abilities import ActionSurge,  SecondWind, Indomitable
from abilities.rogue_abilities  import DisarmTrap, Evasion, UncannyDodge, SneakAttack 

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