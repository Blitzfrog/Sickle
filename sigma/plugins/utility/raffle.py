﻿import random
import discord
from sigma.core.permission import check_admin

async def raffle(cmd, message, args):
    if check_admin(message.author, message.channel):
        user_list = []
        for member in message.server.members:
            status = str(member.status)
            if not member.bot:
                if status == 'offline':
                    pass
                else:
                    user_list.append(member.id)
        winner = random.choice(user_list)
        embed = discord.Embed(title=':tada: Congrats! You won the raffle!', color=0x1ABC9C)
        await cmd.bot.send_message(message.channel, 'Hey <@' + winner + '>!', embed=embed)
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
