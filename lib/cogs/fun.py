from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	# @Cog.listener()
	# async def on_ready(self):
	# 	await self.bot.stdout.send("cog ready")

	@command()
	async def ping(self, ctx):
		print("called function")
		await ctx.send(f'Ping is ms')


def setup(bot):
	bot.add_cog(Fun(bot))