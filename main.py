#!/usr/bin/env python3
import os

import config
import discord_bot
from mqtt_device import Device

if __name__ == "__main__":
    discord_bot.init(config.token)

    discord_bot.add_device("Θερμοσίφωνο")
    discord_bot.add_device("Καλοριφέρ")

    discord_bot.start()
