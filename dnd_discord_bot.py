import os
import discord
from discord.ext import commands
from dnd_bot_config import TOKEN
import dnd_character_creator
import sqlite3
import math
import json
import random
import ast

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

last_generated_character = {}

@bot.event
async def on_ready():
    print("Emilie's DnD Character Creator has arrived!")

@bot.command(name = 'random')
async def new_character(ctx):
    result = dnd_character_creator.play()

    last_generated_character[ctx.author.id] = result

    print(f"DEBUG - result: {repr(result)}")

    if result and result.strip():
        await ctx.send(result)

    else:
        await ctx.send("Oops! Something went wrong — character could not be created.")

@bot.command(name = 'add')
async def save_character(ctx, type: str = None):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    character_subrace = None 
    character_god = None

    add_types = ["random", "custom", "sheet"]

    if type is None:
        await ctx.send("Sorry, that isn't a valid input. Please use 'Custom' to add by custom inputs, 'Random' to add by the built in randomizer, or 'Sheet' to add by google sheet. If you need the empty sheet, type **!sheet**")
        return

    type = type.lower()

    if type not in add_types:
        await ctx.send("Sorry, that isn't a valid input. Please use 'Custom' to add by custom inputs, 'Random' to add by the built in randomizer, or 'Sheet' to add by google sheet. If you need the empty sheet, type **!sheet**")
        return

    if type == 'random':
        character = last_generated_character.get(ctx.author.id)
        if not character:
            await ctx.send("You haven't rolled a randomized character yet. Use **!random** to do so!")
            return

        await ctx.send("Enter Character Name")
        name_msg = await bot.wait_for('message', check=check, timeout=60)
        name = name_msg.content

        if name_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Character Level")
        level_msg = await bot.wait_for('message', check=check, timeout=60)
        level = int(level_msg.content)

        if level_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        race = character['character_race']
        subrace = character['character_subrace']
        character_class = character['character_class']
        subclass = character['character_subclass']
        strength = character['strength']
        dex = character['dex']
        constitution = character['constitution']
        intelligence = character['intelligence']
        wisdom = character['wisdom']
        charisma = character['charisma']
        background = character['character_background']
        proficiencies = character['skill_proficiency']
        expertise = character['skill_expertise']


        conn = sqlite3.connect('dnd_characters.db')
        c = conn.cursor()

        c.execute("""INSERT INTO characters (
            name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, expertise
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background,
        json.dumps(proficiencies), json.dumps(expertise)))

        conn.commit()
        conn.close()

        await ctx.send(f"**{name}** added to database")

    elif type == 'custom':

        await ctx.send("Enter Character Name")
        name_msg = await bot.wait_for('message', check=check, timeout=60)
        name = name_msg.content

        if name_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Character Level")
        level_msg = await bot.wait_for('message', check=check, timeout=60)
        level = int(level_msg.content)

        if level_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Character Race and Subrace")
        race_msg = await bot.wait_for('message', check=check, timeout=60)
        try:
            race, subrace = map(str.strip, race_msg.content.split(', ', 1))
        except ValueError:
            await ctx.send("Please use the format: Race, Subrace (e.g., 'Half-Elf, Wood Elf')")
            return

        if race_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Character Class and Subclass")
        classes_msg = await bot.wait_for('message', check=check, timeout=60)
        try:
            character_class, character_subclass = map(str.strip, classes_msg.content.split(', ', 1))
        except ValueError:
            await ctx.send("Please use the format: Class, Subclass (e.g., 'Wizard, Bladesinger')")
            return

        if classes_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Character Stats (str, dex, con, int, wis, cha): ")
        stats_msg = await bot.wait_for('message', check=check, timeout=60)
        stats = list(map(int, stats_msg.content.replace(' ', '').split(',')))
        str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat = stats

        if stats_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Character Background")
        background_msg = await bot.wait_for('message', check=check, timeout=60)
        background = background_msg.content

        if background_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Skill proficiencies (comma-separated): ")
        prof_msg = await bot.wait_for('message', check=check, timeout=60)
        proficiencies = [s.strip().lower() for s in prof_msg.content.split(',')]

        if prof_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Enter Expertise (comma-separated, optional): ")
        exp_msg = await bot.wait_for('message', check=check, timeout=60)
        expertise = [s.strip().lower() for s in exp_msg.content.split(',') if s.strip()]

        if exp_msg.content.lower() == 'quit':
            await ctx.send("Database Entry Cancelled")
            return

        await ctx.send("Save to database? (Y/N): ")
        confirm_msg = await bot.wait_for('message', check=check, timeout=60)
        if confirm_msg.content.upper() != 'Y':
            await ctx.send("Character creation cancelled")
            return

        conn = sqlite3.connect('dnd_characters.db')
        c = conn.cursor()

        c.execute("""INSERT INTO characters (
            name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, expertise
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, level, race, subrace, character_class, character_subclass, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, background,
        json.dumps(proficiencies), json.dumps(expertise)))

        conn.commit()
        conn.close()

        await ctx.send(f"**{name}** added to database")

    else:
        await ctx.send("Sorry, that isn't a valid input. Please use 'Custom' to add by custom inputs, 'Random' to add by the built in randomizer, or 'Sheet' to add by google sheet. If you need the empty sheet, type **!sheet**")
        return

