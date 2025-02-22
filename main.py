import os
import discord
import random
import json
import asyncio
from discord.ext import commands
from discord.ext.commands import BucketType

json_path = os.path.join(os.getcwd(), "mainbank.json")


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot démarré avec succès !")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1336739895577935893:
        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return
        user = guild.get_member(payload.user_id)
        if user is None:
            return

        if payload.emoji.name == "Valorant":
            role = discord.utils.get(guild.roles, name="Valorant")
        elif payload.emoji.name == "LeagueofLegend":
            role = discord.utils.get(guild.roles, name="League of Legend")
        else:
            return

        if role:
            await user.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 1335660092867084358:
        guild = bot.get_guild(payload.guild_id)
        if guild is None:
            return
        user = guild.get_member(payload.user_id)
        if user is None:
            return

        if payload.emoji.name == "Valorant":
            role = discord.utils.get(guild.roles, name="Valorant")
        elif payload.emoji.name == "LeagueofLegend":
            role = discord.utils.get(guild.roles, name="League of Legend")
        else:
            return

        if role:
            await user.remove_roles(role)


@bot.command()
async def roulette(ctx, arg: str = "", argt: str = ""):

    sortie = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
              "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
              "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34",
              "35", "36")

    if arg == "" or argt == "":
        await ctx.send(
            "Cet commande fonctionne sous la forme : !casino <red/black/nombre> <montant>"
        )
        return
    elif arg != "red" and arg != "black" and arg not in sortie:
        await ctx.send(
            "Cet commande fonctionne sous la forme : !casino <red/black/nombre> <montant>"
        )
        return
    try:
        argt = int(argt)
    except ValueError:
        await ctx.send(
            "Cet commande fonctionne sous la forme : !casino <red/black/nombre> <montant>"
        )

    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if users[str(user.id)]["wallet"] < int(argt):
        await ctx.send("vous n'avez pas le montant necessaire pour jouer")
        return
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    i = random.randint(0, 36)

    color = "🟥" if i in red else "⬛" if i != 0 else "🟩"

    if (arg == "red" and i in red) or (arg == "black" and i not in red):
        em = discord.Embed(title="Resultat du Casino",
                           color=discord.Color.from_str("#29D381"))
        em.add_field(name=f"{i} {color}", value="")
        em.add_field(name=f"Gain: {argt}€", value="")
        await ctx.send(embed=em)

        users[str(user.id)]["wallet"] += argt
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    elif arg.isdigit() and int(arg) == i:
        em = discord.Embed(title="Resultat du Casino",
                           color=discord.Color.from_str("#FFD700"))
        em.add_field(name=f"{i} {color}", value="")
        em.add_field(name=f"Gain: {argt*36}€ !", value="")
        await ctx.send(embed=em)

        users[str(user.id)]["wallet"] += argt * 36
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    else:
        em = discord.Embed(title="Resultat du Casino",
                           color=discord.Color.from_str("#df2e2e"))
        em.add_field(name=f"{i} {color}", value="")
        em.add_field(name="Gain: 0€", value="")
        await ctx.send(embed=em)

        users[str(user.id)]["wallet"] -= argt
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@bot.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    em = discord.Embed(title=f"porte monnaie de {ctx.author.name}",
                       color=discord.Color.from_str("#29D381"))
    em.add_field(name="Wallet", value=wallet_amt)
    await ctx.send(embed=em)


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    json_path = "mainbank.json"

    if not os.path.exists(json_path):
        with open(json_path, "w") as f:
            json.dump({}, f)

    with open(json_path, "r") as f:
        users = json.load(f)

    return users
    
@bot.command()
@commands.cooldown(1, 3600 * 1, BucketType.user)  

async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    millionaire= random.randint(0,20)
    em = discord.Embed(title="Argent récolté",color=discord.Color.from_str("#29D381"))
    if millionaire == 20:
        argt = random.randint(1000,3000)
        em.add_field(name="Passant riche", value="")
    else:
        em.add_field(name="Simple passant", value="")
        argt = random.randint(100,300)

        
    em.add_field(name=f"Gain: {argt}€", value="")

    argt=random.randint(150,300)

    users[str(user.id)]["wallet"] += argt
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    await ctx.send(embed=em)

@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        hours, remainder = divmod(int(error.retry_after), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Patience! Vous pourrez mendier de nouveau dans {hours}h {minutes}m {seconds}s.")





@bot.command()
async def clear(ctx,amount:int=5) :
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("vous ne pouvez pas utiliser cette commande en message privé")

    has_permission = ctx.author.guild_permissions.manage_messages
    if not has_permission:
        return(await ctx.send("vous n'avez pas les permissions pour utiliser la commande."))

    is_limit_reached = amount > 100
    if is_limit_reached:
        return await ctx.send("vous ne pouvez pas supprimez plus de 100 messages")

    is_text_channel =isinstance(ctx.channel, discord.TextChannel)
    if not is_text_channel:
        return await ctx.send("vous ne pouvez pas utiliser ces commande dans un salon vocal")

    await ctx.channel.purge(limit=amount+1)

    return await ctx.send(f"{amount} messages ont été supprimés")

@bot.command()
async def tg(ctx, member: discord.Member, time:int):
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("vous ne pouvez pas utiliser cette commande en message privé")

    has_permission = ctx.author.guild_permissions.administrator
    if not has_permission:
        return(await ctx.send("vous n'avez pas les permissions pour utiliser la commande."))

    if time>10:
        return await ctx.send("vous ne pouvez pas mettre un temps supérieur à 10 minutes")
    

    async def on_message(message):
        if message.author.id == member.id:
            await message.add_reaction("🇹")  
            await message.add_reaction("🇬")

    bot.add_listener(on_message, "on_message")
    await ctx.send(f"{member.mention} est puni pendant {time} minutes.")

    await asyncio.sleep(time * 60)

    bot.remove_listener(on_message, "on_message")

    await ctx.send(f"{member.mention} n'est plus puni.")


"""
@bot.command()
async def tg2(ctx, member: discord.Member, time:int):
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("vous ne pouvez pas utiliser cette commande en message privé")

    has_permission = ctx.author.guild_permissions.administrator
    if not has_permission:
        return(await ctx.send("vous n'avez pas les permissions pour utiliser la commande."))

    if time>10:
        return await ctx.send("vous ne pouvez pas mettre un temps supérieur à 10 minutes")
    

    async def on_message(message):
        if message.author.id == member.id:
            await message.delete
            await ctx.send("")

    bot.add_listener(on_message, "on_message")
    await ctx.send(f"{member.mention} est puni pendant {time} minutes.")

    await asyncio.sleep(time * 60)

    bot.remove_listener(on_message, "on_message")

    await ctx.send(f"{member.mention} n'est plus puni.")
    """
    





bot.run("MTMzNTYwMDIzNzA2NjA2Mzk0Ng.G-7NI0.Na12CrNGxCATq7iy39jZnTjRRqdlE8aaEM1Cx0")
