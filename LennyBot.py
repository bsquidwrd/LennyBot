import discord
import asyncio
import credentials

client = discord.Client()
logChannel = '310083179052793858' #bot_log

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.change_presence(game=discord.Game(name='@Lenny enabled')) # simple news/update status

@client.event
async def on_message(message):
  if message.author != client.user and not message.author.bot:
    if message.author.id == credentials.owner:
        servers = []
        if 'servers' in message.content.lower():
            numServers = 0
            for server in client.servers:
                numServers+=1
                servers.append(server.name)

            await client.send_message(client.get_channel(logChannel), ', '.join(servers) + ' - ' + str(numServers) + ' servers, ' + str(sum(1 for _ in client.get_all_members())) + ' users.')

    if message.channel.is_private:
        await client.send_message(client.get_channel(logChannel), ':mailbox_with_mail: ' + message.author.name + ' - ' + message.clean_content)
        await client.send_message(message.channel, 'Hello ' + message.author.name + " ( ͡° ͜ʖ ͡°). I don\'t have any commands! I\'m triggered by the phrase lennyface or via " + client.user.mention + ", have a nice day!")

    ## Lennyface send / delete
    if 'lennyface' in message.content.lower() or client.user.mentioned_in(message) and not message.mention_everyone:
        await client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')
        await client.send_message(client.get_channel(logChannel), '[' + message.author.server.name + '] ' + message.author.name + ' - ' + message.clean_content)

        if (message.content.lower() == 'lennyface') or (message.content.lower() == client.user.mention):
            try:
                await client.delete_message(message)
            except Exception as e:
                print(e)

        # Log lenny count
        with open(r'count.txt','r+') as f:
            value = int(f.read())
            f.seek(0)
            f.write(str(value + 1))
            await client.change_presence(game=discord.Game(name='( ͡° ͜ʖ ͡°) - ' + str(value + 1) ))


    elif 'lenny' in message.content.lower():
        await client.send_message(client.get_channel(logChannel), '[' + message.author.server.name + '] ' + message.author.name + ' - ' + message.clean_content)

@client.event
async def on_server_join(server):
   await client.send_message(client.get_channel(logChannel), ':heart: Lenny was added to ' + str(server) + ' - ' + str(sum(1 for e in server.members)))

@client.event
async def on_server_remove(server):
   await client.send_message(client.get_channel(logChannel), ':broken_heart: Lenny was removed from ' + str(server))

client.run(credentials.token)
