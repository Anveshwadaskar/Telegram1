import discord
from discord.ext import commands
from telegram import Bot
import asyncio
import websockets

# Discord configuration
discord_token = "DISCORD_TOKEN"
discord_channel_ids = [123456789012345678, 987654321098765432] 

# Telegram configuration
telegram_token = "TELEGRAM_BOT_TOKEN"
telegram_channel_ids = {"discord_channel_id": -1001234567890} 

# Discord client
intents = discord.Intents.default()
intents.message_content = True
intents.message_embeds = True
client = commands.Bot(command_prefix="!", intents=intents)

# Telegram bot
telegram_bot = Bot(token=telegram_token)

async def forward_to_telegram(message):
    
    content = message.content
    images = [attachment.url for attachment in message.attachments if attachment.url.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    embeds = message.embeds

   
    combined_content = f"{content}\n\n" if content else ""
    for embed in embeds:
        combined_content += f"{embed.title}\n{embed.description}\n"

    
    for telegram_channel_id in telegram_channel_ids.values():
        for image in images:
            telegram_bot.send_photo(chat_id=telegram_channel_id, photo=image, caption=combined_content)
        else:
            telegram_bot.send_message(chat_id=telegram_channel_id, text=combined_content)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@client.event
async def on_message(message):
    if message.channel.id in discord_channel_ids:
        await forward_to_telegram(message)

# Discord connection
async def discord_connection():
    await client.start(discord_token)

# Telegram connection
async def telegram_connection():
    await telegram_bot.send_message(chat_id=telegram_channel_ids["discord_channel_id"], text="Connected to Discord")


async def main():
    while True:
        try:
            await asyncio.gather(discord_connection(), telegram_connection())
        except (discord.DiscordException, websockets.exceptions.WebSocketException) as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(5)  

if __name__ == "__main__":
    asyncio.run(main())
