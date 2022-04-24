import discord

client = discord.Client()


@client.event
async def on_ready():
    print("BasketBot started.")


@client.event
async def on_message(msg):
    pinged = False
    for m in msg.mentions:
        if m.bot == True and m.name == "BasketBot":
            pinged = True
            break

    if pinged:
        await msg.channel.send("You pinged me.")


if __name__ == "__main__":
    with open("token.txt", "r") as fp:
        token = fp.read().strip()
    client.run(token)
