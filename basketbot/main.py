import asyncio
import time
from datetime import datetime

import discord

from meet import Meet, DATE_PATTERN


ALERT = 5   # Minutes

client = discord.Client()

meets = []


def parse_meet(parts):
    meet = Meet(parts[1], parts[2]+" "+parts[3])
    return meet


@client.event
async def on_ready():
    print("BasketBot started.")

    while True:
        await asyncio.sleep(1)
        now = time.time()

        for meet in meets:
            if len(meet.people) > 0 and not meet.alerted:
                t = meet.time.timestamp()
                if 0 <= t-now < ALERT*60:
                    msg = f"Meet {meet.as_str()} starting in {ALERT} minutes."
                    msg = f"{meet.channel.guild.default_role} {msg}"
                    meet.alerted = True
                    await meet.channel.send(msg)

        for i, meet in enumerate(meets):
            if now >= meet.time.timestamp():
                meets.pop(i)
                break


@client.event
async def on_message(msg):
    pinged = False
    for m in msg.mentions:
        if m.bot == True and m.name == "BasketBot":
            pinged = True
            break

    if pinged:
        parts = msg.content.split()[1:]
        subcmd = "help" if len(parts) == 0 else parts[0]

        if subcmd == "help":
            data = "BasketBot help:\n"
            data += "- @BasketBot help: Show this help message.\n"
            data += "- @BasketBot list: List pending meets.\n"
            data += "- @BasketBot add location date: Add a meet.\n"
            data += "- @BasketBot yes location date: You can go to a meet.\n"
            data += "- @BasketBot no location date: You can't go to a meet.\n"
            data += "Locations are words with no spaces.\n"
            data += "Dates are of the format \"4/24 17:30\""
            await msg.channel.send(data)

        elif subcmd == "list":
            data = "Meets:\n"
            for meet in meets:
                data += f"- {meet.as_str()}: "
                for p in meet.people:
                    data += f"{p}, "
                data += "\n"

            await msg.channel.send(data)

        elif subcmd == "add":
            if len(parts) < 4:
                await msg.reply("Invalid command format.")
            else:
                try:
                    meet = parse_meet(parts)
                    meet.channel = msg.channel
                except ValueError:
                    await msg.reply("Error parsing time.")
                else:
                    meets.append(meet)
                    await msg.channel.send(f"Added meet: {meet.as_str()}.")

        elif subcmd == "yes":
            if len(parts) < 4:
                await msg.reply("Invalid command format.")
            else:
                try:
                    meet = parse_meet(parts)
                except ValueError:
                    await msg.reply("Error parsing time.")
                else:
                    for m in meets:
                        if m == meet:
                            m.people.add(msg.author.name)
                            await msg.reply("Added you to meet.")
                            break
                    else:
                        await msg.reply("Meet not found.")

        elif subcmd == "no":
            if len(parts) < 4:
                await msg.reply("Invalid command format.")
            else:
                try:
                    meet = parse_meet(parts)
                except ValueError:
                    await msg.reply("Error parsing time.")
                else:
                    for m in meets:
                        if m == meet:
                            m.people.remove(msg.author.name)
                            await msg.reply("Removed you from meet.")
                            break
                    else:
                        await msg.reply("Meet not found.")

        else:
            await msg.reply(f"Unknown command: {subcmd}")


if __name__ == "__main__":
    with open("token.txt", "r") as fp:
        token = fp.read().strip()
    client.run(token)
