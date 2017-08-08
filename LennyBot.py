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

        self.loop.create_task(self.bot_status_changer())
        self.log_channel = discord.utils.get(self.get_all_channels(), id=logChannel)

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_resumed(self):
        print('resumed...')


    async def on_guild_join(self, guild):
        await self.log_channel.send(':heart: Lenny was added to {} - {}'.format(str(guild), str(len(guild.members))))
        await self.update()


    async def on_guild_remove(self, guild):
        await self.log_channel.send(':broken_heart: Lenny was removed from {}'.format(str(guild)))
        await self.update()


    async def update(self):
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
        while not self.is_closed():
            try:
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

                await asyncio.sleep(20)
            except asyncio.CancelledError as e:
                pass
            except Exception as e:
                print(e)


    async def on_message(self, message):
        if message.author != self.user and not message.author.bot:
            channel = message.channel
            if message.author.id == credentials.owner:
                if 'servers' in message.content.lower():
                    numServers = len(self.guilds)
                    numUsers = sum(1 for i in self.get_all_members())
                    await self.log_channel.send('{} servers, {} users.'.format(str(numServers), str(numUsers)))

            if type(channel) != discord.channel.TextChannel:
                await self.log_channel.send(':mailbox_with_mail: {0.author.name} - {0.clean_content}'.format(message))

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
                    await self.log_channel.send('[{0.author.guild.name}] {0.author.name} - {0.clean_content}'.format(message))

                if (message.content.lower() == 'lennyface') or (message.content.lower() == self.user.mention):
                    try:
                        await message.delete()
                    except discord.Forbidden as e:
                        pass
                    except Exception as e:
                        print(e)

                # Log lenny count
                with open(count_file,'r+') as f:
                    value = int(f.read())
                    f.seek(0)
                    f.write(str(value + 1))

            elif 'lenny' in message.content.lower():
                if type(channel) == discord.channel.TextChannel:
                    await self.log_channel.send('[{0.author.guild.name}] {0.author.name} - {0.clean_content}'.format(message))
                else:
                    await self.log_channel.send(':mailbox_with_mail: {0.author.name} - {0.clean_content}'.format(message))


    async def close(self):
        await super().close()
        await self.session.close()


    def run(self):
        super().run(self.client_token, reconnect=True)


if __name__ == '__main__':
    bot = LennyBot()
    bot.run()
