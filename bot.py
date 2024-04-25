import asyncio
import requests
import json
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True  # Enable the member intent

bot = commands.Bot(command_prefix=">", intents=intents)
bot.remove_command('help')  # Removing default help command


# Event: Bot is ready
@bot.event
async def on_ready():
    print("Bot is ready")

# Command: Help
@bot.command()
async def help(ctx):
    """
    Displays information about bot commands.
    """
    embed = discord.Embed(
        title='Bot Commands',
        description='Welcome to the help section. Here are all the commands',
        colour=discord.Colour.dark_gold()
    )

    embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqCjJ4HreZZOZq_GKV2DfXGFHRrFPtpxuAXg&s')

    # Adding fields for each command
    embed.add_field(
        name='>help',
        value='Shows this',
        inline=False
    )
    embed.add_field(
        name='>info',
        value='Send the information of the user',
        inline=False
    )
    embed.add_field(
        name='>punch',
        value='Punch someone you don\'t like. Command: >punch name',
        inline=False
    )
    embed.add_field(
        name='>strike',
        value='Allows you to strike a user. Command: >strike name1 name2',
        inline=False
    )
    embed.add_field(
        name='>kick',
        value='Kick a user you don\'t like. Command: >kick name reason',
        inline=False
    )
    embed.add_field(
        name='>ban',
        value='Ban a user who don\'t respect the rules. Command: >ban name reason',
        inline=False
    )
    embed.add_field(
        name='>quiz',
        value='Start a quiz session. Command: >quiz',
        inline=False
    )
    await ctx.send(embed=embed)

# Command: Punch
@bot.command()
async def punch(ctx, arg):
    """
    Allows you to punch a user: >punch name
    """
    embed = discord.Embed(
        title="Punch",
        description=f'Punched {arg}',
        color=discord.Color.dark_gold()
    )
    await ctx.send(embed=embed)

# Command: Strike
@bot.command()
async def strike(ctx, arg1, arg2):
    """
    Allows you to strike a user: >strike name1 name2
    """
    embed = discord.Embed(
        title="Strike",
        description=f'{arg1} c\'est fait foudroyer par {arg2}',
        color=discord.Color.dark_gold()
    )
    await ctx.send(embed=embed)

# Command: Info
@bot.command()
async def info(ctx):
    """
    Send the information of the user: >info
    """
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc = ctx.guild.description

    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.dark_gold()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    # Send member information
    members = []
    async for member in ctx.guild.fetch_members(limit=150):
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name, str(member.status),
                                                                       str(member.joined_at)))

# Command: Kick
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    """
    Kick a user from the server.
    """
    embed = discord.Embed(
        title='KICK ALERT !',
        description='AN ADMIN JUST KICK SOMEONE, LET\'S SEE WHO HAVE BEEN KICKED',
        colour=discord.Colour.dark_gold()
    )
    embed.set_thumbnail(url='https://media.tenor.com/PHWXH5oWlJIAAAAM/lit-retourne-tv.gif')

    if ctx.message.author.guild_permissions.kick_members:  # Check if the user has permission to kick members
        if reason is None:
            kick_message = f"{member.mention} has been kicked by {ctx.author} (No reason provided)."
        else:
            kick_message = f"{member.mention} has been kicked by {ctx.author} (Reason: {reason})."

        embed.add_field(
            name="Member Kicked",
            value=kick_message,
            inline=False
        )

        try:
            await member.kick(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick that member.")
    else:
        await ctx.send("You do not have permission to kick members.")

# Command: Ban
@bot.command()
async def ban(ctx, member: discord.Member, reason=None):
    """
    Ban a user from the server.
    """
    embed = discord.Embed(
        title='BAN ALERT!',
        description='AN ADMIN JUST BAN SOMEONE, LET\'S SEE WHO HAVE BEEN BANNED',
        colour=discord.Colour.dark_gold()
    )
    embed.add_field(name='Reason:', value=reason if reason else 'No reason provided')
    embed.set_thumbnail(url='https://media1.tenor.com/m/atbWSwDthPkAAAAC/case-caseoh.gif')
    await ctx.send(embed=embed)

    if reason is None:
        await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
    else:
        message_ok = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message_ok)
        await member.ban(reason=reason)

# Command: Quiz
@bot.command()
async def quiz(ctx):
    """
    Start a quiz session.
    """
    if ctx.author == bot.user:
        return
    qs, answer = get_question()
    
    embed = discord.Embed(
        title="Quiz",
        description=qs,
        color=discord.Color.dark_gold()
    )
    embed.set_thumbnail(url='https://media.tenor.com/NiGJMe3lTHcAAAAM/counter10-countdown.gif')

    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.content.isdigit()
    
    try:
        guess = await bot.wait_for('message', check=check, timeout=12.0)
    except asyncio.TimeoutError:
        return await ctx.channel.send('Timeout')
    
    if int(guess.content) == answer:
        await ctx.channel.send('You got it right!')
    else:
        await ctx.channel.send('Try again')

# Function: Get Question
def get_question():
    """
    Fetches a random question from an API.
    """
    qs = ''
    id = 1
    answer = 0
    response = requests.get("http://127.0.0.1:8000/api/random/")
    json_data = json.loads(response.text)
    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"
    for item in json_data[0]['answer']:
        qs += str(id) + "." + item['answer'] + "\n"
        if item['is_correct']:
            answer = id
        id += 1
    return (qs, answer)

# Running the bot
bot.run(os.getenv('DISCORD-TOKEN'))
