﻿import discord


async def invite(cmd, message, args):
    embed = discord.Embed(title='ℹ Click here to invite me to your Discord server.', color=0x0099FF, url='\nhttps://discordapp.com/oauth2/authorize?client_id=' + cmd.bot.user.id + '&scope=bot&permissions=8')
    await cmd.bot.send_message(message.channel, None, embed=embed)
