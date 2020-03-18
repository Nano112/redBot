import discord

client = discord.Client()
specialties = ['Computational', 'Java', 'Bedrock', 'Flying-machines', 'Door-making', 'Command-blocks', 'Storage-tech', 'Minigames','Basics','Technical']
mute_list = []
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    content = message.content
    channel = message.channel
    author = message.author
    if author in mute_list:
        client.delete_message(message)
        return
    if channel.name != 'bot':
        return
    if not content.startswith('$'):
        return
    content = content[1:]
    if author == client.user:
        return

    print(content)
    if content.startswith('help'):
        embed = discord.Embed(title="Commands", description="redBot is here to help", color=0xff0000)
        embed.add_field(name="specialties", value="type **$specialties** for help about specialties", inline=False)
        await channel.send(embed=embed)
    if content.startswith('specialties'):
        params = content[len('specialties'):].strip().split()
        print('params:' + repr(params))
        if len(params) == 0:
            embed = discord.Embed(title="Specialties",
                                  description="redBot can manage your specialties ",
                                  color=0xff0000)
            embed.add_field(name="list",
                            value="type **$specialties list** to get the list of specialties",
                            inline=False)
            embed.add_field(name="get",
                            value="type **$specialties get [specialty1 specialty2 ...]** to get specialties",
                            inline=False)
            embed.add_field(name="remove",
                            value="type **$specialties remove [specialty1 specialty2 ...]** to remove specialties",
                            inline=False)
            await channel.send(embed=embed)
        else:
            if params[0] == 'list':
                embed = discord.Embed(title="Available specialties", description="These are the specialties you can get",
                                      color=0xff0000)
                for index, specialty in enumerate(specialties):
                    embed.add_field(name=index, value='**'+specialty+'**', inline=False)
                await channel.send(embed=embed)

            if params[0] == 'get':
                params = params[1:]
                added_specialties = []
                unknown_specialties = []
                for param in params:
                    param = param.capitalize()
                    if param in specialties:
                        added_specialties.append(param)
                        specialty = discord.utils.get(message.author.guild.roles, name=param)
                        await author.add_roles(specialty)
                    else:
                        unknown_specialties.append(param)
                await channel.send(('Roles ' + repr(added_specialties) + ' were added to ' + author.name) if len(
                    added_specialties) > 0 else 'No ranks were added')
                if len(unknown_specialties) > 0:
                    await channel.send(('Roles ' + repr(unknown_specialties) + ' are unknown '))



            elif params[0] == 'remove':
                params = params[1:]
                added_specialties = []
                unknown_specialties = []
                for param in params:
                    param = param.capitalize()
                    if param in specialties:
                        added_specialties.append(param)
                        specialty = discord.utils.get(author.guild.roles, name=param)
                        await author.remove_roles(specialty)
                    else:
                        unknown_specialties.append(param)
                await channel.send(('Roles ' + repr(added_specialties) + ' were removed from ' + author.name) if len(
                    added_specialties) > 0 else 'No ranks were added')
                if len(unknown_specialties) > 0:
                    await channel.send(('Roles ' + repr(unknown_specialties) + ' are unknown '))

            client.run(open('discordToken', "r").read())