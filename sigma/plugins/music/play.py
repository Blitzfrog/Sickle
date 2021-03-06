import discord
import asyncio
from sigma.core.utils import user_avatar
from .init_clock import init_clock


async def play(cmd, message, args):
    if args:
        task = cmd.bot.plugin_manager.commands['queue'].call(message, args)
        cmd.bot.loop.create_task(task)
        player = cmd.music.get_player(message.server.id)
        if player:
            if player.is_playing():
                return
        await asyncio.sleep(3)
    if message.server.id not in cmd.music.initializing:
        if not message.author.voice_channel:
            embed = discord.Embed(
                title='⚠ I don\'t see you in a voice channel', color=0xFF9900)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return

        srv_queue = cmd.music.get_queue(message.server.id)
        if len(srv_queue.queue) == 0:
            embed = discord.Embed(
                title='⚠ The queue is empty', color=0xFF9900)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
        cmd.music.add_init(message.server.id)
        cmd.bot.loop.create_task(init_clock(cmd.music, message.server.id))
        voice_connected = cmd.bot.is_voice_connected(message.server)
        if not voice_connected:
            try:
                await cmd.bot.join_voice_channel(message.author.voice_channel)
                embed = discord.Embed(title='✅ Joined ' + message.author.voice_channel.name,
                                      color=0x66cc66)
            except Exception as e:
                cmd.log.error(f'ERROR: {e} | TRACE: {e.with_traceback}')
                embed = discord.Embed(color=0xDB0000)
                embed.add_field(name='❗ I was unable to connect.',
                                value='The most common cause is your server being too far or a poor connection.')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        player = cmd.music.get_player(message.server.id)
        if player:
            if player.is_playing():
                embed = discord.Embed(
                    title='⚠ Already playing in ' + cmd.bot.voice_client_in(message.server).channel.name,
                    color=0xFF9900)
                await cmd.bot.send_message(message.channel, None, embed=embed)
                return
        voice_instance = cmd.bot.voice_client_in(message.server)
        while cmd.music.get_queue(message.server.id) and len(cmd.music.get_queue(message.server.id).queue) != 0:
            item = cmd.music.get_from_queue(message.server.id)
            if message.server.id in cmd.music.repeaters:
                cmd.music.add_to_queue(message.server.id, item)
            cmd.music.currents.update({message.server.id: item})
            sound = item['sound']
            await cmd.music.make_player(message.server.id, voice_instance, item)
            player = cmd.music.get_player(message.server.id)
            if not player:
                return
            def_vol = cmd.music.get_volume(cmd.db, message.server.id)
            player.volume = def_vol / 100
            player.start()
            cmd.db.add_stats('MusicCount')
            embed = discord.Embed(color=0x0099FF)
            if item['type'] == 0:
                embed.add_field(name='🎵 Now Playing', value=sound.title)
                embed.set_thumbnail(url=sound.thumb)
                embed.set_author(name=f'{item["requester"].name}#{item["requester"].discriminator}',
                                 icon_url=user_avatar(item['requester']), url=item['url'])
                embed.set_footer(text=f'Duration: {sound.duration}')
            elif item['type'] == 1:
                embed.add_field(name='🎵 Now Playing', value=sound['title'])
                embed.set_thumbnail(url=sound['artwork_url'])
                embed.set_author(name=f'{item["requester"].name}#{item["requester"].discriminator}',
                                 icon_url=user_avatar(item['requester']), url=item['url'])
            else:
                return
            await cmd.bot.send_message(message.channel, None, embed=embed)
            while not player.is_done():
                await asyncio.sleep(2)
            cmd.music.kill_player(message.server.id)
        try:
            await voice_instance.disconnect()
        except:
            pass
        del cmd.music.currents[message.server.id]
    else:
        cmd.log.warning('Play Command Ignored Due To Server Being In The Music Initialization List')
