import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta

# Set the token and channel ID
TOKEN = "MTIxOTI1MTAwMzE1MzcxMTEyNA.G6VM-g.ItOVIHV1qevVwyszkw3hje059-dC3vBt7jKdD4"
CHANNEL_ID = "1161347892070596702"

# Create a bot instance with the appropriate intents
intents = discord.Intents.default()
intents.presences = False
intents.members = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to calculate time until the next event
def get_time_until_next_event():
    # Get the current time in UTC
    current_time = datetime.utcnow()

    # Set the target time for the first event at 17:00 UTC
    target_time = current_time.replace(hour=17, minute=0, second=0, microsecond=0)

    # If the current time is after the first event, set the target time to the next day
    if current_time > target_time:
        target_time += timedelta(days=1)

    # Calculate the time difference until the next event (every 4 hours)
    while (target_time - current_time).total_seconds() > 7200:  # 2 hours
        target_time -= timedelta(hours=4)

    time_until_event = target_time - current_time

    return time_until_event

# Function to format time duration in a human-readable format
def format_timedelta(td):
    seconds = td.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

# Background task to update the countdown
async def update_countdown():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(CHANNEL_ID))
    
    while not bot.is_closed():
        # Get the time until the next event
        time_until_event = get_time_until_next_event()

        # Format the time until the event
        formatted_time = format_timedelta(time_until_event)

        # Send the formatted time to the channel
        await channel.send(f"Time until the next event: {formatted_time}")

        # Wait for 1 minute before updating again
        await asyncio.sleep(60)

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print('Bot is ready!')
    bot.loop.create_task(update_countdown())

# Run the bot
bot.run(TOKEN)
