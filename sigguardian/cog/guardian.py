import discord
from discord.ext import commands
from sigguardian.data_models import User, Signature, Mistake

class guardian(commands.Cog):
    def __init__(self, bot, db_session):
        self.bot = bot
        self.db_session = db_session
    
    async def on_mistake(self, user, msg):
        user.mistakes.append(Mistake(contents=msg.content, discord_guild_id=msg.guild.id, discord_channel_id=msg.channel.id, discord_message_id=msg.id))
        self.db_session.commit()

        await msg.channel.send('{0} did you forget about something?'.format(msg.author.mention))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.startswith(self.bot.command_prefix):
            return

        user = self.db_session.query(User).filter(User.discord_user_id == msg.author.id).first()
        
        if user:
            missing_sig = True
            
            if any(signature.signature in msg.content for signature in user.signatures): 
                missing_sig = False
            
            if missing_sig:
                await self.on_mistake(user, msg)
        

    @commands.command(name='help')
    async def show_help(self, ctx):

        emb = discord.Embed(title='',
                description='''Commands : 
                ''')
        await ctx.send(embed=emb)

    @commands.command(name='register')
    async def register_user(self, ctx, *signatures):
        user = self.db_session.query(User).filter(User.discord_user_id == ctx.author.id).first()

        if user:
            await ctx.send('{0}, you are already registered.'.format(ctx.author.mention))
        else:
            user = User(discord_user_id=ctx.author.id)
            self.db_session.add(user)
            self.db_session.commit()

            user.signatures.extend([Signature(signature=sig) for sig in signatures])

            self.db_session.commit()
            await ctx.send('{0}, you have been registered successfully'.format(ctx.author.mention))

    @commands.command(name='leave')
    async def remove_user(self, ctx):
        user = self.db_session.query(User).filter(User.discord_user_id == ctx.author.id).first()

        if user:
            self.db_session.delete(user)

            await ctx.send('{0}, you have been unregistered successfully'.format(ctx.author.mention))
        else:
            await ctx.send('{0}, you are not registered'.format(ctx.author.mention))

    @commands.command(name='mistakes')
    async def list_mistakes(self, ctx):
        user = self.db_session.query(User).filter(User.discord_user_id == ctx.author.id).first()
        emb = discord.Embed(title='Your recent mistakes : ')
        content_str = ''
        links_str = ''
        channel_str = ''

        if user:
            for mistake in reversed(user.mistakes):
                newline_count = mistake.contents.count('\n')
                content_str += mistake.contents + '\r\n'
                links_str +='[Link!](https://discordapp.com/channels/{0.discord_guild_id}/{0.discord_channel_id}/{0.discord_message_id})'.format(mistake)
                links_str += '\r\n' * (newline_count + 1)
                channel_str += '<#{0.discord_channel_id}>'.format(mistake)
                channel_str += '\r\n' * (newline_count + 1)

            emb.add_field(name='Content', value=content_str)
            emb.add_field(name='Channel', value=channel_str)
            emb.add_field(name='Link', value=links_str)

            await ctx.send('', embed=emb)

    @commands.command(name='add')
    async def add_signature(self, ctx, sig):
        user = self.db_session.query(User).filter(User.discord_user_id == ctx.author.id).first()

        if user:
            if any(signature.signature == sig for signature in user.signatures):
                await ctx.send('This signature is already added.')
                return

            user.signatures.append(Signature(signature=sig))
            self.db_session.commit()

            await ctx.send('Successfully added signature {0}.'.format(sig))

    @commands.command(name='delete')
    async def delete_signature(self, ctx, sig):
        user = self.db_session.query(User).filter(User.discord_user_id == ctx.author.id).first()

        if user:
            for signature in user.signatures:
                if signature.signature == sig:
                    self.db_session.delete(signature)
                    self.db_session.commit()
                    await ctx.send('Successfully removed signature {0}.'.format(sig))
                    return


    @commands.command(name='list')
    async def list_signatures(self, ctx):
        user = self.db_session.query(User).filter(User.discord_user_id == ctx.author.id).first()

        if user:
            emb = discord.Embed(title='Your registered signatures: ')

            emb.add_field(name='Signature', value='\r\n'.join([sig.signature for sig in user.signatures]))
            emb.add_field(name='User', value=ctx.author.mention)

            await ctx.send('', embed=emb)

