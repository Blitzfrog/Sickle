import discord
from sigma.core.permission import check_admin


async def bye(cmd, message, args):
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted. Server Admin Only.', color=0xDB0000)
    else:
        active = cmd.db.get_settings(message.server.id, 'Bye')
        greet_channel = cmd.db.get_settings(message.server.id, 'ByeChannel')
        if not active:
            cmd.db.set_settings(message.server.id, 'Bye', True)
            if not greet_channel:
                cmd.db.set_settings(message.server.id, 'ByeChannel', message.server.default_channel.id)
            embed = discord.Embed(color=0x66CC66,
                                  title='✅ Goodbye Messages Enabled')
        else:
            cmd.db.set_settings(message.server.id, 'Bye', False)
            embed = discord.Embed(color=0x66CC66,
                                  title='✅ Goodbye Messages Disabled')
    await cmd.bot.send_message(message.channel, None, embed=embed)
