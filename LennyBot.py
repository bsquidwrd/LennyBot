import aiohttp
import asyncio
import copy
import credentials
import datetime
import discord
import json
import logging
import os
import re
import sys
import traceback
from collections import Counter
from discord.ext import commands


description = """
Hello! I am a bot written by Isk to provide lennyface for your amusement
"""

count_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'count.txt')
logChannel = credentials.logChannel
DISCORD_BOTS_API ='https://bots.discord.pw/api'
dbots_key = credentials.dbots_key
invite_url = credentials.invite_url

log = logging.getLogger(__name__)

class LennyBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=None, description=description,
                         pm_help=None, help_attrs=dict(hidden=True))

        self.client_token = credentials.token
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.currentStatus = 0


    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        self.task_runner = self.loop.create_task(self.bot_status_changer())
        self.log_channel = discord.utils.get(self.get_all_channels(), id=logChannel)

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_resumed(self):
        print('resumed...')


    async def on_server_join(server):
        await self.log_channel.send(':heart: Lenny was added to ' + str(server) + ' - ' + str(sum(1 for e in server.members)))
        await self.update()


    async def on_server_remove(server):
        await self.log_channel.send(':broken_heart: Lenny was removed from ' + str(server))
        await self.update()


    async def update():
        payload = json.dumps({
            'server_count': len(self.guilds)
        })

        headers = {
            'authorization': dbots_key,
            'content-type': 'application/json'
        }

        url = '{0}/bots/{1.user.id}/stats'.format(DISCORD_BOTS_API, client)
        async with session.post(url, data=payload, headers=headers) as resp:
            await self.log_channel.send('DBots statistics returned {0.status} for {1}'.format(resp, payload))


    async def bot_status_changer(self):
        try:
            while not self.is_closed:
                if self.currentStatus == 0:
                    game_message = '@Lenny'
                if self.currentStatus == 1:
                    game_message = 'lennyface'
                if self.currentStatus == 2:
                    with open(count_file, 'r+') as f:
                        value = int(f.read())
                        game_message = '{} lennys called'.format(str(value))
                if self.currentStatus == 3:
                    game_message = 'PM for help/info'

                await self.change_presence(game=discord.Game(name=(game_message)))

                self.currentStatus += 1
                if self.currentStatus >= 4:
                    self.currentStatus = 0

                await asyncio.sleep(20) # task runs every 20 seconds
        except asyncio.CancelledError as e:
            pass


    async def on_message(self, message):
        if message.author != self.user and not message.author.bot:
            channel = message.channel
            if message.author.id == credentials.owner:
                servers = []
                if 'servers' in message.content.lower():
                    numServers = 0
                    for server in self.guilds:
                        numServers+=1
                        servers.append(server.name)

                    await self.log_channel.send(str(numServers) + ' servers, ' + str(sum(1 for _ in self.get_all_members())) + ' users.')

            if type(channel) != discord.channel.TextChannel:
                await self.log_channel.send(':mailbox_with_mail: ' + message.author.name + ' - ' + message.clean_content)

                # with channel.typing():
                if 'lennyface' in message.content.lower() or self.user.mentioned_in(message) and not message.mention_everyone:
                    await channel.send('( ͡° ͜ʖ ͡°)')

                else:
                    embed = discord.Embed(title = "Invite Lenny:", color = 0xD1526A)
                    embed.description = "[Click me!]({})".format(invite_url)
                    avatar = self.user.avatar_url or self.user.default_avatar_url
                    embed.set_author(name = "Lenny (Discord ID: {})".format(self.user.id), icon_url = avatar)
                    embed.add_field(name = "Triggers: ", value = "`lennyface`\n{}".format(self.user.mention))
                    me = discord.utils.get(self.get_all_members(), id=credentials.owner)
                    avatar = me.default_avatar_url if not me.avatar else me.avatar_url
                    embed.set_footer(text = "Developer/Owner: {0} (Discord ID: {0.id})".format(me), icon_url = avatar)
                    await channel.send('', embed = embed)
                    await channel.send('Support server: https://discord.gg/nwYjRz4')

            ## Lennyface send / delete
            if 'lennyface' in message.content.lower() or self.user.mentioned_in(message) and not message.mention_everyone:
                if type(channel) == discord.channel.TextChannel:
                    await channel.send('( ͡° ͜ʖ ͡°)')
                    await self.log_channel.send('[' + message.author.guild.name + '] ' + message.author.name + ' - ' + message.clean_content)

                if (message.content.lower() == 'lennyface') or (message.content.lower() == self.user.mention):
                    try:
                        await message.delete()
                    except Exception as e:
                        print(e)

                # Log lenny count
                with open(count_file,'r+') as f:
                    value = int(f.read())
                    f.seek(0)
                    f.write(str(value + 1))

            elif 'lenny' in message.content.lower():
                await self.log_channel.send('[' + message.author.server.name + '] ' + message.author.name + ' - ' + message.clean_content)


    async def close(self):
        await super().close()
        await self.session.close()


    def run(self):
        super().run(self.client_token, reconnect=True)


if __name__ == '__main__':
    bot = LennyBot()
    bot.run()
