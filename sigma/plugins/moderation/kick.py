﻿from sigma.core.permission import check_kick
import discord


async def kick(cmd, message, args):
    channel = message.channel
    if message.mentions:
        user_q = message.mentions[0]
        if message.author is not user_q:
            if check_kick(message.author, channel):
                await cmd.bot.kick(user_q)
                out_content = discord.Embed(color=0x993300,
                                            title=':boot: User **' + user_q.name + '** has been kicked!')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
            else:
                out_content = discord.Embed(color=0xDB0000,
                                            title='⛔ Insufficient Permissions. Users with Kick permissions only.')
                await cmd.bot.send_message(message.channel, None, embed=out_content)
        else:
            await cmd.bot.send_message(message.channel, cmd.help())
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
