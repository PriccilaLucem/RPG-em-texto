from enums.rarity_enum import Rarity_Enum
from models.quests import Quests, DeliverQuestsItems, CollectableQuest
from models.item_model import ItemModel
from resources.ores import iron_ore

deliver_sword_to_damon = DeliverQuestsItems(
    id=-1,
    difficult_stars=1,
    xp_given=10,
    gold_given=10,
    mission="Deliver sword to Damon",
    description="The guard captain Damon needs this sword urgently to fend off",
    additional_info={
        "location": "Prismeer after crossroads",
    },
    item_to_be_delivered=ItemModel(
        "Regular sword", 
        0, 
        Rarity_Enum.COMMON, 
        0, 
        False
    )
)

prismeer_owl_bear_quest = Quests(
    id=-2,
    difficult_stars=10,
    xp_given=300,
    gold_given=85,
    mission="Help the brothers of Damon in Owlbear cave!",
    description="The desperate brothers of the Damon clan ventured into the \n" +
                "They were mining and have been surrounded by an OwlBear",
    additional_info={
        "location": "Iron mine Cave",
        "historical_note": "The caverns were discovered long time ago by the North empire",
        "Warning": "Do not go alone"
    }
)

prismeer_blacksmith_quest = CollectableQuest(
    id=-3,
    difficult_stars=1,
    xp_given=20,
    gold_given=50,
    mission="Collect some iron ores for Walver the blacksmith!",
    description="The gruff but kind-hearted blacksmith Walver needs quality \n" +
                "iron ore to repair the village's farming tools before \n" +
                "harvest season. Mine fresh ore from the nearby cliffs", 
    additional_info={
        "best_locations": [
            "Iron mine Cave",
        ],
        "Warning": "They said it might be dangerous",
        "hidden_bonus": "Gold ores give an extra reward",
        "blacksmith_note": "I'll throw in a sharpening stone for good ore!"
    },
    items_to_be_collected=[(iron_ore, 3)]
)