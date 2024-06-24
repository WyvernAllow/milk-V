import nextcord
from nextcord.ext import commands

import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

discord_bot_token = os.getenv('DISCORD_BOT_TOKEN');

bot = commands.Bot()

test_txt = '''
    Hello, World! This is a test message which has to be somewhat longer than just hello world so that I can see if the artificial typing works.
'''

awake_probability = 1 / 6

def calculate_time_to_write(sentence: str, wpm: int):
    word_count = len(sentence.split())
    time_to_write_seconds = (word_count / wpm) * 60
    return time_to_write_seconds

@bot.slash_command(description="Replies with pong!")
async def ping(interaction: nextcord.Interaction):
    await interaction.send("Pong!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.offline)

@bot.event
async def on_message(message: nextcord.Message):
    if message.author == bot.user:
        return
    
    global awake_probability
    
    if bot.user.mentioned_in(message):
        if random.random() < awake_probability:
            print('No longer ignoring mention. Going online...')
            await bot.change_presence(status=nextcord.Status.online)
            
            await asyncio.sleep(random.randint(3, 10))

            async with message.channel.typing():
                input_string = test_txt
                
                wpm = random.randint(90, 110)
                time_to_write = calculate_time_to_write(input_string, wpm)

                print(f'Typing for {time_to_write} seconds at {wpm} words per minute')

                await asyncio.sleep(time_to_write)

                await message.channel.send(input_string)

        else:
            # The more you spam her, the more likely she is to wake up
            awake_probability = awake_probability + (1 / 6)
            print(f'Ignorning message. New probablity {awake_probability * 100}%')

bot.run(discord_bot_token)