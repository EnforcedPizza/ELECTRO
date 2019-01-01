import discord
from discord.ext import commands
import asyncio
import colorsys
import random
import time
import os
import json
import aiohttp
import datetime
from discord import Game, Embed, Color, Status, ChannelType

with open("prefixes.json") as f:
    prefixes = json.load(f)
default_prefix = "e!"

def prefix(bot, message):
    id = message.server.id
    return prefixes.get(id, default_prefix)

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

@bot.command(name="prefix", pass_context=True)
async def _prefix(ctx, new_prefix):
    # Do any validations you want to do
    prefixes[ctx.message.server.id] = new_prefix
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)
        await bot.say('{} is the new prefix for your server!'.format(new_prefix))

async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name='for e!help'))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name='with '+str(len(set(bot.get_all_members())))+' users'))
        await asyncio.sleep(5)
        await bot.change_presence(game=discord.Game(name='in '+str(len(bot.servers))+' servers'))
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    print('the bot is ready')
    print(bot.user.name)
    print(bot.user.id)
    print('working properly')
    bot.loop.create_task(status_task())

def is_owner(ctx):
    return ctx.message.author.id == "488353416599306270" 
 
@bot.command(pass_context=True)
@commands.check(is_owner)
async def oof():
	await bot.change_presence(game=discord.Game(name='For e!help with '+str(len(set(bot.get_all_members())))+' users in' +str(len(bot.servers))+' servers'))
	await bot.delete_message(ctx.message)
 
@bot.command(pass_context = True)
@commands.check(is_owner)
async def servers(ctx):
  servers = list(bot.servers)
  await bot.say(f"Connected on {str(len(servers))} servers:")
  await bot.say('\n'.join(server.name for server in servers))						
 																
@bot.command(pass_context = True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    await bot.say("Pong! {}ms".format(round((t2-t1)*1000)))

@bot.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await bot.change_nickname(user, nickname)
    await bot.say("{}'s nickname was changed to {}!".format(user, nickname))
    await bot.delete_message(ctx.message)

@bot.command()
async def invite():
	await bot.say('Add me to your server by this link - https://discordapp.com/api/oauth2/authorize?client_id=510491243155816449&permissions=8&scope=bot')
	
@bot.command()
async def authlink():
	await bot.say('https://discordapp.com/api/oauth2/authorize?client_id=510491243155816449&permissions=8&scope=bot')	

@bot.command(pass_context = True)  
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="HERE WHAT I FOUND!", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)	

@bot.command(pass_context = True)  
async def avatar(ctx, user: discord.Member):
	url = user.avatar_url
	await bot.say(url)
												
@bot.command()
async def ownerinfo():
    await bot.say("**__THIS BOT WAS CREATED BY ADIB HOQUE__**    **DISCORD** - `@Adib Hoque#5782` **YOUTUBE** - YouTube.com/AdibHoque")	
	  		   	   	
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await bot.send_message(user, message)
    await bot.say('✅YOUR DM WAS SENT!')
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def say(ctx, *, message=None):
    message = message or "Please specify a message to say!"
    await bot.say(message)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def purge(ctx, number):
    mgs = [] 
    number = int(number) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    await bot.say('✅ {} MESSAGES WERE PURGED!'.format(number))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def spam():
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
	await bot.say('spam')
 
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def english(ctx, *, msg = None):
	channel = ctx.message.channel
	await bot.say(msg + ', Please do not use any other languages than **English.**')
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
@commands.check(is_owner)
async def masstype(ctx, *, message=None):
    message = message or "Please specify a word to masstype!"
    await bot.delete_message(ctx.message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)
    await bot.say(message)		

@bot.command(pass_context = True) 
@commands.has_permissions(kick_members=True)
async def giverole(ctx, user: discord.Member, *, role: discord.Role = None):
        if role is None:
            return await bot.say("Please specify a role to give! ")
            if role not in user.roles:
            	await bot.add_roles(user, role)
            	return await bot.say("{} role has been added to {}.".format(role, user))

@bot.command(pass_context = True) 
@commands.has_permissions(kick_members=True)
async def removerole(ctx, user: discord.Member, *, role: discord.Role = None):
	if role is None:
		return await bot.say('Please specify a role to remove!')
		if role in user.roles:
			return await bot.remove_roles(user, role)
			return await bot.say("{} role has been removed from {}.".format(role, user))

