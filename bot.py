import discord
from discord.ext import commands
import random
import json

queue = []
fights = []

#embed=discord.Embed(title="CIS Creative", description="Поиск боксфайта")
#embed.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
#embed.add_field(name="Хочешь боксфайт?", value="Нажми на ✋ снизу и бот найдет тебе соперника.", inline=False)
#embed.add_field(name="Want a boxfight?", value="Click on the ✋ from the bottom and the bot will find you an opponent.", inline=False)



TOKEN = 'NjY4MDQwNzg4NDgyOTgxODk5.XiNqiw.BESeRIDSoBLGnfC7mweW40R6Sg4'

client = commands.Bot(command_prefix = '.')
def get_points(s):
    l = len(s)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = s[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = s[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))

    return integ[0]

client = commands.Bot(command_prefix = '.')
def get_p1(s):
    l = len(s)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = s[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = s[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))

    return integ[0]

client = commands.Bot(command_prefix = '.')
def get_p2(s):
    l = len(s)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = s[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = s[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))

    return integ[2]

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def createnewmsg(ctx):
    embed=discord.Embed(title="CIS Creative", description="Поиск боксфайта")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
    embed.add_field(name="Хочешь боксфайт?", value="Нажми на ✋ снизу и бот найдет тебе соперника.", inline=False)
    embed.add_field(name="Want a boxfight?", value="Click on the ✋ from the bottom and the bot will find you an opponent.", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✋')


@client.command()	
async def close(ctx):	
    if ctx.author in queue:	
        queue.remove(ctx.author)	
        await ctx.author.send('Вы отменили поиск боксфайта.')	
    else:	
        await ctx.author.send('Вы не искали боксфайт.')	

    
@client.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)
    user = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    channel = discord.utils.find(lambda c: c.id == payload.channel_id, guild.channels)
    if not user.display_name.startswith("["):
        try:
            await user.edit(nick='[0] ' + user.name)
        except:
            print('sad')

    if payload.user_id == 668040788482981899:
        return
    
    #await user.send('{} has added {} to the the message {} {}'.format(user.name, reaction.emoji, reaction.message.content, queue))
    if payload.channel_id == 668140694996779072:
        if (user in fights) or (user in queue):
            print('Вы уже ищете боксфайт.')
            return
        queue.append(user)
        if len(queue) >= 2:
            messagefinder: discord.Message = await channel.fetch_message(payload.message_id)
            print('Нашли опонента. И создаем все остальное')
            queue.remove(user)
            oponnent = queue[random.randint(0,len(queue)) - 1]
            if user == oponnent:
                print('error user==opponent')
                return
            if user == client.user:
                print('error user==bot')
                return
            queue.remove(oponnent)
            overwrites_admin = {
            user.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            oponnent: discord.PermissionOverwrite(read_messages=True)
            }
            print(oponnent, user)
            boxchannel = await user.guild.create_text_channel('boxfight', overwrites=overwrites_admin, topic=str(payload.user_id) + ' p2 ' + str(oponnent.id))
            await oponnent.send('Вам нашли боксфайт.')
            embedplayers=discord.Embed(title="CIS Creative", description="Боксфайт.")
            embedplayers.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
            embedplayers.add_field(name="Первый игрок (♥): ", value=user.display_name, inline=False)
            embedplayers.add_field(name="Второй игрок (💩): ", value=oponnent.display_name, inline=False)
            embedrules=discord.Embed(title="CIS Creative", description="Правила.")
            embedrules.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
            embedrules.add_field(name="Карта:", value="7620-0771-9529", inline=False)
            embedrules.add_field(name="Играете до:", value="3 побед", inline=False)
            msg = await boxchannel.send(embed=embedplayers)
            await boxchannel.send(embed=embedrules)
            await msg.add_reaction('♥')
            await msg.add_reaction('💩')
            for reaction in messagefinder.reactions:
                await reaction.remove(user)
            fights.append(user)
            fights.append(oponnent)
    if payload.emoji.name == '♥':
        p1 = discord.utils.find(lambda m: m.id == int(get_p1(channel.topic)), guild.members)
        p2 = discord.utils.find(lambda m: m.id == int(get_p2(channel.topic)), guild.members)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.count <= 2 and reaction.emoji == '♥':
                return
        embed=discord.Embed(title="CIS Creative", description="Результаты боксфайта:")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
        embed.add_field(name="Победитель:", value=p1.name + " (+10)", inline=False)
        embed.add_field(name="Проигравший:", value=p2.name + " (-10)", inline=False)
        await p2.send(embed=embed)
        await p1.send(embed=embed)
        
        try:
            await p1.edit(nick='['+ str(get_points(p1.display_name) + 10) +'] ' + p1.name)
        except:
            print('cant change nick for p1')
        try:
            await p2.edit(nick='['+ str(get_points(p1.display_name) - 10) +'] ' + p2.name)
        except:
            print('cant change nick for p2')

        fights.remove(p1)
        fights.remove(p2)
        await channel.delete()
    if payload.emoji.name == '💩':
        p1 = discord.utils.find(lambda m: m.id == int(get_p1(channel.topic)), guild.members)
        p2 = discord.utils.find(lambda m: m.id == int(get_p2(channel.topic)), guild.members)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.count <= 2 and reaction.emoji == '💩':
                return
        print('Победил p2')
        embed=discord.Embed(title="CIS Creative", description="Результаты боксфайта:")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
        embed.add_field(name="Победитель:", value=p2.name + " (+10)", inline=False)
        embed.add_field(name="Проигравший:", value=p1.name + " (-10)", inline=False)
        await p2.send(embed=embed)
        await p1.send(embed=embed)
        try:
            await p2.edit(nick='['+ str(get_points(p2.display_name) + 10) +'] ' + p2.name)
        except:
            print('cant change nick for p2')

        try:
            await p1.edit(nick='['+ str(get_points(p1.display_name) - 10) +'] ' + p1.name)
        except:
            print('cant change nick for p1')

        fights.remove(p1)
        fights.remove(p2)
        await channel.delete()

client.run(TOKEN)
