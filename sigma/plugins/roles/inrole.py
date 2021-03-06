﻿import discord


async def inrole(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        role_input = ' '.join(args)
        role_choice = None
        user_list = ''
        for role in message.server.roles:
            if role.name.lower() == role_input.lower():
                role_choice = role
        if not role_choice:
            embed = discord.Embed(color=0x696969, title=':notebook: No channel like that was found on this server.')
        else:
            embed = discord.Embed(color=0x0099FF)
            for member in message.server.members:
                for role in member.roles:
                    if role == role_choice:
                        user_list += '\n - ' + member.name
            embed.add_field(name='ℹ The Following Users Are In ' + role_choice.name,
                            value='```haskell\n' + user_list + '\n```')
        await cmd.bot.send_message(message.channel, None, embed=embed)