@bot.command(pass_context=True)
async def serverinfo(ctx):
    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50:
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await bot.say(embed = join);
		   	   	   	  				   	   	   
@bot.command(pass_context=True) 
@commands.has_permissions(kick_members=True)     
async def kick(ctx, user:discord.Member):
    if user is None:
      await bot.say('Please mention a user to kick!')
    if user.server_permissions.kick_members:
      await bot.say('**{} is mod or admin so Im unable to kick!**'.format(user))
      return
    else:
      await bot.kick(user)
      await bot.say(user.name+' was kicked. Good bye '+user.name+'!')
      await bot.delete_message(ctx.message)
    
@bot.command(pass_context=True)  
@commands.has_permissions(ban_members=True)      
async def ban(ctx,user:discord.Member=None):
    if user is None:
      await bot.say('Please specify a member to ban!')
    if user.server_permissions.ban_members:
      await bot.say('**{} is mod or admin so Im unable to ban**'.format(user))
      return
    else:
      await bot.ban(user)
      await bot.say(user.name+' was banned. Good bye '+user.name+'!')   

@bot.command(pass_context=True)
@commands.check(is_owner)
async def roledm(ctx, role: discord.Role, *, message):
    for member in ctx.message.server.members:
        if role in member.roles:
        	await bot.delete_message(ctx.message)
        	await bot.send_message(member, message)

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def substract(left : int, right : int):
    """Subtracts two numbers together."""
    await bot.say(left - right)

@bot.command()
async def divide(left : int, right : int):
    """Divides two numbers together."""
    await bot.say(left / right)

@bot.command()
async def multiply(left : int, right : int):
    """Multiplies two numbers together."""
    await bot.say(left * right)
 
@bot.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_image(url=res['message'])
            embed.title = "{} twitted: {}".format(usernamename, txt)
            await bot.say(embed=embed)		   	   	 
 
@bot.command(pass_context=True)
async def love(ctx, user: discord.Member = None, *, user2: discord.Member = None):
    shipuser1 = user.name
    shipuser2 = user2.name
    useravatar1 = user.avatar_url
    useravatar2s = user2.avatar_url
    self_length = len(user.name)
    first_length = round(self_length / 2)
    first_half = user.name[0:first_length]
    usr_length = len(user2.name)
    second_length = round(usr_length / 2)
    second_half = user2.name[second_length:]
    finalName = first_half + second_half
    score = random.randint(0, 100)
    filled_progbar = round(score / 100 * 10)
    counter_ = '█' * filled_progbar + '‍ ‍' * (10 - filled_progbar)
    url = f"https://nekobot.xyz/api/imagegen?type=ship&user1={useravatar1}&user2={useravatar2s}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f"{shipuser1} ❤ {shipuser2} Love each others", description=f"Love\n`{counter_}` Score:**{score}% **\nLoveName:**{finalName}**", color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_image(url=res['message'])
            await bot.say(embed=embed)   		   	   	   	 		   	  		   
 

@bot.command(pass_context = True)
async def rolldice(ctx):
    choices = ['1', '2', '3', '4', '5', '6']
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Rolled! (1 6-sided die)', description=random.choice(choices))
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=em)
    
@bot.command(pass_context = True)
async def flipcoin(ctx):
    choices = ['Heads', 'Tails', 'Coin self-destructed']
    color = discord.Color(value=0x00ff00)
    em=discord.Embed(color=color, title='Flipped a coin!')
    em.description = random.choice(choices)
    await bot.send_typing(ctx.message.channel)
    await bot.say(embed=em)
    
