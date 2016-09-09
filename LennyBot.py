import discord
import asyncio
import credentials

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if 'lennyface' in message.content.lower():
        await client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')
        if  message.content.lower() == 'lennyface':
            try:
                await client.delete_message(message)
            except Exception as e:
                print(e)

    if message.channel.is_private:
        if message.author.id == credentials.owner:
            if 'servers' in message.content:
                numServers = 0
                for server in client.servers:
                    numServers+=1

                await client.send_message(message.channel, str(numServers) + ' servers.')


client.run(credentials.token)