@bot.command(name = 'database')
async def database(ctx, *, character_name):

    def fetch_character(character_name):
        conn = sqlite3.connect("dnd_characters.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, expertise
            FROM characters 
            WHERE name = ?
        """, (character_name,))
        row = cursor.fetchone()
        conn.close()
        return row

    character = fetch_character(character_name)

    if not character:
        await ctx.send(f"{ctx.author.mention}, no character registered under that name, please use *!add* to add your character!")
        return

    name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, expertise = character


    def format_skills(skills):
        if not skills:
            return "None"
        
        try:
            parsed = ast.literal_eval(skills)
            if isinstance(parsed, list):
                return ', '.join(skill.title().strip() for skill in parsed)
        except (ValueError, SyntaxError):
            pass

        return ', '.join(skill.title().strip() for skill in skills.split(','))

    embed = discord.Embed(
        title=f"{name}'s Character Sheet",
        description=f"**Level {level}**",
        color=discord.Color.random()
    )

    embed.add_field(
        name="Race",
        value = f"{subrace} {race}",
        inline=False
    )

    embed.add_field(
        name = "Class",
        value = f"{subclass} {character_class}",
        inline = False
    )

    embed.add_field(
        name="Abilities",
        value=f"**STR**: {strength}  |  **DEX**: {dex}  |  **CON**: {constitution}\n"
              f"**INT**: {intelligence}  |  **WIS**: {wisdom}  |  **CHA**: {charisma}",
        inline=False
    )

    embed.add_field(
        name="Background",
        value=(background),
        inline=True
    )

    embed.add_field(
        name="Skill Proficiencies",
        value=format_skills(proficiencies) or "None",
        inline=False
    )

    embed.add_field(
        name="Skill Expertise",
        value=format_skills(expertise) or "None",
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command(name = 'edit')
async def edit(ctx, *, args):

    try:
        character_name, stat_name, new_value = [a.strip() for a in args.split(',')]
    except ValueError:
        await ctx.send("Please format your command like: `!edit character_name, stat_name, new_value`")
        return

    valid_stats = {
        "name", "level", "race", "subrace", "character_class", "character_subclass",
        "strength", "dex", "constitution", "intelligence", "wisdom", "charisma",
        "background", "proficiencies", "expertise"
    }

    conn = sqlite3.connect("dnd_characters.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE characters
        SET {stat_name} = ?
        WHERE name = ?
    """, (new_value, character_name))
    conn.commit()
    conn.close()

    await ctx.send(f"Updated `{stat_name}` for **{character_name}** to `{new_value}`.")