@bot.command(pass_context=True)
async def kiss(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(andom.random(), 1, 1))
    randomurl = ["https://media3.giphy.com/media/G3va31oEEnIkM/giphy.gif", "https://i.imgur.com/eisk88U.gif", "https://media1.tenor.com/images/e4fcb11bc3f6585ecc70276cc325aa1c/tenor.gif?itemid=7386341", "http://25.media.tumblr.com/6a0377e5cab1c8695f8f115b756187a8/tumblr_msbc5kC6uD1s9g6xgo1_500.gif"]
    if user.id == ctx.message.author.id:
        await bot.say("Goodluck kissing yourself {}".format(ctx.message.author.mention))
    else:
        embed = discord.Embed(title=f"{user.name} You just got a kiss from {ctx.message.author.name}", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(randomurl))
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def hug(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    if user.id == ctx.message.author.id:
        await bot.say("{} Wanted to hug himself/herself , good luck on that you will look like an idiot trying to do it".format(user.mention))
    else:
        randomurl = ["http://gifimage.net/wp-content/uploads/2017/09/anime-hug-gif-5.gif", "https://media1.tenor.com/images/595f89fa0ea06a5e3d7ddd00e920a5bb/tenor.gif?itemid=7919037", "https://media.giphy.com/media/NvkwNVuHdLRSw/giphy.gif"]
        embed = discord.Embed(title=f"{user.name} You just got a hug from {ctx.message.author.name}", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(randomurl))
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def gender(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    random.seed(user.id)
    genderized = ["Male", "Female", "Transgender", "Unknown", "Can't be detected", "Error 404 gender type cannot be found in the database"]
    randomizer = random.choice(genderized)
    if user == ctx.message.author:
        embed = discord.Embed(title="You should know your own gender", color = discord.Color((r << 16) + (g << 8) + b))
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0xfff47d)
        embed.add_field(name=f"{user.name}'s gender check results", value=f"{randomizer}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def virgin(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    random.seed(user.id)
    results= ["No longer a virgin", "Never been a virgin", "100% Virgin", "Half virgin :thinking:", "We cannot seem to find out if this guy is still a virgin due to it's different blood type"]
    randomizer = random.choice(results)
    if user == ctx.message.author:
        embed = discord.Embed(title="Go ask yourself if you are still a virgin", color = discord.Color((r << 16) + (g << 8) + b))
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0x7dfff2)
        embed.add_field(name=f"{user.name}'s virginity check results", value=f"{randomizer}")
        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def joke(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    joke = ["What do you call a frozen dog?\nA pupsicle", "What do you call a dog magician?\nA labracadabrador", "What do you call a large dog that meditates?\nAware wolf", "How did the little scottish dog feel when he saw a monster\nTerrier-fied!", "Why did the computer show up at work late?\nBecause it had a hard drive", "Autocorrect has become my worst enime", "What do you call an IPhone that isn't kidding around\nDead Siri-ous", "The guy who invented auto-correct for smartphones passed away today\nRestaurant in peace", "You know you're texting too much when you say LOL in real life, instead of laughing", "I have a question = I have 18 Questions\nI'll look into it = I've already forgotten about it", "Knock Knock!\nWho's there?\Owls say\nOwls say who?\nYes they do.", "Knock Knock!\nWho's there?\nWill\nWill who?\nWill you just open the door already?", "Knock Knock!\nWho's there?\nAlpaca\nAlpaca who?\nAlpaca the suitcase, you load up the car.", "Yo momma's teeth is so yellow, when she smiled at traffic, it slowed down.", "Yo momma's so fat, she brought a spoon to the super bowl.", "Yo momma's so fat, when she went to the beach, all the whales started singing 'We are family'", "Yo momma's so stupid, she put lipstick on her forehead to make up her mind.", "Yo momma's so fat, even Dora can't explore her.", "Yo momma's so old, her breast milk is actually powder", "Yo momma's so fat, she has to wear six different watches: one for each time zone", "Yo momma's so dumb, she went to the dentist to get a bluetooth", "Yo momma's so fat, the aliens call her 'the mothership'", "Yo momma's so ugly, she made an onion cry.", "Yo momma's so fat, the only letters she knows in the alphabet are K.F.C", "Yo momma's so ugly, she threw a boomerang and it refused to come back", "Yo momma's so fat, Donald trump used her as a wall", "Sends a cringey joke\nTypes LOL\nFace in real life : Serious AF", "I just got fired from my job at the keyboard factory. They told me I wasn't putting enough shifts.", "Thanks to autocorrect, 1 in 5 children will be getting a visit from Satan this Christmas.", "Have you ever heard about the new restaurant called karma?\nThere's no menu, You get what you deserve.", "Did you hear about the claustrophobic astronaut?\nHe just needed a little space", "Why don't scientists trust atoms?\nBecase they make up everything", "How did you drown a hipster?\nThrow him in the mainstream", "How does moses make tea?\nHe brews", "A man tells his doctor\n'DOC, HELP ME. I'm addicted to twitter!'\nThe doctor replies\n'Sorry i don't follow you...'", "I told my wife she was drawing her eyebrows too high. She looked surprised.", "I threw a boomeranga a few years ago. I now live in constant fear"]
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name=f"Here is a random joke that {ctx.message.author.name} requested", value=random.choice(joke))
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def slap(ctx, user: discord.Member = None):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    gifs = ["http://rs20.pbsrc.com/albums/b217/strangething/flurry-of-blows.gif?w=280&h=210&fit=crop", "https://media.giphy.com/media/LB1kIoSRFTC2Q/giphy.gif", "https://i.imgur.com/4MQkDKm.gif"]
    if user == None:
        await bot.say(f"{ctx.message.author.mention} ```Proper usage is\n\n>slap <mention a user>```")
    else:
        embed = discord.Embed(title=f"{ctx.message.author.name} Just slapped the shit out of {user.name}!", color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_image(url=random.choice(gifs))
        await bot.say(embed=embed)
   
@bot.command(pass_context=True, aliases=['server'])
@commands.has_permissions(kick_members=True)
async def membercount(ctx, *args):
    if ctx.message.channel.is_private:
        await bot.delete_message(ctx.message)
        return

    g = ctx.message.server

    gid = g.id
    membs = str(len(g.members))
    membs_on = str(len([m for m in g.members if not m.status == Status.offline]))
    users = str(len([m for m in g.members if not m.bot]))
    users_on = str(len([m for m in g.members if not m.bot and not m.status == Status.offline]))
    bots = str(len([m for m in g.members if m.bot]))
    bots_on = str(len([m for m in g.members if m.bot and not m.status == Status.offline]))
    created = str(g.created_at)
    
    em = Embed(title="Membercount")
    em.description =    "```\n" \
                        "Members:   %s (%s)\n" \
                        "  Users:   %s (%s)\n" \
                        "  Bots:    %s (%s)\n" \
                        "Created:   %s\n" \
                        "```" % (membs, membs_on, users, users_on, bots, bots_on, created)

    await bot.send_message(ctx.message.channel, embed=em)
    await bot.delete_message(ctx.message)
    
@bot.command()
async def fortnite():
	await bot.delete_message(ctx.message)
	await bot.say('<a:fortnite1:527116722369593365> <a:fortnite2:527116726249193472> <a:fortnite1:527116722369593365>')
	
@bot.command()
async def hundred():
	await bot.delete_message(ctx.message)
	await bot.say('<a:100:527116694506700819>')
	
@bot.command()
async def party():
	await bot.delete_message(ctx.message)
	await bot.say('<a:PartyGlasses:527116697791102977>')	
	
@bot.command()
async def dogdance():
	await bot.delete_message(ctx.message)
	await bot.say('<a:dogdance:527116702580867092>')
	
@bot.command()
async def hype():
	await bot.delete_message(ctx.message)
	await bot.say('<a:DiscordHype:527116695253286933>')
	
@bot.command()
async def plsboi():
	await bot.delete_message(ctx.message)
	await bot.say('<a:plsboi:527116722218467328>')
	
@bot.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='ELECTRO Commands')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = '``USAGE:`` ',value ='To see a page, just add the page number after the `e!help` command.Like this `e!help1`, `e!help2` Etc.',inline = False)
    embed.add_field(name = 'PAGE 1 | General Commands ',value ='General commands which everyone can use!.',inline = False)
    embed.add_field(name = 'PAGE 2 | Moderation Commands',value ='Commands that are used for moderation and can only be used by server moderators.',inline = False)
    embed.add_field(name = 'PAGE 3 | Fun Commands ',value ='Fun commands are used for fun and can be used by everyone.',inline = False)
    embed.add_field(name = 'PAGE 4 | Emoji Commands ',value ='Commands that makes ELECTRO send gif emotes.',inline = False)
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Bot Commands!')
    			
