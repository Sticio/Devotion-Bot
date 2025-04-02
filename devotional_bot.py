import discord
from discord.ext import commands, tasks
import csv
import datetime
import asyncio
import os
import json
import calendar
from dotenv import load_dotenv
import random
import pytz

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure message content is enabled
client = commands.Bot(command_prefix="!", intents=intents)

# File to store the chosen channels
CHANNEL_FILE = "channel.json"

def load_channels():
    if os.path.exists(CHANNEL_FILE):
        with open(CHANNEL_FILE, "r") as file:
            return json.load(file)  # Load all saved channels
    return {}

def save_channel(guild_id, channel_id):
    channels = load_channels()
    channels[str(guild_id)] = channel_id  # Save by guild ID (as string)
    with open(CHANNEL_FILE, "w") as file:
        json.dump(channels, file)

# Load quotes from CSV file
def load_quotes(filename="Quotes.csv"):
    quotes = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quotes.append(row)
    return quotes

quotes = load_quotes()

# Get the quote of the day based on day of the year
def get_today_quote():
    today = datetime.datetime.now()
    day_of_year = today.timetuple().tm_yday
    year = today.year

    if calendar.isleap(year):
        if day_of_year == 60:
            index = 58
        elif day_of_year > 60:
            index = day_of_year - 2
        else:
            index = day_of_year - 1
    else:
        index = day_of_year - 1

    index = index % len(quotes)
    quote_data = quotes[index]

    return quote_data["Quote"], quote_data["Author"]

# Easter egg quotes
hayman_quotes = [
    "I gave her the awkward white boy smile - Br. Lucas Miller",
    "Oh me, Oh my, or HAYMAN - Br. Lucas Miller",
    "Preacher you’re casting stones. Well learn to duck - The Rev. Doug McClung",
    "Pride didn't stop you from leaving so it shouldn’t stop you from coming back - The Rev. Doug McClung",
    "They ain’t nobody more old time than I am. I give Tony Hutson a run for his money - Br. Micah Renfrow",
    "You better thank God your kids go to a God fearing church- Rev. Doug McClung on Catholic Pedos",
]

@client.command(name="hayman")
async def hayman(ctx):
    random_quote = random.choice(hayman_quotes)
    await ctx.send(random_quote)

# Send the daily devotional
async def send_daily_devotional():
    await client.wait_until_ready()
    channels = load_channels()

    for guild_id, channel_id in channels.items():
        channel = client.get_channel(int(channel_id))
        if channel:
            quote, author = get_today_quote()
            embed = discord.Embed(
                title="📖 Daily Devotional",
                description=f'**"{quote}"**\n\n— *{author}*',
                color=discord.Color.blue()
            )
            embed.set_footer(text="Sent automatically at 9 AM EST")
            await channel.send(embed=embed)
            print(f"✅ Daily devotional sent to {channel.name} in {guild_id}.")
        else:
            print(f"⚠️ Could not find channel {channel_id} in guild {guild_id}.")

# Check the time every minute
@tasks.loop(minutes=1)
async def schedule_task():
    now = datetime.datetime.now(pytz.timezone("US/Eastern"))
    print(f"⏳ Checking time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    if now.hour == 9 and now.minute == 0:
        print("🚀 Sending daily devotional...")
        await send_daily_devotional()

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user.name}")

    # Ensure task loop runs only once
    if not schedule_task.is_running():
        schedule_task.start()
        print("📅 Daily devotional scheduler started.")

# Manually trigger the devotional
@client.command(name="devotional")
async def devotional(ctx):
    quote, author = get_today_quote()
    embed = discord.Embed(
        title="📖 Daily Devotional",
        description=f'**"{quote}"**\n\n— *{author}*',
        color=discord.Color.blue()
    )
    embed.set_footer(text="Requested manually")
    await ctx.send(embed=embed)

# Set the channel for daily devotionals
@client.command(name="setchannel")
async def set_channel(ctx):
    print(f"📌 Channel set by {ctx.author} in {ctx.guild.name}")
    save_channel(ctx.guild.id, ctx.channel.id)
    await ctx.send(":white_check_mark: This channel is now set for daily devotionals!")

client.run(TOKEN)
