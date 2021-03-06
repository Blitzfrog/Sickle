﻿import discord
from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role


async def destroyrole(cmd, message, args):
    if not check_man_roles(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Not Enough Arguments', value=cmd.help())
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    role_qry = ' '.join(args)
    target_role = matching_role(message.server, role_qry)
    if not target_role:
        out_content = discord.Embed(type='rich', color=0xFF9900, title='❗ Error')
        out_content.add_field(name='Role Not Found', value='I was unable to find **' + role_qry + '** on this server.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        await cmd.bot.delete_role(message.server, target_role)
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title='✅ Role ' + role_qry + ' destroyed.')
        await cmd.bot.create_role(message.server, name=role_qry)
        await cmd.bot.send_message(message.channel, None, embed=out_content)
