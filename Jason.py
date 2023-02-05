#Jason discord bot with base functionality
#pulls from youtube and plays music
#pulls from reddit and posts old memes

#base imports
import discord
import asyncio
import youtube_dl
import praw
import random
import os
import time
import datetime
import json
import requests
import urllib.request
import urllib.parse
import urllib.error
import re
import sys
import traceback
import subprocess
import shlex
import shutil
import glob
import logging
import logging.handlers
import threading
import queue
import collections
import functools
import inspect
import itertools
import math
import operator

#discord imports
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CommandOnCooldown
from discord.ext.commands import MissingPermissions
from discord.ext.commands import BadArgument
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands import CommandInvokeError
from discord.ext.commands import CommandError
from discord.ext.commands import NoPrivateMessage
from discord.ext.commands import DisabledCommand

#youtube imports
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import opus
from discord import Game
from discord import Embed
from discord import Colour
from discord import Status
from discord import ChannelType
from discord import File
from discord import Member
from discord import Role
from discord import Object
from discord import Permissions
from discord import utils
from discord import Spotify
from discord import Game
from discord import Activity
from discord import ActivityType

#reddit imports
from praw.models import MoreComments
from praw.models import Submission
from praw.models import Comment
from praw.models import Redditor
from praw.models import Message
from praw.models import Subreddit
from praw.models import Inbox
from praw.models import SubredditMessage
from praw.models import SubredditStream
from praw.models import LiveThread
from praw.models import LiveUpdate
from praw.models import LiveContributor
from praw.models import LiveThreadContribution
from praw.models import LiveUpdateContribution
from praw.models import LiveHelper
from praw.models import ModAction


#bot setup
bot = commands.Bot(command_prefix='j')
bot.remove_command('help')

#bot startup
@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Game(name="jhelp"))

#bot commands
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#base bot functionality
@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('**Now playing:** {}'.format(player.title))

@bot.command()
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()

@bot.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()

@bot.command()
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.resume()

@bot.command()
async def volume(ctx, volume: int):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.source.volume = volume / 100
    await ctx.send("Changed volume to {}%".format(volume))

@bot.command()
async def queue(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('**Now playing:** {}'.format(player.title))

@bot.command()
async def skip(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()

#bot responses

#bot says "you guys are dicks" when someone says "Big suit"
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "Big suit" in message.content:
        await message.channel.send("You guys are dicks")
    await bot.process_commands(message)

#bot says "I'm gonna eat your ass" when someone says "Shut up jason"
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "Shut up Jason" in message.content:
        await message.channel.send("I'm gonna eat your ass")
        await bot.process_commands(message)

#bot posts a random picture from JasonPics folder
