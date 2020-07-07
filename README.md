# sigguardian
A discord bot to enforce user signatures

## Features
## Requirements
This project uses python 3, [discord.py](https://github.com/Rapptz/discord.py), and [sqlalchemy](https://www.sqlalchemy.org).
You can check your python version by running `python --version`.

You can install discord.py and sqlalchemy with pip : 
```
python3 -m pip install -U discord.py
python3 -m pip install -U sqlalchemy
```

## Usage/installation
1. Create a copy of config.ini named config.dev.ini. (you can change the naming in conf.py)
2. Put your discord token next to `token=` and change any other options you'd like
3. Run `python3 setup_db.py`, this will create the database for the bot.
4. Run `python3 sigguardian.py`. You should see the following if the bot is running correctly:
```
sigguardian extension loading.
your_bot_name has connected to Discord!
```

## Usage on discord
### Commands : 
### Examples : 
