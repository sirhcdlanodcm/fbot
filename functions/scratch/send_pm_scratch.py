import discord
import random
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

bot = commands.Bot(command_prefix='!')

# List of user IDs as strings. Replace these with actual user IDs.
user_ids = [690043477374795826]

scheduler = AsyncIOScheduler()

async def send_random_user_dm():
    user_id = random.choice(user_ids)  # Pick a random user ID from the list.
    user = await bot.fetch_user(user_id)  # Fetch the User object.
    await user.send("Your daily message!")  # Send a DM to the user.

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Schedule the task to run daily. Adjust the hour and minute according to your needs.
    # scheduler.add_job(send_random_user_dm, 'cron', hour=12, minute=0)
    scheduler.add_job(send_random_user_dm, 'interval', minutes=1)
    scheduler.start()

@bot.command(name='testdm', help='Sends a test DM to a random user from the list.')
async def test_dm(ctx):
    await send_random_user_dm()
    await ctx.send("Sent a test DM to a random user.")

bot.run('paste private bot key here')