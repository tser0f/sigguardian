import sigguardian.cog.guardian
import importlib
import conf

from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def setup_dbsession():
    engine = create_engine(conf.ini_config.get('sqlalchemy', 'connection_string'))    
    
    sessionm = sessionmaker()
    sessionm.configure(bind=engine)
    return sessionm()

def setup(bot):
    print('sigguardian extension loading.')

    dbsession = setup_dbsession()
    importlib.reload(sigguardian.cog.guardian)
    bot.remove_command('help')
    bot.add_cog(sigguardian.cog.guardian.guardian(bot, dbsession))


def teardown(bot):
    print('sigguardian extension unloading')
    bot.remove_cog('guardian')
