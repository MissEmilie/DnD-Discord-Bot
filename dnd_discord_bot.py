import os
import discord
from discord.ext import commands
from dnd_bot_config import TOKEN
import dnd_character_creator
import sqlite3
import math
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)


@bot.event
async def on_ready():
    print("Emilie's DnD Character Creator has arrived!")

@bot.command(name = 'roll')
async def new_character(ctx):
    result = dnd_character_creator.play()
    print(f"DEBUG - result: {repr(result)}")

    if result and result.strip():
        await ctx.send(result)

    else:
        await ctx.send("Oops! Something went wrong — character could not be created.")

@bot.command(name = 'add')
async def save_character(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send("Enter Character Name")
    name_msg = await bot.wait_for('message', check=check, timeout=60)
    name = name_msg.content

    await ctx.send("Enter Character Level")
    level_msg = await bot.wait_for('message', check=check, timeout=60)
    level = int(level_msg.content)

    await ctx.send("Enter Character Stats (str, dex, con, int, wis, cha): ")
    stats_msg = await bot.wait_for('message', check=check, timeout=60)
    stats = list(map(int, stats_msg.content.replace(' ', '').split(',')))
    str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat = stats

    await ctx.send("Enter Skill proficiencies (comma-separated): ")
    prof_msg = await bot.wait_for('message', check=check, timeout=60)
    proficiencies = [s.strip().lower() for s in prof_msg.content.split(',')]

    await ctx.send("Enter Expertise (comma-separated, optional): ")
    exp_msg = await bot.wait_for('message', check=check, timeout=60)
    expertise = [s.strip().lower() for s in exp_msg.content.split(',') if s.strip()]

    await ctx.send("Save to database? (Y/N): ")
    confirm_msg = await bot.wait_for('message', check=check, timeout=60)
    if confirm_msg.content.upper() != 'Y':
        await ctx.send("Character creation cancelled.")
        return

    conn = sqlite3.connect('characters.db')
    c = conn.cursor()

    c.execute("""INSERT INTO characters (
        name, level, strength, dex, constitution, intelligence, wisdom, charisma, proficiencies, expertise
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    (name, level, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat,
     json.dumps(proficiencies), json.dumps(expertise)))

    conn.commit()
    conn.close()

    await ctx.send(f"**{name}** added to database")

@bot.command(name = 'Wyll')
async def new_character(ctx):
    result = dnd_character_creator.wyll()
    print(f"DEBUG - result: {repr(result)}")

    if result and result.strip():
        await ctx.send(result)

    else:
        await ctx.send("Oops! Something went wrong — character could not be created.")

@bot.command(name = 'Astarion')
async def new_character(ctx):
    result = dnd_character_creator.astarion()
    print(f"DEBUG - result: {repr(result)}")

    if result and result.strip():
        await ctx.send(result)

    else:
        await ctx.send("Oops! Something went wrong — character could not be created.")
    

bot.run(TOKEN)