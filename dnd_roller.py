# Inputs - find a way to only ask this at first or ask if a new character is desired at the end.

strength, dex, constitution, intelligence, wisdom, charisma = input("Current Ability Scores (str, dex, con, int, wis, cha): ").split(',')

lvl_input = input("Current Level: ")
character_lvl = int(lvl_input)

skill_profs = input("Current Skill Proficiencies: ")

roll = input("Roll for: ")


prof_bonus = 2
if character_lvl >= 5:
    prof_bonus = 3
if character_lvl >= 9:
    prof_bonus = 4

# character = input("Use Previously Created Character or Use New Character? (Previous/New): ")
   # if character == "Previous":
   #     print(sum(strength), sum(dex), sum(constitution), sum(intelligence), sum(wisdom), sum(charisma))

   # if character == "New":
   #     input("Input Character Ability Stats (str, dex, con, int, wis, cha): ")

    
# ability_modifier = ()