from models.npc_model import Character_model, Character_with_a_quest_model  
from models.quests import Quests
from util.id_generator import IDGenerator
drunkard = Character_model(
    name="Old Tom",
    speeches=[
        "*hic* Buy an old man a drink?",
        "I 'member when this place was just two barrels an' a plank...",
        "Don' lissen to Bessie, she's always lyin'",
        "*snore*"
    ]
)

barmaid = Character_model(
    name="Bessie",
    speeches=[
        "What'll it be, love?",
        "Old Tom? Pay him no mind, the drunkard.",
        "We've got ale, wine, and some questionable stew.",
        "Last call! Unless you tip well..."
    ]
)

mercenary = Character_model(
    name="One-Eyed Jack",
    speeches=[
        "I didn't get this eye patch from knitting.",
        "Keep your distance unless you're buying.",
        "The war? Aye, I was there. Wish I wasn't.",
        "*sharpens dagger aggressively*"
    ]
)

guard = Character_model(
    name="Captain Aldric",
    speeches=[
        "Halt! State your business.",
        "Keep your weapons sheathed in town.",
        "Move along, citizen."
    ]
)

stranger = Character_model(
    name="Hooded Figure",
    speeches=[
        "...",
        "You shouldn't talk to me.",
        "The less you know, the safer you are.",
        "*keeps face hidden*"
    ]
)

shady_dealer = Character_with_a_quest_model(
    name="Ratface Eddie",
    speeches=[
        "Psst... hey kid... you look like someone who knows their way around a problem...",
        "My basement's got a bit of a... pest situation. You handle that sorta thing?",
        "What? No, those white powders? Just flour for my... baking business.",
        "You didn't see nothin', capisce?",
        "*nervously scratches arm*"
    ],
    quest=Quests(
        id= IDGenerator.generate_id(),
        mission="Exterminate Eddie's 'Pests'",
        description="Clear out the giant rats in Eddie's basement. He insists they're normal rats. They're not.",
        gold_given=120,
        difficult_stars=3,
        xp_given=150,
        additional_info={
            "location": "The backroom of 'Eddie's Pharmaceutical Supplies'",
            "special_condition": "Don't ask what the rats have been eating",
            "rumors": "Some say Eddie's 'special flour' made the rats grow..."
        }
    )
)

