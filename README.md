# LennyBot ( ͡° ͜ʖ ͡°)
A stupid and simple bot to supply easy access to the face of Lenny.

If you want to add Lenny to your server without running from source click [here.](https://discordapp.com/oauth2/authorize?client_id=193179442665750528&scope=bot&permissions=0x00002000)

The bot is triggered by the phrase `lennyface` and simply posts ( ͡° ͜ʖ ͡°) in the chat and deletes the invoking message.
The message is only deleted if the only text present is `lennyface`.

## Requirements
* Python (Preferably 3.5+)

* This bot uses the [discord.py API wrapper](https://github.com/Rapptz/discord.py), you'll need to set that up for this bot to work.

## Usage

1. Create a bot account using the [discord developer section.](https://discordapp.com/developers/applications/me)
2. Add your bot token in `credentials.py`

3. Add the bot to your server using the OAUTH url:
  * `https://discordapp.com/oauth2/authorize?client_id=BOTCLIENTIDHERE&scope=bot&permissions=0x00002000`
  * (If you give the bot permissions to manage messages on your server it will delete the invoking lennyface message.)
  * :exclamation: Make sure to insert your bots client ID in the url.

4. Start the bot using `python LennyBot.py`.

### Extra bits
Thanks to Rapptz for the discord.py wrapper.

If you want any help feel free to join my [testing server](https://discord.gg/0n4QSS0mmQNtD5Ve) and message me.
