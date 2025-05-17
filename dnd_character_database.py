import random
import math
import sqlite3


class Character:
    def __init__(self, name, stats, level, proficiencies, expertise=None):
        self.name = name
        self.stats = {k: int(v) for k, v in zip(['str', 'dex', 'con', 'int', 'wis', 'cha'], stats)}
        self.modifiers = {k: math.floor((v - 10) / 2) for k, v in self.stats.items()}
        self.level = level
        self.proficient = proficiencies
        self.expertise = expertise or []
        self.proficiency_bonus = 2 + (level - 1) // 4


def add_character():
    conn = sqlite3.connect('characters.db')
    c = conn.cursor()

    #c.execute("""CREATE TABLE characters (
            #name text,
            #level integer,

            #strength integer,
            #dex integer,
            #constitution integer,
            #intelligence integer,
            #wisdom integer,
            #charisma integer,

            #proficiencies text,
            #expertise text
    #)""")

    character_name = input("Character Name: ")

    character_level = int(input("Character Level (value): "))


    character_stats = input("Character Stats (str, dex, con, int, wis, cha): ")
    abilities = character_stats.replace(' ', '').split(',')
    str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat = map(int, abilities)


    proficiencies_input = input("Skill Proficiencies (comma separated): ")
    proficiencies = [skill.strip().lower() for skill in proficiencies_input.split(',')]

    expertise_input = input("Expertise Skills (comma separated, optional): ")
    expertise = [skill.strip().lower() for skill in expertise_input.split(',') if skill.strip()]

    proficiencies_str = ','.join(proficiencies)
    expertise_str = ','.join(expertise)


    my_character = Character(
        name=character_name,
        stats=[str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat],
        level=character_level,
        proficiencies=proficiencies_str,
        expertise=expertise_str
    )


    add_to_db = input("Add to Database? (Y/N): ")
    if add_to_db.upper() == "Y":
        c.execute("""INSERT INTO characters (
            name, level, strength, dex, constitution, intelligence, wisdom, charisma, proficiencies, expertise
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (character_name, character_level, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, proficiencies_str, expertise_str))

        conn.commit()
        print(f"{character_name} saved to database.")
    else:
        print("Character not saved.")

    conn.close()
    return my_character


created_character = add_character()
print(f"Created Character: {created_character.name} (Level {created_character.level})")






#def athletics():
    
    #check = [random.randint(1, 20)] + self.modifers

    #if proficiencies == "Athletics":
        #final_score = check + prof_bonus
    #else:
        #final_score = check

    #print("{my_character} makes an Athletics Check: {check} + {prof_bonus} = {final score}")
    #print(final_score)

#print(athletics())