@bot.command(pass_context = True)
async def help1(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='General Commands')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Ping',value ='Returns ping lantency! **USAGE:**``e!ping``',inline = False)
    embed.add_field(name = 'Userinfo',value ='Shows info about mentioned user! **USAGE:**``e!userinfo @user``',inline = False)
    embed.add_field(name = 'Serverinfo',value ='Shows info about the server! **USAGE:**``e!serverinfo``',inline = False)
    embed.add_field(name = 'Ownerinfo',value ='Shows info about the bot owner! **USAGE:**``e!ownerinfo``',inline = False)
    embed.add_field(name = 'Avatar',value ='Shows avatar of the mentioned user! **USAGE:**``e!avatar @user``',inline = False)
    embed.add_field(name = 'Membercount',value ='Shows member count of the server! **USAGE:**``e!membercount``',inline = False)
    embed.add_field(name = 'Invite',value ='Sends bot invite link! **USAGE:**``e!invite``',inline = False)
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For General Commands!')
    
@bot.command(pass_context = True)
async def help2(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Moderation Commands')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Kick',value ='Kicks out mentioned user from the server! **USAGE:**``e!kick @user``',inline = False)
    embed.add_field(name = 'Ban',value ='Bans mentioned user from the server! **USAGE:**``e!ban @user``',inline = False) 
    embed.add_field(name = 'Setnick',value ='Changes nickname of mentioned user! **USAGE:**``e!setnick @user [new nickname]``',inline = False)
    embed.add_field(name = 'Giverole',value ='Gives role to mentioned user! **USAGE:**``e!giverole @user @role``',inline = False)
    embed.add_field(name = 'Removerole',value ='Removes a role from mentioned user! **USAGE:**``e!removerole @user @role``',inline = False)
    embed.add_field(name = 'Say',value ='Make ELECTRO say anything you want! **USAGE:**``e!say [your text]``',inline = False)
    embed.add_field(name = 'DM',value ='Make ELECTRO DM mentioned user anything you want! **USAGE:**``e!dm @user [your text]``',inline = False) 
    embed.add_field(name = 'English',value ='Softwarns mentioned user to talk in English! **USAGE:**``e!englis;h @user``',inline = False) 
    embed.add_field(name = 'Purge',value ='Bulk deletes messages! **USAGE:**``e!purge [amount]``',inline = False)
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Moderation Commands!') 
    
