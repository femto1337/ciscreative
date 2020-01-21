import discord
from discord.ext import commands
import random
from random import randint
import json

queue = []
fights = []
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

def check_points(member, guild):
    pts = get_points(member.display_name)
    opendiv = discord.utils.find(lambda r: r.id == 668152509088399370, guild.roles)
    contenderdiv = discord.utils.find(lambda r: r.id == 668152388959469596, guild.roles)
    masterdiv = discord.utils.find(lambda r: r.id == 668153566766301186, guild.roles)
    championdiv = discord.utils.find(lambda r: r.id == 668153990994722832, guild.roles)
    if (pts >= 10) and (pts <= 59):
        member.add_roles(opendiv)
    elif (pts >= 60) and (pts <= 99):
        member.add_roles(contender)
    elif (pts >= 100) and (pts <= 199):
        member.add_roles(masterdiv)
    elif (pts >= 200):
        member.add_roles(championdiv)

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
        
@client.command()	
async def closefight(ctx, member: discord.Member):	
    if member in queue:	
        queue.remove(ctx.member)	
    elif member in fights:	
        fights.remove(member)

@client.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)
    user = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    print('on_raw_reaction_clear')
    if payload.channel_id == 668140694996779072:
        print('reaction removed')
        queue.remove(user)
        await user.send('Вы отменили поиск.')

@client.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)
    user = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    channel = discord.utils.find(lambda c: c.id == payload.channel_id, guild.channels)

    #Проверка на новичка
    if not user.display_name.startswith("["):
        try:
            await user.edit(nick='[0] ' + user.name)
        except:
            print('cant add [0] to ' + user.name)

    #Проверка на бота
    if payload.user_id == 668040788482981899:
        return

    #проверка на канал поиска боксфайтов
    if payload.channel_id == 668140694996779072:
        
        #проверка на очередь и файты
        if (user in fights) or (user in queue):
            await user.send('Вы уже ищете боксфайт.')
            return
        
        queue.append(user)

        #очередь больше или равна двум
        if len(queue) >= 2:
            print('queue >= 2')
            
            queue.remove(user)
            
            oponnent = queue[random.randint(0,len(queue)) - 1]
            
            #если искавший = опонненту
            if user == oponnent:
                await user.send('Произошла ошибка. Попробуйте ещё раз.')
                queue.remove(user)
                return
            
            #если кто то из них бот
            if (user == client.user) and (oponnent == client.user):
                await user.send('Произошла ошибка. Попробуйте ещё раз.')
                queue.remove(user)
                return
            
            queue.remove(oponnent)

            
            #создание боксфайт канала
            overwrites_admin = {
            user.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            oponnent: discord.PermissionOverwrite(read_messages=True)
            }
            boxchannel = await user.guild.create_text_channel('boxfight-' + str(randint(1000, 10000)), overwrites=overwrites_admin, topic=str(payload.user_id) + ' p2 ' + str(oponnent.id))
            embedplayers=discord.Embed(title="CIS Creative", description="Боксфайт.")
            embedplayers.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
            embedplayers.add_field(name="Первый игрок (♥): ", value=user.mention, inline=False)
            embedplayers.add_field(name="Второй игрок (💩): ", value=oponnent.mention, inline=False)
            embedrules=discord.Embed(title="CIS Creative", description="Правила.")
            embedrules.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
            embedrules.add_field(name="Карта:", value="7620-0771-9529", inline=False)
            embedrules.add_field(name="Играете до:", value="3 побед", inline=False)
            msg = await boxchannel.send(embed=embedplayers)
            await boxchannel.send(embed=embedrules)
            await msg.add_reaction('♥')
            await msg.add_reaction('💩')
            ########################

            
            fights.append(user)
            fights.append(oponnent)
    if payload.emoji.name == '♥':
        p1 = discord.utils.find(lambda m: m.id == int(get_p1(channel.topic)), guild.members)
        p2 = discord.utils.find(lambda m: m.id == int(get_p2(channel.topic)), guild.members)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        #проверка на то что голос не один.
        for reaction in message.reactions:
            if reaction.count <= 2 and reaction.emoji == '♥':
                return
        ##################################

        if get_points(p1.display_name) > get_points(p2.display_name)
            diff = get_points(p1.display_name) - get_points(p2.display_name)
        elif:
            diff = get_points(p2.display_name) - get_points(p1.display_name)
            
        if diff > 50:
            ptsforgame = 5
        if diff > 150:
            ptsforgame = 3
        
        #отправить сообщение о результате
        embed=discord.Embed(title="CIS Creative", description="Результаты боксфайта:")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
        embed.add_field(name="Победитель:", value=p1.name + " (+ "+ str(ptsforgame) +" )", inline=False)
        embed.add_field(name="Проигравший:", value=p2.name + " (- "+ str(ptsforgame) +" )", inline=False)
        await p2.send(embed=embed)
        await p1.send(embed=embed)
        #################################

        #изменить никнеймы
        try:
            await p1.edit(nick='['+ str(get_points(p1.display_name) + ptsforgame) +'] ' + p1.name)
        except:
            print('cant change nick for p1')


        try:
            await p2.edit(nick='['+ str(get_points(p2.display_name) - ptsforgame) +'] ' + p2.name)
        except:
            print('cant change nick for p2')
        #################################
        
        #выдача ролей
        check_points(p1, guild)
        check_points(p2, guild)
        ##############

        fights.remove(p1)
        fights.remove(p2)
        await channel.delete()
    if payload.emoji.name == '💩':
        p1 = discord.utils.find(lambda m: m.id == int(get_p1(channel.topic)), guild.members)
        p2 = discord.utils.find(lambda m: m.id == int(get_p2(channel.topic)), guild.members)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        #проверка на то что голос не один.
        for reaction in message.reactions:
            if reaction.count <= 2 and reaction.emoji == '💩':
                return
        ##################################
        if get_points(p1.display_name) > get_points(p2.display_name)
            diff = get_points(p1.display_name) - get_points(p2.display_name)
        elif:
            diff = get_points(p2.display_name) - get_points(p1.display_name)
            
        if diff > 50:
            ptsforgame = 5
        if diff > 150:
            ptsforgame = 3
            


        #отправить сообщение о результате
        embed=discord.Embed(title="CIS Creative", description="Результаты боксфайта:")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/668037249056768020/668166034783600670/Logo_cis_customs.png?width=473&height=473")
        embed.add_field(name="Победитель:", value=p2.name + " (+ "+ str(ptsforgame) +" )", inline=False)
        embed.add_field(name="Проигравший:", value=p1.name + " (- "+ str(ptsforgame) +" )", inline=False)
        await p2.send(embed=embed)
        await p1.send(embed=embed)
        #################################

        #изменить никнеймы
        
        try:
            await p1.edit(nick='['+ str(get_points(p1.display_name) - ptsforgame) +'] ' + p1.name)
        except:
            print('cant change nick for p1')

        try:
            await p2.edit(nick='['+ str(get_points(p2.display_name) + ptsforgame) +'] ' + p2.name)
        except:
            print('cant change nick for p2')
        #################################
        
        
        #выдача ролей
        check_points(p1, guild)
        check_points(p2, guild)
        ##############

        fights.remove(p1)
        fights.remove(p2)
        await channel.delete()

client.run(TOKEN)
