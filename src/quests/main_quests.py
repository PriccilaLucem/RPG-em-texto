from enums.rarity_enum import Rarity_Enum
from models.quests import Quests, DeliverQuestsItems, CollectableQuest
from models.item_model import ItemModel
from resources.ores import iron_ore

deliver_sword_to_damon =  DeliverQuestsItems(-1, 1, 10, 10, "Deliver sword to Damon",  ItemModel("Regular sword", 0, Rarity_Enum.COMMON, 0, False))
prismeer_owl_bear_quest = Quests(id=-2,difficult_stars=4,xp_given=100,gold_given=85, mission="Help the brothes of Damon in OwBear cave!")
prismeer_blacksmith_quest = CollectableQuest(id=-3, difficult_stars=1, xp_given=20, gold_given=50, mission="Collect some iron ores to Walver the blacksmith!",
                                              items_to_be_collected=[(iron_ore, 3)])