@bot.command(name = 'check')
async def check(ctx, *, args):
    try:
        skill_name, character_name = [a.strip() for a in args.split(',')]
    except ValueError:
        await ctx.send("Please format your command like: `!check skill, character`")
        return

    user_id = ctx.author.id

    def fetch_character(character_name):
        conn = sqlite3.connect("dnd_characters.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, expertise
            FROM characters 
            WHERE name = ?
        """, (character_name,))
        row = cursor.fetchone()
        conn.close()
        return row

    character = fetch_character(character_name)

    if not character:
        await ctx.send(f"{ctx.author.mention}, no character named '{character_name}' found, please use *!add* to add your character!")
        return


    prof_roll = None
    exp_roll = None

    name, level, race, subrace, character_class, subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, expertise = character

    prof_bonus = math.ceil(level/4) + 1


    modifiers = {
        "str": math.floor((int(strength) - 10)/2),
        "dex": math.floor((int(dex) - 10)/2),
        "con": math.floor((int(constitution) - 10)/2),
        "int": math.floor((int(intelligence) - 10)/2),
        "wis": math.floor((int(wisdom) - 10)/2),
        "cha": math.floor((int(charisma) - 10)/2)
    }

    ability_skills = {
        "str": ['athletics'],
        "dex": ['acrobatics', 'stealth', 'sleight of hand'],
        "int": ['arcana', 'history', 'investigation', 'nature', 'religion'],
        "wis": ['animal handling', 'insight', 'medicine', 'perception', 'survival'],
        "cha": ['deception', 'intimidation', 'persuasion', 'performance']
    }

    def roll_skill(skill_name, ability_skills, proficiencies, expertise, prof_bonus):

        ability_used = None

        for ability, skills  in ability_skills.items():
            if skill_name in skills:
                ability_used = ability
                break

        ability_mod = modifiers.get(ability_used, 0)

        roll = random.randint(1, 20)

        if roll == 1:
            return f"{name} rolls for **{skill_name.capitalize()}**: Nat `{roll}`, Critical Failure"

        elif roll == 20:
            return f"{name} rolls for **{skill_name.capitalize()}**: Nat `{roll}`, Critical Success"


        if skill_name in expertise:
            exp_roll = roll + (prof_bonus * 2) + ability_mod
            print(roll, ability_mod)
            return f"{name} rolls for **{skill_name.capitalize()}**: {roll} + expertise bonus ({prof_bonus*2}) + ability modifer ({ability_mod}) = `{exp_roll}`"

        elif skill_name in proficiencies:
            prof_roll = roll + prof_bonus + ability_mod
            print(roll, ability_mod)
            return f"{name} rolls for **{skill_name.capitalize()}**: {roll} + proficiency bonus ({prof_bonus}) + ability modifer ({ability_mod}) = `{prof_roll}`"

        no_prof_roll = roll + ability_mod
        return f"{name} rolls for **{skill_name.capitalize()}**: {roll} + ability modifer ({ability_mod}) = `{no_prof_roll}`"

    result = roll_skill(skill_name, ability_skills, proficiencies, expertise, prof_bonus)
    await ctx.send(result)
    
@bot.command(name = 'how')
async def help_embed(ctx):

    embed = discord.Embed(
        title="Welcome to Emilie's DnD Character Creator",
        description="Here's a list of the currently available commands, how to use them and what they do!",
        color=discord.Color.random()
    )

    embed.add_field(
        name="!random",
        value = "Generates a random DnD character including race, class, ability scores, background, skill proficiencies and expertise!",
        inline=False
    )

    embed.add_field(
        name = "!add",
        value = "Adds a character to the database to be used later.",
        inline = False
    )

    embed.add_field(
        name="!database | Type !database *character name*",
        value= "Displays the character sheet for any character that has been added to the database. Character name is case sensitive.",
        inline=False
    )

    embed.add_field(
        name="!edit | Type !edit *character name*, *stat you wish to edit*, *new value*",
        value="Edits values within the database for a specific character.\nValid stats are name, level, race, subrace, character_class, character_subclass, strength, dex, constitution, intelligence, wisdom, charisma, background, proficiencies, and expertise.",
        inline=True
    )

    embed.add_field(
        name="!check | Type !check *skill*, *character name*",
        value="Rolls a skill check with proficiency bonuses and ability bonuses already applied!",
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command(name = 'roll')
async def roll_d20(ctx, *, args):

    number, dice = args.lower().split('d')
    num_dice = int(number) if number else 1
    die_type = int(dice)

    if die_type not in [4, 6, 8, 10, 12, 20]:
        await ctx.send("Unsupported die type! Please use one of: d4, d6, d8, d10, d12, d20 <33")
        return

    rolls = [random.randint(1, die_type) for _ in range(num_dice)]
    total = sum(rolls)
    roll_results = ', '.join(str(roll) for roll in rolls)

    await ctx.send(f"Rolled **{num_dice}d{die_type}**: {roll_results}\nTotal: `{total}`")

bot.run(TOKEN)
