﻿import discord
from sigma.core.permission import check_admin


async def cleverbot(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.server.id, 'CleverBot')
        if active:
            cmd.db.set_settings(message.server.id, 'CleverBot', False)
            state = '**Disabled**.'
        else:
            cmd.db.set_settings(message.server.id, 'CleverBot', True)
            state = '**Enabled**.'
        embed = discord.Embed(title='✅ CleverBot Feature Has Been ' + state + '.', color=0x66CC66)
    await cmd.bot.send_message(message.channel, None, embed=embed)
