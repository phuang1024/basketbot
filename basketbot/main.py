import discord

client = discord.Client()


if __name__ == "__main__":
    with open("token.txt", "r") as fp:
        token = fp.read().strip()
    client.run(token)
