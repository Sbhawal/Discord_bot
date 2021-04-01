from discord.ext.commands import Cog
from discord.ext.commands import command
import requests
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import io

from PIL import Image

def ocr(url):
	response = requests.get(url)
	img = Image.open(io.BytesIO(response.content))
	text = pytesseract.image_to_string(img)
	return text


class Ocr(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command()
	async def ocr(self, ctx):
		try:
			channel = self.bot.get_channel(ctx.message.reference.channel_id)
			message = await channel.fetch_message(ctx.message.reference.message_id)
			try:
				url = message.attachments[0].url
				text = ocr(url)
				await ctx.message.reply(text)
			except:
				await ctx.message.reply('Not a valid image !')
		except:
			await ctx.message.reply('Attach a valid image for ocr as "reply" like I did!')	



def setup(bot):
	bot.add_cog(Ocr(bot))



