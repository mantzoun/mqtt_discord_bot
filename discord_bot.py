#!/usr/bin/env python3
import os
import asyncio
import datetime

import discord
import config
from my_io import myIO

from mqtt_device import Device

intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents = intents)

deviceList = []
token = ""
my_guild = None

async def __send_message(message, channel):
    await channel.send(message)

async def send_message(message, channel = "general"):
    chan = discord.utils.get(my_guild.text_channels, name=channel)
    await __send_message(message, chan)

@bot.event
async def on_raw_reaction_add(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    user = payload.member

    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute

    if user == bot.user:
        return

    dev = find_device(message)
    if not dev:
        return

    if str(payload.emoji) == "✅":
        await message.remove_reaction("✅", user)
        if dev.status != "off":
            return

        dev.set_on(user)
        await message.add_reaction("❌")
        await message.remove_reaction("✅", bot.user)

        await message.edit(content = ("%s αναψε στις %02d:%02d απο τον/την %s" %
                                        (dev.get_name(), hour, minute, str(user))))
    if str(payload.emoji) == "❌":
        await message.remove_reaction("❌", user)
        if dev.status != "on":
            return

        dev.set_off(user)
        await message.add_reaction("✅")
        await message.remove_reaction("❌", bot.user)

        await message.edit(content = ("%s έσβησε στις %02d:%02d απο τον/την %s, μετά από %d λεπτά" %
                                        (dev.get_name(), hour, minute, str(user), dev.get_last_on_duration())))

@bot.event
async def on_ready():
    global my_guild

    print(f'{bot.user} has connected to Discord!')

    for guild in bot.guilds:
        print(f"Guild_id {guild.id}")
        my_guild = guild

        overwrites_h = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            discord.utils.get(guild.roles, name="Household"): discord.PermissionOverwrite(read_messages=True),
            discord.utils.get(guild.roles, name="Household"): discord.PermissionOverwrite(send_messages=False)
        }

        try:
            channel = discord.utils.get(guild.text_channels, name='general')
            cat_h = discord.utils.get(guild.categories, name='Home Automation')
            if not cat_h:
                cat_h = await guild.create_category("Home Automation", overwrites = overwrites_h)

            cat_c = discord.utils.get(guild.categories, name='Comics')
            if not cat_c:
                cat_c = await guild.create_category("Comics")

            if not discord.utils.get(cat_h.text_channels, name='devices'):
                await guild.create_text_channel('Devices', category = cat_h)

            chan = discord.utils.get(cat_h.text_channels, name='devices')
            await chan.purge(limit=10000)

            for dev in deviceList:
                dev_msg = await chan.send(dev.get_name())
                dev.set_msg(dev_msg)

                await dev_msg.add_reaction("✅")

            if not discord.utils.get(cat_c.text_channels, name='calvin'):
                await guild.create_text_channel('Calvin', category = cat_c)

            if not discord.utils.get(cat_c.text_channels, name='dilbert'):
                await guild.create_text_channel('Dilbert', category = cat_c)

            if not discord.utils.get(cat_c.text_channels, name='garfield'):
                await guild.create_text_channel('Garfield', category = cat_c)

        except Exception as e:
            print(e)

@bot.event
async def setup_hook():
    my_io = myIO(config.fifo_path, message_parser)
    bot.loop.create_task(io_task(my_io))

async def io_task(my_io):
    await my_io.receive()

def init(t):
    global token
    token = t

async def message_parser(data):
    print("RCV")
    fields = data.strip().split('#')
    for field in fields:
        print(field)
    await send_message(data)

def start():
    bot.run(token)

def add_device(dev_name):
    deviceList.append(Device(dev_name))

def find_device(message):
    for dev in deviceList:
        if message == dev.get_msg():
            return dev
    return None

