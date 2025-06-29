import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN') #You must have a seperate file in the folder named .env that contains a variable called DISCORD_TOKEN=put your discord bots token here

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

poppy_meow_role = "Poppy meow"

class user_balance():
    def __init__(self, name, bal):
        self.name = name
        self.bal = bal

    def __str__(self):
        return(f"Hello {self.name}! Your balance is {self.bal}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is Online.") 

    await bot.tree.sync()
    print(f"slash commands synced") #The print statements are not needed they just add clarity for the person running the code

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "meow" in message.content: #This section can be used for an automod as an autodelete/reply for banned words if you wish
        await message.channel.send("Meow.")

    elif bot.user in message.mentions:
        await message.reply(f"Hello {message.author.display_name}! For a list of commands type !poppy")

    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        print(f"DM from {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.tree.command(name="poppyhelp", description="Lists bot commands.")
async def poppy_command(interaction: discord.Interaction):
    await interaction.response.send_message(
"Here's a list of commands I can run for you!\n"
"```"
"!poppy - I wonder 🤔\n"
"!hello - haiii \n"
"!arr - arr\n"
"!checkbal - shows user their account balance or creates an account for them if they didnt have one \n"
"!addbal - (Admin) allows user to add funds to their account"
"!roll (put a number here) - rolls a number 1 through whatever you input \n"
"!dm (message) - I will dm you the message you put into the command \n"
f"!assign - assigns the Poppy meow role \n"
f"!unassign - unassigns the Poppy meow role \n"
"!reply - Poppy replies to you\n"
"!secret - shhhh... 🤫"
"```"
)

@bot.command()
async def poppy(ctx):
    await ctx.send(
"Here's a list of commands I can run for you!\n"
"```"
"!poppy - I wonder 🤔\n"
"!hello - haiii \n"
"!arr - arr\n"
"!checkbal - shows user their account balance or creates an account for them if they didnt have one \n"
"!addbal - (Admin) allows user to add funds to their account"
"!roll (put a number here) - rolls a number 1 through whatever you input \n"
"!dm (message) - I will dm you the message you put into the command \n"
f"!assign - assigns the {poppy_meow_role} role \n"
f"!unassign - unassigns the {poppy_meow_role} role \n"
"!reply - Poppy replies to you\n"
"!secret - shhhh... 🤫"
"```"
)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx. author.mention}! <:TiktokHappy:1379550917485134005> ")

@bot.command()
async def arr(ctx):
    await ctx.send(f"arr")

@bot.command()
async def roll(ctx, * ,msg):
    msg = msg.replace("(", "").replace(")", "")
    msg = int(msg)
    random_int = random.randint(1, msg)
    await ctx.send(f"You rolled a {random_int}.")

@bot.command()
@commands.has_role(poppy_meow_role)
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=poppy_meow_role)
    if role: #server must have the role Poppy Meow or replace the variable in poppy_meow_role for this to work
        await ctx.send(f"{ctx.author.mention} You already have the {role} role.")
    else:
        await ctx.send("Role does not exist!")

@assign.error
async def assign_error(ctx, error):
    role = discord.utils.get(ctx.guild.roles, name=poppy_meow_role)
    if isinstance(error, commands.MissingRole):
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} {role} has been added to your roles!")

@bot.command()
@commands.has_role(poppy_meow_role)
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=poppy_meow_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} your {role} has been removed!")
    else:
        await ctx.send("Role does not exist!")

@unassign.error
async def unassign_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention} You do not have the {poppy_meow_role} role.")

@bot.command()
@commands.has_role(poppy_meow_role)
async def secret(ctx):
    await ctx.send("meow")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention} You must have the {poppy_meow_role} role to execute this command!")

@bot.command() #if the user types !dm hello world the *, msg breaks that hello world off into a msg variable 
async def dm(ctx, *, msg):
    if msg in (): #<- you can add banned words in this list
        await ctx.author.send(f"Hateful use of the !dm command is not tolerated.")
    else:
        await ctx.author.send(f"You said {msg}.")

    '''
    user = discord.utils.find(
    lambda m: m.name == "laiopsol",
    ctx.guild.members
)
    if user:
        await user.send(f"{msg}")
        print(f"sent {user} {msg}")
    else:
        print(f"{user} not found")
'''

@bot.command()
async def checkbal(ctx):
    found = False #Must have a file named Balances.txt in the folder your ide is working from
  
    with open("Balances.txt", 'r') as file:
        for line in file: 
            name = line.strip().split()[0]
            bal = line.strip().split()[1]

            if name == str(ctx.author):
                await ctx.reply(f"Hello {ctx.author.mention}! Your balance is ${bal}.")
                found = True
                break
    
    if not found:
        with open("Balances.txt",'a') as file:
            file.write(f"{ctx.author} 100\n")
            print(f"created new balance account for {ctx.author}")
            await ctx.reply(f"Created account for {ctx.author.mention}! You get a free $100!")

@bot.command()
@commands.has_role("Bank Admin") #You can change this role name to the mod role name in your server or add the role Bank Admin
async def addbalself(ctx, *, msg):
    found = False
    updated_lines = []
    msg = int(msg)
    author = str(ctx.author)

    with open("Balances.txt", 'r') as file:
        for line in file:
            name, bal = line.strip().split()

            if name == author:
                bal = int(bal) + msg
                updated_lines.append(f"{name} {bal}\n")
                found = True
                break

            else:
                updated_lines.append(line)

    if found:
        with open("Balances.txt", 'w') as file:
            file.writelines(updated_lines)
            print(bal)

        await ctx.reply(f"Successfully added ${msg} to your account.\nYour Balance is now ${bal}")
    else:
        await ctx.reply("Please create a balance account first by doing !checkbal")



@addbalself.error
async def addbalself(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention} You must have the Bank Admin role to execute this command!")

@bot.command()
async def meow(ctx):
    await ctx.reply("Meow.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
