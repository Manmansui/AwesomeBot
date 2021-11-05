import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_word = [
    "sad", "unhappy", "depressed", "misserable", "angry", "horrible", "cry",
    "tragic"
]

start_awesomeness = [
    "Cheer up mate!", "Hang in there.", "You are a great person / bot!"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def update_awesomeMessage(awesome_message):
    if "awesomeness" in db.keys():
        awesome = list(db["awesomeness"])
        # awesome = db["awesomeness"]
        awesome.append(awesome_message)
        db["awesomeness"] = awesome
    else:
        db["awesomeness"] = [awesome_message]


def delete_awesomeMessage(index):
    awesome = db["awesomeness"]
    if len(awesome) > index:
        del awesome[index]
        db["awesomeness"] = awesome


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$quote'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        # add choice: start_awesomeness + db
        options = start_awesomeness
        if "awesomeness" in db.keys():
            # options = options + db["awesomeness"]
            options = options + list(db["awesomeness"])
            # options.append(db["awesomeness"])

    # sad word
        if any(word in msg for word in sad_word):
            await message.channel.send(random.choice(options))

# add new awesome message
    if msg.startswith('$newMsg'):
        awesome_message = msg.split("$newMsg ", 1)[1]
        update_awesomeMessage(awesome_message)
        await message.channel.send('New awesome message added!')

# delete awesome message
    if msg.startswith('$delMsg'):
        awesomes = []
        if "awesomeness" in db.keys():
            index = int(msg.split("$delMsg ", 1)[1])
            delete_awesomeMessage(index)
            awesomes = db["awesomeness"]
        await message.channel.send(awesomes)


#list message
    if msg.startswith('$listMsg'):
        messages = []
        if "awesomeness" in db.keys():
            messages = db["awesomeness"]
        await message.channel.send(messages)

    if msg.startswith('$respond'):
        value = msg.split('$respond ', 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is On!")
        elif value.lower() == "false":
            db["responding"] = False
            await message.channel.send("Responding is Off!")

my_token = os.environ['DISCORD_TOKEN']
print(db["awesomeness"])
keep_alive()
client.run(my_token)
