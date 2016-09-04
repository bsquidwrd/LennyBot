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

client.run(credentials.token)