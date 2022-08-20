import discord
import os
from discord.ext import commands
from discord import Option
import datetime
import requests
import json


TOKEN = os.getenv("DISCORD_TOKEN")
LOG = 'none'
intents = discord.Intents.all()
BREAK = 1010549847612457041 
staff = 1010549171025105008
global staff_break
global staff_id
global staff_role
staff_break = []
staff_id = []
staff_role = []
staff_server = 988184113250959401

bot = commands.Bot(status=discord.Status.dnd, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
	print('Bot is ready')

##########################################################################

@bot.slash_command(description='test', guild_ids=[983839961025507350,988184113250959401])
async def test(ctx):
	await ctx.respond('hello')


@bot.slash_command(description='Check the Ping!', guild_ids=[983839961025507350,988184113250959401])
async def ping(ctx):
	embed = discord.Embed(title=f"🏓 Pong! {round(bot.latency * 1000)}ms", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command(description='Delets messages', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    manage_messages=True
)
async def purge(ctx, 
	amount:Option(int, 'Number of messages you want to delete', required=True)):
	try:
		await ctx.channel.purge(limit=int(amount))
		embed = discord.Embed(title=f"{str(amount)} messages has been purged!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		await ctx.respond(embed=embed, ephemeral=True)
	except:
		await ctx.respond('Not enough perms or an Error occured',ephemeral=True)


@bot.slash_command(description='Timeouts a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    manage_messages=True
)
async def timeout(ctx,
	member:Option(discord.Member, 'The Member you want to timeout', required=True),
	minutes:Option(int, 'Number of minutes you want to time out', required=True)):
	try:
		if minutes > 36000:
			await ctx.respond('Cant timeout for more than 25 days!', ephemeral=True)
		else:
			duration = datetime.timedelta(minutes=int(minutes))
			await member.timeout_for(duration)
			embed = discord.Embed(title="Timeout!", description=f"{member.mention} has been timed out!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			embed.add_field(name="Time left for the timeout:", value=str(minutes)+' minutes', inline=False)
			await ctx.respond(embed=embed)
	except:
		await ctx.respond('Not enough perms or an Error occured',ephemeral=True)


@bot.slash_command(description='Removes Timeout from a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    manage_messages=True
)
async def rem_timeout(ctx,
	member:Option(discord.Member, 'The Member you want to remove timeout from', required=True)):
	try:
		if False:
			await ctx.respond('Cant timeout for more than 25 days!', ephemeral=True)
		else:
			await member.remove_timeout()
			embed = discord.Embed(title="Removed Timeout!", description=f"{member.mention} has been removed from timeout!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			await ctx.respond(embed=embed)
	except:
		await ctx.respond('Not enough perms or an Error occured',ephemeral=True)


@bot.slash_command(description='Removes Timeout from a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    kick_members=True
)
async def kick(ctx,
	member:Option(discord.Member, 'The Member you want to kick', required=True),
	reason:Option(str, 'Reason you want to kick the memeber', required=False, default='Not Specified')):
	try:
		guild = ctx.guild
		embed = discord.Embed(title="Kicked!", description=f"{member.mention} has been kicked!!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		embed.add_field(name="Reason: ", value=reason, inline=False)
		await guild.kick(user=member, reason=reason)
		await ctx.respond(embed=embed)
	except:
		await ctx.respond('Not enough perms or an Error occured',ephemeral=True)


@bot.slash_command(description='Bans a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    kick_members=True
)
async def ban(ctx,
	member:Option(discord.Member, 'The Member you want to ban', required=True),
	reason:Option(str, 'Reason you want to ban the memeber', required=False, default='Not Specified')):
	try:
		guild = ctx.guild
		embed = discord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		embed.add_field(name="Reason: ", value=reason, inline=False)
		embed.add_field(name=f"ID:",value=member.id, inline=False)
		await guild.ban(user=member, reason=reason)
		await ctx.respond(embed=embed)
	except:
		await ctx.respond('Not enough perms or an Error occured',ephemeral=True)

@bot.slash_command(description='Unbans a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    kick_members=True
)
async def unban(ctx,
	member:Option(str, 'The id of the Member you want to unban', required=True)):
	try:
		member = int(member)
		guild = ctx.guild
		member = await bot.fetch_user(member)
		embed = discord.Embed(title="Unbanned!", description=f"{member.mention} has been unbanned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		await guild.unban(user=member)
		await ctx.respond(embed=embed)
	except:
		await ctx.respond('Not enough perms or an Error occured',ephemeral=True)


@bot.slash_command(description='DMs a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    manage_messages=True
)
async def dm(ctx,
	member:Option(discord.Member, 'The Member you want to DM', required=True),
	message:Option(str, 'Message', required=True)):
	try:
		user = bot.get_user(int(member.id))
		await user.send(message)
		await ctx.respond('Message successfully sent',ephemeral=True)
	except:
		await ctx.respond('An error occured',ephemeral=True)

@bot.slash_command(description='Hire a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    administrator=True,
)
async def hire(ctx,
	member:Option(str, 'The id of the member you want to hire', required=True),
	role:Option(discord.Role, 'The role you want to give', required=True)):
	member = int(member)
	try:
		guild = ctx.guild
		role = guild.get_role(role.id)
		user = guild.get_member(member)
		await user.add_roles(role)
	finally:
		if member in staff_id:
			return
		staff_id.append(member)
		staff_role.append(role.id)
		await ctx.respond('Member has been successfully hired', ephemeral=True)
		await user.send('You have been hired in '+guild.name+'. as '+role.name)


@bot.slash_command(description='Fire a member', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    administrator=True,
)
async def fire(ctx,
	member:Option(discord.Member, 'The member you want to Fire', required=True),
	reason:Option(str, 'The reason you want fire', required=True),
	role:Option(discord.Role, 'The role you want to fire', required=True)):
	user = bot.get_user(int(member.id))
	guild = ctx.guild
	role = guild.get_role(role.id)
	await member.remove_roles(role)
	try:
		i = staff_id.index(member.id)
		staff_id.pop(i)
		staff_role.pop(i)
	finally:
		await user.send('You have been Fired in '+guild.name+'. Reason: '+reason)
		await ctx.respond('Member has been successfully Fired', ephemeral=True)

@bot.slash_command(name='break', description='Go on a break!', guild_ids=[983839961025507350,988184113250959401])
@discord.default_permissions(
    manage_messages=True
)
async def breakk(ctx,
	reason:Option(str, 'The reason you want break', required=True),
	time:Option(int, 'Number of minutes you want break', required=True)):
	if ctx.author.id in staff_break:
		await ctx.respond('You are already in break!', ephemeral=True)
	else:
		try:
			guild = ctx.guild
			role = guild.get_role(BREAK)
			await ctx.author.add_roles(role)
			staff_break.append(int(ctx.author.id))
			await ctx.respond('You can now go on a break!', ephemeral=True)
			embed=discord.Embed(title="Staff Break!", description=f"{ctx.author} is on break!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			embed.add_field(name=f"Reason:", value=reason, inline=True)
			embed.add_field(name=f"Time", value=f"{time} minutes", inline=False)
			await ctx.send(embed=embed)
		except:
			await ctx.respond('An error occured', ephemeral=True)


@bot.slash_command(description='Report a staff', guild_ids=[983839961025507350,988184113250959401])
async def staff_report(ctx,
	member:Option(discord.Member, 'The member you want to Report', required=True),
	reason:Option(str, 'The reson you want to report', required=True)):
	try:
		embed=discord.Embed(title="Staff Report", description=f"Reported by {ctx.author}", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		embed.add_field(name=f"Report for : {member}", value=reason, inline=False)
		embed.set_thumbnail(url=str(member.display_avatar))
		channel = bot.get_channel(staff)
		await channel.send(embed=embed)
		await ctx.respond('Report sent successfully!', ephemeral=True)
	except:
		await ctx.respond('An error occured', ephemeral=True)

#############################################################################################################
@bot.listen('on_message')
async def on_message(message):
	if message.author != bot.user:
		result = requests.get('https://www.purgomalum.com/service/containsprofanity?text='+message.content)
		if result.text == 'true':
			text = str(requests.get('https://www.purgomalum.com/service/json?text='+message.content.replace(' ', '%20')).text)
			text = json.loads(texst)
			await message.delete()
			embed = discord.Embed(title="Inappropriate message detected", description='Sent by '+message.author.name)
			embed.add_field(name='Bad words removed text', value=text["result"].replace('*','#'))
			embed.set_thumbnail(url=str(message.author.display_avatar))
			await message.channel.send(embed=embed, delete_after=10.0)

		if message.author.id in staff_break:
			guild = message.guild
			role = guild.get_role(BREAK)
			await message.author.remove_roles(role)
			staff_break.remove(message.author.id)
			await message.channel.send(f'Hope you enjoyed your break {message.author.name} :)')

@bot.event
async def on_member_join(member):
	if member.guild.id == staff_server:
		if member.id in staff_id:
			i = staff_id.index(member.id)
			guild = member.guild
			role = guild.get_role(staff_role[i])
			await member.add_roles(role)
			staff_id.pop(i)
			staff_role.pop(i)


############################################################################################################




bot.run(TOKEN)
