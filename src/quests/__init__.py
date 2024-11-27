import random
from typing import List
from quests.quests import Quests

def generate_random_quests(n: int = 5) -> List[Quests]:
    quest_data = [
        ("Retrieve the Ancient Artifact", "Journey deep into the ruins to retrieve a lost artifact."),
        ("Defeat the Bandit Leader", "The local bandits have been terrorizing travelers. Find and defeat their leader."),
        ("Rescue the Villagers", "A group of villagers has been kidnapped by goblins. Rescue them!"),
        ("Slay the Forest Troll", "A massive troll is rampaging through the forest. Stop it before it reaches the city."),
        ("Deliver the King's Message", "The King has entrusted you with delivering an important message to a neighboring realm."),
        ("Find the Lost Treasure", "An ancient treasure map has been discovered. Follow its clues to find the treasure."),
        ("Investigate the Haunted Mansion", "Strange events have been reported at the old mansion. Investigate and find the truth."),
        ("Stop the Necromancer's Ritual", "A necromancer is attempting to raise an army of undead. Stop the ritual before it's too late."),
        ("Escort the Merchant Caravan", "A merchant caravan is being threatened by highwaymen. Escort them to safety."),
        ("Defend the Village from Goblins", "A goblin horde is attacking a nearby village. Defend the villagers and drive them out."),
        ("Rescue the Princess", "The princess has been kidnapped by a dragon. Rescue her from the dragon's lair."),
        ("Protect the Sacred Grove", "The sacred grove is under threat from evil forces. Defend it at all costs."),
        ("Gather Rare Herbs for the Healer", "The local healer needs rare herbs to make a powerful potion. Collect them in the wild."),
        ("Recover the Stolen Artifact", "An ancient artifact has been stolen. Track down the thief and recover it."),
        ("Investigate the Disappearance of the Scouts", "A group of scouts has gone missing. Find them and uncover what happened."),
        ("Uncover the Secret of the Sunken Temple", "A mysterious sunken temple has been discovered. Explore it and uncover its secrets.")
    ]

    # Shuffle the quest data to ensure randomness
    random.shuffle(quest_data)

    quests = []
    for _ in range(min(n, len(quest_data))):  
        title, description = quest_data.pop() 
        difficulty = random.randint(1, 3)
        reward = difficulty * random.randint(10, 20)  
        xp_given = difficulty * random.randint(20, 50)
        quests.append(Quests(None, difficulty, xp_given, reward, f"{title}: {description}"))

    return quests
