import requests
import os
from dotenv import load_dotenv
import discord
load_dotenv()

YOUR_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}

async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content





# Create a Discord client
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print("Type '!imagine <prompt>' to send an image.")

@client.event
async def on_message(message):
    # Check if the message author is not a bot
    if not message.author.bot:
        # Check if the message contains a command to send an image
        if message.content.startswith('!imagine'):
            # recieved message: !send_image <image file path>
            print("Recieved message: ", message.content)

            # Extract the image file path from the message content
            inputs = message.content[len('!imagine'):].strip()
            image_bytes = await query({
                "inputs": inputs,
            })
            print("Called API")
            # You can access the image with PIL.Image for example
            import io
            from PIL import Image
            image = Image.open(io.BytesIO(image_bytes))
            image_path = "./tmp/image.png"
            image.save(image_path)

            try:
                # Open the image file
                with open(image_path, 'rb') as f:
                    # Create a Discord file object to send the image
                    image_attachment = discord.File(f)

                    # Send the image as a message
                    await message.channel.send(file=image_attachment)
            except FileNotFoundError:
                await message.channel.send("Image file not found.")


# Replace 'YOUR_BOT_TOKEN' with your Discord bot token
client.run(YOUR_BOT_TOKEN)

