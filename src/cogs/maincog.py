import discord
from discord.ext import commands
import json
from pprint import pprint

def setup(bot):
    bot.add_cog(MainCog(bot))

class MainCog(commands.Cog):
    def __init__(self, bot):
        with open('config.json') as file:
            config = json.load(file)
        self.bot = bot
        self.specialties = config['specialties']
        self.mute_list = []

    async def send_help_embed(self, ctx):
            pprint(vars(self))
            pprint(vars(ctx))
            embed = discord.Embed(title="Specialties",  description="redBot can manage your specialties ", color=0xff0000)
            embed.add_field(name="list", value="type **$specialties list** to get the list of specialties",  inline=False)
            embed.add_field(name="get", value="type **$specialties get [specialty1 specialty2 ...]** to get specialties",  inline=False)
            embed.add_field(name="remove", value="type **$specialties remove [specialty1 specialty2 ...]** to remove specialties",  inline=False)
            await ctx.send(embed=embed)
            

    @commands.command()
    async def specialties(self, ctx, *, message = None):
        if message is None:
            await self.send_help_embed(ctx)
            return
        params = message.split()
        if params[0] == 'list':
            embed = discord.Embed(title="Available specialties", description="These are the specialties you can get",
                                  color=0xff0000)
            for index, specialty in enumerate(self.specialties):
                embed.add_field(name=index, value='**'+specialty+'**', inline=False)
            await ctx.send(embed=embed)
        if params[0] == 'get':
            params = params[1:]
            added_specialties = []
            unknown_specialties = []
            for param in params:
                param = param.capitalize()
                if param in self.specialties:
                    added_specialties.append(param)
                    specialty = discord.utils.get(message.author.guild.roles, name=param)
                    await author.add_roles(specialty)
                else:
                    unknown_specialties.append(param)
            await ctx.send(('Roles ' + repr(added_specialties) + ' were added to ' + author.name) if len(
                added_specialties) > 0 else 'No ranks were added')
            if len(unknown_specialties) > 0:
                await ctx.send(('Roles ' + repr(unknown_specialties) + ' are unknown '))
        elif params[0] == 'remove':
            params = params[1:]
            added_specialties = []
            unknown_specialties = []
            for param in params:
                param = param.capitalize()
                if param in self.specialties:
                    added_specialties.append(param)
                    specialty = discord.utils.get(author.guild.roles, name=param)
                    await author.remove_roles(specialty)
                else:
                    unknown_specialties.append(param)
            await ctx.send(('Roles ' + repr(added_specialties) + ' were removed from ' + author.name) if len(
                added_specialties) > 0 else 'No ranks were added')
            if len(unknown_specialties) > 0:
                await ctx.send(('Roles ' + repr(unknown_specialties) + ' are unknown '))

    async def on_message(self, message):
        content = message.content
        channel = message.channel
        author = message.author
        if author in self.mute_list:
            self.delete_message(message)
            return
        if channel.name != 'bot':
            return
        if not content.startswith('$'):
            return
        content = content[1:]
        if author == self.user:
            return

        print(content)
        if content.startswith('help'):
            embed = discord.Embed(title="Commands", description="redBot is here to help", color=0xff0000)
            embed.add_field(name="specialties", value="type **$specialties** for help about specialties", inline=False)
            await channel.send(embed=embed)
           

    

