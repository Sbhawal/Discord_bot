from discord import Intents
from discord import Embed
from discord.ext.commands import Context
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from glob import glob


from apscheduler.schedulers.asyncio import AsyncIOScheduler
PREFIX = "!"
OWNER_IDS = [372614427373207552]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix = PREFIX, 
						 owner_ids = OWNER_IDS,
						 intents = Intents.all()
						)
	def setup(self):
		for cog in COGS:
			self.load_extension(f'lib.cogs.{cog}')
			print(f'{cog} cog loaded')


	def run(self, version):
		self.VERSION = version
		self.setup()
		with open("./lib/bot/token.0", "r", encoding = "utf-8") as tf:
			self.TOKEN = tf.read()

		print("RUNNING BOT....")
		super().run(self.TOKEN, reconnect = True)


	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			# if message.author.id in self.banlist:
			# 	await ctx.send("You are banned from using commands.")

			if not self.ready:
				await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

			else:
				await self.invoke(ctx)




	async def on_connect(self):
		print("BOT CONNECTED!")



	async def on_disconnect(self):
		print("BOT DISCONNECTED!")



	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(825753375312183387)
			print("Bot Ready")
			self.stdout = self.get_channel(826734157916799006)
			channel = self.get_channel(826768448045842432)
			await self.stdout.send("Now Online")
		else:
			print("Bot reconnected")



	async def on_message(self, message):
		if not message.author.bot: # and message.author !=message.guild.me:
			# print(message.type)
			# if message.content[0] == '!':
				# print(message.content)
				await self.process_commands(message)




	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong!")
		await self.stdout.send("An error occured")
		raise





	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			await self.stdout.send("Invalid Command!")
		elif hasattr(exc, "original"):
			raise exc.original
		else:
			raise exc


bot = Bot()

