import discord
import asyncio
import mysql.connector
import random
import Database
from Database import get_random_paragraph
from discord.ext import commands
from google_images_search import GoogleImagesSearch
from discord.utils import get

gis = GoogleImagesSearch('AIzaSyBL7qarT8cAKLAyhsD9CCUVvZXSgPxXj5I', 'e01b3022d5f9a45c4')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.command()
async def button(ctx):
    view = discord.ui.View()
    button = discord.ui.Button(label="Click me")
    view.add_item(button)
    await ctx.send(view=view)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def kitty(ctx):
    gis.search({'q': 'cute kittens', 'num': 5, 'start': 1})
    results = gis.results()
    if results:
        random.shuffle(results)
        random_image = random.choice(results)
        await ctx.send(random_image.url)
    else:
        await ctx.send("No images found :(")


@bot.command()
async def madlib(ctx):
    # Get a random paragraph and the list of words to search for
    paragraph = get_random_paragraph()
    words_to_search = ["Noun", "Animal", "Verb", "Foods", "Saying", "Color", "Person", "Adjective"]
    found_words = []
    # Search for each word in the paragraph
    for word in paragraph.split():
        # Strip any punctuation from the word
        stripped_word = word.strip(".,!?")
        if stripped_word in words_to_search:
            # If the word is in the list of words to search for, add it to the list of found words
            found_words.append(stripped_word)
    # If there are found words, create a message for the user to fill in the blanks
    if found_words:
        title = "Enter for the following - {}".format(" ".join(found_words))
        description = "Fill in the words below as asked, then hit enter to receive the next word:"
        fields = []
        for word in found_words:
            # Create a field for each found word, prompting the user for input
            fields.append(
                {
                    "name": word,
                    "value": "Please enter a {} here!(hit enter when done)".format(word.lower()),
                    "inline": False
                }
            )
        # Send the initial message with the fields for user input
        message = await ctx.send(embed=discord.Embed(title=title, description=description, color=0xff0000))
        # Replace each found word with the user's input
        for field in fields:
            user_input = await wait_for_text_input(ctx, field["name"], field["value"])
            paragraph = paragraph.replace(field["name"], user_input, 1)
        # Delete the initial message with the fields
        await message.delete()
        # Send the completed madlib
        await ctx.send(paragraph)
    else:
        # If no words were found, send a message to the user
        message = "No words found."
        await ctx.send(message)


async def wait_for_text_input(ctx, name, value):
    # Define a check function to ensure that the input is from the correct user and channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    # Send a message to prompt the user for input
    message = await ctx.send(embed=discord.Embed(title=name, description=value))
    # Wait for the user to input text
    user_input = await bot.wait_for("message", check=check)
    return user_input.content



@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.close()

@bot.command()
async def help(ctx):
    message = "I am here to help!"
    await ctx.author.send(message)



bot.run('MTA5MDgwMzQ3ODA5NzU2NzgyNQ.GPTtnX.CpQ6eWNKRUueC-PiodGiRSNV_W6yZvDOIVDgbQ')