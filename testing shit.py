#import discord

#help(discord.message)

fruits = ['banana', 'apple',  'mango']
message = "this banana is good"

#if any(fruit in message for fruit in fruits):        # traversal of List sequence
#   print ('Current fruit :', fruit)

for fruit in fruits:
    if fruit in message:
        print ('Current fruit :', fruit)