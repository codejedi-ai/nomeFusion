import requests
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from PIL import Image, UnidentifiedImageError
import io

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print('Bot is ready')
    channel_id = 1096850050988114040  # Replace YOUR_CHANNEL_ID with the DM channel ID
    channel = await bot.fetch_channel(channel_id)
    if channel:
        await channel.send("This is a direct message sent by the bot.")
    else:
        print("Channel not found.")

@bot.command()
async def imagine(ctx, *, inputs):
    await ctx.send("Received message: " + inputs)

    # Call the API and get the image bytes
    response = await query({"inputs": inputs})
    image_bytes = response.content

    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Process the image here
        # ...
    except UnidentifiedImageError:
        await ctx.send("Sorry, the image could not be generated. It may be NSFW.")
        return

    image_path = "./tmp/image.png"

    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    
    image.save(image_path)

    try:
        with open(image_path, 'rb') as f:
            image_attachment = discord.File(f)
            await ctx.send(file=image_attachment)
    except FileNotFoundError:
        await ctx.send("Image file not found.")

async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

# Replace 'YOUR_BOT_TOKEN' with your Discord bot token
bot.run(os.getenv("DISCORD_TOKEN"))
