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
            embed = discord.Embed(title="Specialties",  description="redBot can manage your specialties ", color=0xff0000)
            embed.add_field(name="list", value="type **$specialties list** to get the list of specialties",  inline=False)
            embed.add_field(name="get", value="type **$specialties get [specialty1 specialty2 ...]** to get specialties",  inline=False)
            embed.add_field(name="remove", value="type **$specialties remove [specialty1 specialty2 ...]** to remove specialties",  inline=False)
            await ctx.send(embed=embed)

    async def list_specialties(self, ctx):
        embed = discord.Embed(title="Available specialties", description="These are the specialties you can get", color=0xff0000)
        for index, specialty in enumerate(self.specialties):
            embed.add_field(name=index, value='**'+specialty+'**', inline=False)
        await ctx.send(embed=embed)
    
    async def get_specialty(self, ctx, params):
        author = ctx.message.author
        params = params[1:]
        added_specialties = []
        unknown_specialties = []
        message = ""
        for param in params:
            param = param.capitalize()
            if param in self.specialties:
                added_specialties.append(param)
                specialty = discord.utils.get(author.guild.roles, name=param)
                await author.add_roles(specialty)
            elif param.isdecimal():
                if int(param) < len(self.specialties):
                    param_from_index = self.specialties[int(param)]
                    added_specialties.append(param_from_index)
                    specialty = discord.utils.get(author.guild.roles, name=param_from_index)
                await author.add_roles(specialty)
            else:
                unknown_specialties.append(param)
        message += ('Roles ' + repr(added_specialties) + ' were added to ' + author.name) if len(
            added_specialties) > 0 else 'No ranks were added'
        
        if len(unknown_specialties) > 0:
            message += ('\nRoles ' + repr(unknown_specialties) + ' are unknown ')
        await ctx.send(message)
        
    async def remove_specialty(self, ctx, params):
        author = ctx.message.author
        params = params[1:]
        added_specialties = []
        unknown_specialties = []
        message = ""
        for param in params:
            param = param.capitalize()
            if param in self.specialties:
                added_specialties.append(param)
                specialty = discord.utils.get(author.guild.roles, name=param)
                await author.remove_roles(specialty)
            elif param.isdecimal():
                if int(param) < len(self.specialties):
                    param_from_index = self.specialties[int(param)]
                    added_specialties.append(param_from_index)
                    specialty = discord.utils.get(author.guild.roles, name=param_from_index)
                await author.remove_roles(specialty)
            else:
                unknown_specialties.append(param)
         message += ('Roles ' + repr(added_specialties) + ' were removed from ' + author.name) if len(
            added_specialties) > 0 else 'No ranks were added'
        if len(unknown_specialties) > 0:
             message += ('Roles ' + repr(unknown_specialties) + ' are unknown ')
        await ctx.send(message)

    @commands.command()
    async def specialties(self, ctx, *, message = None):
        if message is None:
            await self.send_help_embed(ctx)
            return
        params = message.split()
        sub_command = params[0]
        if sub_command == 'list':
            await self.list_specialties(ctx)
            return
        elif sub_command == 'get':
            await self.get_specialty(ctx, params)
            return
        elif sub_command == 'remove':
            await self.remove_specialty(ctx, params)

            
    