@bot.command(pass_context = True)
async def help3(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Fun Commands')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Joke',value ='Sends a random joke! **USAGE:**``e!joke``',inline = False)
    embed.add_field(name = 'Love',value ='Detect love percentage between two users! **USAGE:**``e!love @user @user``',inline = False) 
    embed.add_field(name = 'Slap',value ='Slaps mentioned user! **USAGE:**``e!slap @user``',inline = False)
    embed.add_field(name = 'Kiss',value ='Kisses mentioned user! **USAGE:**``e!kiss @user``',inline = False)
    embed.add_field(name = 'Hug',value ='Hugs mentioned user! **USAGE:**``e!hug @user``',inline = False)
    embed.add_field(name = 'Virgin',value ='ELECTRO checks virginity of mentioned user! **USAGE:**``e!virgin @user``',inline = False)
    embed.add_field(name = 'Gender',value ='ELECTRO detects gender of mentioned user! **USAGE:**``e!gender @user``',inline = False) 
    embed.add_field(name = 'Tweet',value ='Make a fake twitter tweet! **USAGE:**``e!tweet [twitter name] [text]``',inline = False) 
    embed.add_field(name = 'Rolldice',value ='ELECTRO rolls dice and sends random number 1-6! **USAGE:**``e!rolldice``',inline = False)
    embed.add_field(name = 'Flipcoin',value ='ELECTRO flips coin! **USAGE:**``e!flipcoin``',inline = False)
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For Fun Commands!')   
    
@bot.command(pass_context = True)
async def help4(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Emoji Commands')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/526757013745696769/527492677558599696/electro.png')
    embed.add_field(name = 'Fortnite',value ='<a:fortnite1:527116722369593365> <a:fortnite2:527116726249193472> <a:fortnite1:527116722369593365>',inline = False)
    embed.add_field(name = 'Hundred',value ='<a:100:527116694506700819>',inline = False)
    embed.add_field(name = 'Party',value ='<a:PartyGlasses:527116697791102977>',inline = False)
    embed.add_field(name = 'Dogdance',value ='<a:dogdance:527116702580867092>',inline = False)
    embed.add_field(name = 'Hype',value ='<a:DiscordHype:527116695253286933>',inline = False)
    embed.add_field(name = 'Plsboi',value ='<a:plsboi:527116722218467328>',inline = False)
    await bot.send_message(author ,embed=embed)
    await bot.say('📨 Check Your DMs For General Commands!')    
	 		   	 		   	  		        
bot.run(os.getenv('Token'))		   	   	   	 		   	  		   	 
